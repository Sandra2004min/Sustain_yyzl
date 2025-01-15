import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def scrape_articles(base_url, total_pages):
    all_articles = []

    # Set up a session with retry strategy
    session = requests.Session()
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    for page in tqdm(range(1, total_pages + 1), desc="Scraping pages", unit="page"):
        url = f"{base_url}={page}"
        try:
            response = session.get(url, timeout=10)  # Set timeout
            if response.status_code != 200:
                print(f"Failed to fetch the page {page}: {response.status_code}")
                continue

            soup = BeautifulSoup(response.text, 'html.parser')

            # Locate the container with the articles
            container = soup.find('div', class_='xinwen-list2')
            if not container:
                print(f"No article container found on page {page}.")
                continue

            # Extract article details from the list items
            for li in container.find_all('li'):
                date_span = li.find('span', class_='fr')
                a_tag = li.find('a', href=True)

                if date_span and a_tag:
                    publication_date = date_span.text.strip()
                    title = a_tag.text.strip()
                    link = a_tag['href'].strip()
                    full_link = f"https://www.shccig.com{link}"

                    all_articles.append({
                        'title': title,
                        'link': full_link,
                        'date': publication_date
                    })

        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}")

    return all_articles

def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Usage
base_url = "https://www.shccig.com/articles/14?page"
total_pages = 78
articles = scrape_articles(base_url, total_pages)

# Save articles to a JSON file
save_to_json(articles, "articles.json")

print(f"Scraped {len(articles)} articles and saved to articles.json.")

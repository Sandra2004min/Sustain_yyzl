import requests
from bs4 import BeautifulSoup
import json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# Load the JSON file containing article links
with open("articles.json", "r", encoding="utf-8") as json_file:
    articles = json.load(json_file)

# List to store article content
article_contents = []

# Headers to mimic a browser visit
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36"
}

# Create a session with retry strategy
session = requests.Session()
retries = Retry(total=5, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
session.mount("https://", HTTPAdapter(max_retries=retries))

def fetch_article_content(article):
    link = article.get("link")
    title = article.get("title")
    publication_date = article.get("publication_date")

    if link:
        try:
            # Send a GET request to the article link with a timeout
            response = session.get(link, headers=headers, timeout=10)

            if response.status_code == 200:
                # Parse the HTML content
                soup = BeautifulSoup(response.text, "html.parser")

                # Find the article content
                content_div = soup.find("div", class_="mt-4 article-content")

                if content_div:
                    content = content_div.get_text(strip=True)
                else:
                    content = "Content not found"

                return {
                    "title": title,
                    "link": link,
                    "publication_date": publication_date,
                    "content": content
                }
            else:
                print(f"Failed to retrieve content for {link}. Status code: {response.status_code}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error retrieving content for {link}: {e}")
            return None
    return None

# Use ThreadPoolExecutor for multithreading
with ThreadPoolExecutor(max_workers=10) as executor:
    # Submit tasks to the executor
    future_to_article = {executor.submit(fetch_article_content, article): article for article in articles}

    # Use tqdm for progress bar
    for future in tqdm(as_completed(future_to_article), total=len(future_to_article)):
        result = future.result()
        if result:
            article_contents.append(result)

# Save the article contents to a JSON file
with open("article_contents.json", "w", encoding="utf-8") as json_file:
    json.dump(article_contents, json_file, ensure_ascii=False, indent=4)

print("Article contents saved to article_contents.json")

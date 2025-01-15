import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

def fetch_article_content(link):
    """Fetch text content from the article page."""
    try:
        response = requests.get(link, timeout=10)
        if response.status_code != 200:
            print(f"Failed to fetch the article: {link}, Status Code: {response.status_code}")
            return ""

        soup = BeautifulSoup(response.text, 'html.parser')
        article_container = soup.find('div', class_='article-con', style='padding-top:20px;')
        if not article_container:
            print(f"No article content found for: {link}")
            return ""

        # Extract and concatenate all text from <p> tags inside the container
        paragraphs = article_container.find_all('p')
        text_content = ""
        for p in paragraphs:
            if p.string:  # Only include pure text content
                text_content += p.string.strip() + "\n"

        return text_content.strip()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching article {link}: {e}")
        return ""

def process_articles(json_file):
    """Load articles from JSON and fetch their content with multithreading."""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            articles = json.load(f)
    except FileNotFoundError:
        print(f"File {json_file} not found.")
        return

    result = []

    # Extract links for processing
    tasks = [(article.get('link'), article.get('title'), article.get('date')) for article in articles if article.get('link')]

    def process_task(task):
        link, title, date = task
        content = fetch_article_content(link)
        return {
            'title': title,
            'date': date,
            'link': link,
            'content': content
        }

    # Use ThreadPoolExecutor for multithreading
    with ThreadPoolExecutor(max_workers=10) as executor:
        for article_data in tqdm(executor.map(process_task, tasks), total=len(tasks), desc="Fetching articles", unit="article"):
            result.append(article_data)

    # Save the result to a new JSON file
    output_file = "articles_with_content.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

    print(f"Processed {len(result)} articles. Results saved to {output_file}.")

# Usage
json_file = "articles.json"  # JSON file containing article links
process_articles(json_file)

import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm

def fetch_article_content(url):
    """Fetch the content of an article given its URL."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find the content within <div class="dtl_detail">
        content_div = soup.find('div', class_='dtl_detail')
        if content_div:
            return content_div.get_text(strip=True)
        else:
            return "Content not found"
    except requests.RequestException as e:
        print(f"Failed to fetch {url}: {e}")
        return "Error fetching content"

def read_articles_from_json(filename):
    """Read articles from a JSON file."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Error reading JSON file.")
        return []

def save_articles_with_content(articles, filename):
    """Save articles with content to a JSON file."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)

def fetch_all_article_contents(input_filename, output_filename):
    """Fetch the content for all articles in the JSON file and save them."""
    articles = read_articles_from_json(input_filename)

    for article in tqdm(articles, desc="Fetching article contents"):
        if 'content' not in article or not article['content']:
            article['content'] = fetch_article_content(article['url'])

    save_articles_with_content(articles, output_filename)

if __name__ == "__main__":
    input_filename = "articles.json"
    output_filename = "articles_with_content.json"

    fetch_all_article_contents(input_filename, output_filename)

    print(f"Article contents saved to {output_filename}")

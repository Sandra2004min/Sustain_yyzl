import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import time
import random
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session():
    session = requests.Session()
    retry = Retry(
        total=5,
        backoff_factor=1,
        status_forcelist=[500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

def fetch_news_content(url):
    session = create_session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }
    response = session.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch the webpage. Status code: {response.status_code}")
        return None
    soup = BeautifulSoup(response.text, 'html.parser')
    article_div = soup.find('div', class_='e_box p_articles')
    if article_div:
        return article_div.get_text(strip=True)
    else:
        print("No content found with the specified class.")
        return None

def update_content(item):
    try:
        link = item.get("link")
        if link:
            content = fetch_news_content(link)
            if content:
                item["content"] = content
            time.sleep(random.uniform(1, 3))  # 请求间隔
    except Exception as e:
        print(f"Error fetching content for {item.get('title')}: {e}")
    return item

if __name__ == "__main__":
    input_file = "demo.json"
    output_file = "updated_news.json"

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(tqdm(executor.map(update_content, data), total=len(data), desc="Fetching content"))

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    print(f"Content fetching completed and saved to {output_file}")


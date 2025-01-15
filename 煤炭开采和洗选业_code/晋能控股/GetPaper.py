import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# 读取之前保存的文章链接
input_file = "articles.json"
output_file = "article_contents.json"

# 设置请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}

# 加载文章链接
with open(input_file, "r", encoding="utf-8") as f:
    articles = json.load(f)

# 定义一个函数获取文章内容
def fetch_article_content(url):
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            content_div = soup.find('div', class_='v_news_content')
            if content_div:
                return content_div.get_text(strip=True)
            else:
                print(f"未找到文章内容: {url}")
                return None
        else:
            print(f"请求失败，状态码: {response.status_code}, URL: {url}")
            return None
    except Exception as e:
        print(f"请求失败，URL: {url}, 错误: {e}")
        return None

# 遍历文章链接，获取内容
article_contents = []

def process_article(article):
    link = article['link']
    title = article['title']
    publish_date = article['publish_date']

    content = fetch_article_content(link)
    if content:
        return {
            'title': title,
            'link': link,
            'publish_date': publish_date,
            'content': content
        }
    return None

# 使用多线程和进度条
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(process_article, article) for article in articles]
    for future in tqdm(as_completed(futures), total=len(futures), desc="Fetching articles"):
        result = future.result()
        if result:
            article_contents.append(result)

# 保存文章内容到JSON文件
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(article_contents, f, ensure_ascii=False, indent=4)

print(f"已获取文章内容，并保存到 {output_file}")

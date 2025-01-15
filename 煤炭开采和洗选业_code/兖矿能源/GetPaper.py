import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

# 请求头设置，模拟浏览器访问
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

# 读取保存的文章链接数据
with open('articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

# 定义函数处理微信链接
def process_weixin_link(url):
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找微信文章内容
        content_div = soup.find('div', class_='rich_media_content js_underline_content defaultNoSetting', id='js_content')
        if not content_div:
            return ""

        # 提取 span 标签中的文字内容
        text_content = []
        for span in content_div.find_all('span'):
            if span.string:  # 忽略图片等非文字内容
                text_content.append(span.get_text(strip=True))

        return "\n".join(text_content)
    except Exception as e:
        print(f"Error processing Weixin link {url}: {e}")
        return ""

# 定义函数处理兖矿能源链接
def process_shandong_link(url):
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找兖矿能源文章内容
        content_div = soup.find('div', class_='inner_content_con')
        if not content_div:
            return ""

        # 提取 p 标签中的文字内容
        text_content = []
        for p in content_div.find_all('p'):
            if p.string:  # 忽略非文字内容
                text_content.append(p.get_text(strip=True))

        return "\n".join(text_content)
    except Exception as e:
        print(f"Error processing Shandong link {url}: {e}")
        return ""

# 定义处理单篇文章的函数
def process_article(article):
    url = article.get('url')
    title = article.get('title')
    publish_at = article.get('publish_at')

    if 'mp.weixin.qq.com' in url:
        content = process_weixin_link(url)
    elif 'ykny.shandong-energy.com' in url:
        content = process_shandong_link(url)
    else:
        print(f"Unknown URL type: {url}")
        return None

    return {
        'title': title,
        'url': url,
        'publish_at': publish_at,
        'content': content
    }

# 使用多线程处理文章
processed_articles = []
with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(process_article, article) for article in articles]

    for future in tqdm(futures, desc="Processing Articles"):
        result = future.result()
        if result:
            processed_articles.append(result)

# 保存提取的内容到 JSON 文件
with open('processed_articles.json', 'w', encoding='utf-8') as f:
    json.dump(processed_articles, f, ensure_ascii=False, indent=4)

print(f"Processing completed. {len(processed_articles)} articles saved to 'processed_articles.json'.")

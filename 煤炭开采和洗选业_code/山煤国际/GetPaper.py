import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import time
import random

# 读取保存的 JSON 文件
with open('articles.json', 'r', encoding='utf-8') as json_file:
    articles = json.load(json_file)

# 定义解析函数，支持复杂结构
def fetch_article_content(article):
    link = article['link']
    title = article.get('title', '')  # 获取标题，默认为空字符串
    publish_date = article.get('publish_date', '')  # 获取发布日期，默认为空字符串

    try:
        # 设置随机延时，避免过于频繁访问
        time.sleep(random.uniform(1, 3))
        
        # 发起 GET 请求
        response = requests.get(link, timeout=10)
        response.encoding = 'utf-8'  # 设置为 utf-8 编码
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # 提取 id="js_content" 或 class="rich_media_content js_underline_content autoTypeSetting24psection"
            js_content = soup.find('div', id='js_content') or \
                         soup.find('div', class_='rich_media_content js_underline_content autoTypeSetting24psection')

            content_text = ""
            if js_content:
                # 优先提取 span 标签中的文字
                spans = js_content.find_all('span')
                if spans:
                    content_text = "".join(
                        span.get_text(strip=True) for span in spans if span.get_text(strip=True)
                    )
                else:
                    # 如果没有 span 标签，则提取 p 标签中的文字
                    paragraphs = js_content.find_all('p')
                    content_text = "".join(
                        p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)
                    )

            # 提取 class="bd" 的文字内容
            bd_content = ""
            bd_div = soup.find('div', class_='bd')
            if bd_div:
                # 优先提取 span 标签中的文字
                spans = bd_div.find_all('span')
                if spans:
                    bd_content = "".join(
                        span.get_text(strip=True) for span in spans if span.get_text(strip=True)
                    )
                else:
                    # 如果没有 span 标签，则提取 p 标签中的文字
                    paragraphs = bd_div.find_all('p')
                    bd_content = "".join(
                        p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)
                    )

            return {
                'link': link,
                'title': title,
                'publish_date': publish_date,
                'js_content_text': content_text,
                'bd_content_text': bd_content
            }

        else:
            print(f"请求失败，链接: {link}，状态码: {response.status_code}")
            return {
                'link': link,
                'title': title,
                'publish_date': publish_date,
                'js_content_text': "",
                'bd_content_text': ""
            }

    except Exception as e:
        print(f"请求出错，链接: {link}，错误: {e}")
        return {
            'link': link,
            'title': title,
            'publish_date': publish_date,
            'js_content_text': "",
            'bd_content_text': ""
        }

# 使用多线程和进度条来加速处理
with ThreadPoolExecutor(max_workers=3) as executor:
    results = list(tqdm(executor.map(fetch_article_content, articles), total=len(articles), desc="Fetching Articles"))

# 保存所有文章内容到 JSON 文件
with open('article_contents.json', 'w', encoding='utf-8') as json_file:
    json.dump(results, json_file, ensure_ascii=False, indent=4)

print("文章内容已保存到 article_contents.json 文件！")

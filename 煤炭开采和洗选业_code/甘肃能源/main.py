import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from tqdm import tqdm
import json

def fetch_articles_with_cookies(url):
    # 请求头
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Referer": "https://www.gnhtjt.com/col_jtxw/index/index-4.htm",
        "Sec-CH-UA": "\"Microsoft Edge\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "Sec-CH-UA-Mobile": "?0",
        "Sec-CH-UA-Platform": "\"Windows\"",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
    }
    
    # Cookie
    cookies = {
        "PHPSESSID": "aijc2n7b3lj2foksp3hl8gp07s"  # 替换为你的抓包中获取的 PHPSESSID
    }

    # 发送请求
    response = requests.get(url, headers=headers, cookies=cookies)

    # 检查响应状态
    if response.status_code == 200:
        # 强制设置编码为 UTF-8
        response.encoding = 'utf-8'
        return response.text
    else:
        print(f"Failed to fetch data from {url}: {response.status_code}")
        return None

def parse_articles(html, base_url):
    soup = BeautifulSoup(html, 'html.parser')
    articles = []

    # 找到文章列表的父容器
    articles_ul = soup.find('ul', class_='textlist')
    if not articles_ul:
        print("No articles found in the HTML.")
        return articles

    # 提取每篇文章的信息
    for li in articles_ul.find_all('li', class_='dcjtxw'):
        # 提取链接并补全
        a_tag = li.find('a', href=True)
        if not a_tag:
            continue
        article_url = urljoin(base_url, a_tag['href'])

        # 提取标题
        article_title = a_tag.get('title', 'No Title')

        # 提取发布时间
        time_div = li.find('div', class_='time')
        if time_div:
            day = time_div.find('p', class_='ri').get_text(strip=True)
            year_month = time_div.find('p', class_='ny').get_text(strip=True)
            publish_date = f"{year_month}-{day}"
        else:
            publish_date = "Unknown Date"

        # 添加到结果列表
        articles.append({
            'url': article_url,
            'title': article_title,
            'date': publish_date
        })

    return articles

def scrape_all_pages(start_page, end_page, base_url, page_url_template):
    all_articles = []

    # 爬取指定范围的页码
    for page in tqdm(range(start_page, end_page + 1), desc="Scraping pages"):
        if page == 1:
            url = page_url_template.replace("-index-\{page\}.htm", "/index.htm")
        else:
            url = page_url_template.format(page=page)

        html_content = fetch_articles_with_cookies(url)
        if html_content:
            articles = parse_articles(html_content, base_url)
            all_articles.extend(articles)

    return all_articles

def scrape_single_page(url, base_url):
    html_content = fetch_articles_with_cookies(url)
    if html_content:
        return parse_articles(html_content, base_url)
    return []

def save_articles_to_json(articles, filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = []

    existing_data.extend(articles)

    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

# 主函数
if __name__ == "__main__":
    base_url = "https://www.gnhtjt.com"
    page_url_template = "https://www.gnhtjt.com/col_jtxw/index/index-{page}.htm"

    # 爬取第 1 到第 96 页
    articles = scrape_all_pages(2, 96, base_url, page_url_template)

    # 保存文章信息到 JSON 文件
    save_articles_to_json(articles, "articles.json")

    # 单独爬取 https://www.gnhtjt.com/col_jtxw/index/index.htm
    single_page_url = "https://www.gnhtjt.com/col_jtxw/index/index.htm"
    single_page_articles = scrape_single_page(single_page_url, base_url)

    # 保存首页文章信息到 JSON 文件
    save_articles_to_json(single_page_articles, "articles.json")

    # 打印完成信息
    print(f"Scraped {len(articles) + len(single_page_articles)} articles and saved to articles.json")

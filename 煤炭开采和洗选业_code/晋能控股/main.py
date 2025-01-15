import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

# 设置请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}

# 定义一个函数来爬取页面的文章信息
def scrape_page(url):
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        articles = soup.select('div.bt-list ul li')
        article_list = []

        for article in articles:
            # 提取链接并补全
            a_tag = article.find('a')
            if a_tag:
                link = urljoin(url, a_tag['href'])
                title = a_tag.get_text(strip=True)
            else:
                link = None
                title = None

            # 提取发布时间
            em_tag = article.find('em', class_='col3')
            publish_date = em_tag.get_text(strip=True) if em_tag else None

            # 添加到结果列表
            if link and title and publish_date:
                article_list.append({
                    'title': title,
                    'link': link,
                    'publish_date': publish_date
                })
        return article_list
    else:
        print(f"请求失败，状态码: {response.status_code}, URL: {url}")
        return []

# 爬取第1页到第21页的文章信息
base_url = "https://jnkgmy.jnkgjtnews.com/myyw"
all_articles = []

for page in range(1, 22):  # 页码从1到21
    if page == 1:
        url = f"{base_url}.htm"  # 第1页的特殊URL
    else:
        url = f"{base_url}/{page}.htm"

    articles = scrape_page(url)
    all_articles.extend(articles)

# 将结果保存成JSON文件
output_file = "articles.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_articles, f, ensure_ascii=False, indent=4)

print(f"已爬取文章信息，并保存到 {output_file}")
import requests
from bs4 import BeautifulSoup
import json

# 定义基础 URL
base_url = "http://www.jznyjt.com/xinwenmeiti/jituandongtai/"
pages_to_scrape = range(2, 119)  # 从第2页到第118页的范围

# 保存所有文章信息
all_articles = []

def scrape_page(url):
    """爬取单个页面的文章信息"""
    response = requests.get(url)
    if response.status_code == 200:
        response.encoding = 'utf-8'  # 确保正确的编码解析
        soup = BeautifulSoup(response.text, 'html.parser')

        # 找到所有存放文章信息的 div 标签
        articles = soup.find_all('div', class_='col-lg-3 col-md-4 col-sm-6 padding-box')

        # 用来存储提取的文章信息
        articles_data = []

        for article in articles:
            # 提取文章链接和标题
            link_tag = article.find('a', class_='tit')
            if link_tag:
                link = link_tag.get('href')
                title = link_tag.get('title')

            # 提取发布时间
            date_tag = article.find('i')
            if date_tag:
                # 分别提取 b 和 u 标签内容
                day = date_tag.find('b').get_text(strip=True)
                year_month = date_tag.find('u').get_text(strip=True)
                full_date = f"{year_month}.{day}"  # 拼接为完整日期格式 YYYY.MM.DD

            # 将提取的数据保存到列表
            articles_data.append({
                'title': title,
                'link': link,
                'date': full_date
            })

        return articles_data
    else:
        print(f"请求失败，状态码: {response.status_code}, URL: {url}")
        return []

# 爬取首页文章信息
print("爬取首页文章信息...")
homepage_url = base_url + "index.html"
all_articles.extend(scrape_page(homepage_url))

# 爬取第2页到第118页的文章信息
for page in pages_to_scrape:
    print(f"爬取第 {page} 页文章信息...")
    page_url = f"{base_url}{page}.html"
    all_articles.extend(scrape_page(page_url))

# 保存为 JSON 文件
output_file = "articles.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(all_articles, f, ensure_ascii=False, indent=4)

print(f"爬取完成，共爬取 {len(all_articles)} 篇文章，保存到 {output_file}")

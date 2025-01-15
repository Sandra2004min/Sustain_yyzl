import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

# 保存结果的列表
data = []

# 基础URL
base_url = "http://www.shenhuachina.com"

# 定义函数来提取文章信息
def scrape_page(url):
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        content_div = soup.find('div', style="position: relative;")
        articles = content_div.find_all('div', class_='jcxw_t mtimg')

        for article in articles:
            link_tag = article.find('a', class_='jcxw_t_r_t_l').find_next('a')
            link = link_tag['href']
            full_link = urljoin(base_url, link)
            title = link_tag.get_text(strip=True)
            date_tag = article.find('b').find('span')
            date = date_tag.get_text(strip=True) if date_tag else "N/A"

            data.append({
                'title': title,
                'link': full_link,
                'date': date
            })
    except Exception as e:
        print(f"Error scraping {url}: {e}")

# 爬取第2页到第20页
for page in range(2, 21):
    url = f"http://www.shenhuachina.com/zgshww/xwtt/newslist_{page}.shtml"
    scrape_page(url)

# 爬取第一页（特殊链接）
first_page_url = "http://www.shenhuachina.com/zgshww/xwtt/newslist.shtml"
scrape_page(first_page_url)

# 将结果保存为JSON文件
output_file = "shenhua_articles.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"文章信息已保存到 {output_file}")

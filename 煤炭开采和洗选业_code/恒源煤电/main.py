import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

# 定义基础URL
base_url = "https://www.ahhymd.cn/info.php?class_id=102101&page={page}"
base_domain = "https://www.ahhymd.cn/"

# 存放所有文章信息的列表
all_articles = []

# 爬取1到14页内容
for page in range(1, 15):
    # 生成当前页的URL
    url = base_url.format(page=page)

    # 发送请求获取网页内容
    response = requests.get(url)
    response.encoding = 'utf-8'  # 确保使用正确的编码方式
    html_content = response.text

    # 解析HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # 提取<ul class="list">中的文章信息
    article_list = soup.find('ul', class_='list')
    if article_list:
        for li in article_list.find_all('li'):
            # 提取发布时间
            date_span = li.find('span', class_='d')
            pub_date = date_span.text.strip() if date_span else ''

            # 提取文章链接和标题
            a_tag = li.find('a')
            if a_tag:
                relative_link = a_tag['href']  # 获取相对链接
                full_link = urljoin(base_domain, relative_link)  # 补全为完整链接
                title = a_tag.text.strip()  # 获取标题

                # 将结果存入字典
                all_articles.append({
                    'title': title,
                    'link': full_link,
                    'date': pub_date
                })

# 保存为JSON文件
output_file = "articles.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(all_articles, f, ensure_ascii=False, indent=4)

print(f"爬取完成，数据已保存到 {output_file}")

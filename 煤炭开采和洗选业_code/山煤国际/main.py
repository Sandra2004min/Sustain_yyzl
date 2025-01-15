import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

# 定义基础URL
base_url = "https://www.smgjny.com/newslist/58-{}.html"

# 存储所有页面的结果
all_articles = []

# 遍历每一页（1到14页）
for page in range(1, 15):
    # 构造当前页的URL
    url = base_url.format(page)

    # 发送GET请求获取网页内容
    response = requests.get(url)
    response.encoding = 'utf-8'  # 根据网页编码设置

    # 检查请求是否成功
    if response.status_code == 200:
        # 使用BeautifulSoup解析HTML内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 找到<div class="bd">标签
        div_bd = soup.find('div', class_='bd')

        # 提取所有<li>标签
        li_tags = div_bd.find_all('li') if div_bd else []

        for li in li_tags:
            # 提取<a>标签中的href
            a_tag = li.find('a')
            if a_tag and 'href' in a_tag.attrs:
                relative_link = a_tag['href']
                full_link = urljoin(url, relative_link)  # 补全链接

                # 提取<h4>标签中的标题
                h4_tag = li.find('h4')
                title = h4_tag.text.strip() if h4_tag else ""

                # 提取<dt>标签中的发布时间
                dt_tag = li.find('dt')
                publish_date = dt_tag.text.strip() if dt_tag else ""

                # 保存到结果列表
                all_articles.append({
                    'link': full_link,
                    'title': title,
                    'publish_date': publish_date
                })

    else:
        print(f"第{page}页请求失败，状态码: {response.status_code}")

# 保存结果到JSON文件
with open('articles.json', 'w', encoding='utf-8') as json_file:
    json.dump(all_articles, json_file, ensure_ascii=False, indent=4)

# 打印结果
for article in all_articles:
    print(f"发布时间: {article['publish_date']}")
    print(f"标题: {article['title']}")
    print(f"链接: {article['link']}")
    print("-")

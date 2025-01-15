import requests
from bs4 import BeautifulSoup
import json
import os

# 加载之前保存的文章信息JSON文件
input_file = "shenhua_articles.json"
output_file = "shenhua_articles_with_content.json"

# 确保文件存在
if not os.path.exists(input_file):
    print(f"文件 {input_file} 不存在，请先运行爬取文章列表的代码！")
    exit()

# 读取文章列表
data = []
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 定义函数来获取文章内容
def fetch_content(url):
    try:
        response = requests.get(url)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        content_div = soup.find('div', class_='content_l_con')
        if content_div:
            return content_div.get_text(strip=True)
        else:
            return ""
    except Exception as e:
        print(f"Error fetching content from {url}: {e}")
        return ""

# 遍历每篇文章，获取内容
for article in data:
    link = article['link']
    print(f"正在获取文章内容: {link}")
    content = fetch_content(link)
    article['content'] = content

# 保存结果到新的JSON文件
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

print(f"文章内容已保存到 {output_file}")

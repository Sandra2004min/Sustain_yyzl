import requests
from bs4 import BeautifulSoup
import json

# 读取之前保存的JSON文件
input_file = "articles.json"
output_file = "article_contents.json"

# 加载文章列表
with open(input_file, 'r', encoding='utf-8') as f:
    articles = json.load(f)

# 存放每篇文章内容的列表
article_contents = []

# 遍历每篇文章的链接，提取<div class="bd">标签中的<p>内容
for article in articles:
    url = article['link']
    try:
        # 发送请求获取文章页面内容
        response = requests.get(url)
        response.encoding = 'utf-8'
        html_content = response.text

        # 解析HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # 提取<div class="bd">标签
        content_div = soup.find('div', class_='bd')
        if content_div:
            # 提取所有<p>标签中的文字
            paragraphs = [p.text.strip() for p in content_div.find_all('p') if p.text.strip()]

            # 将结果存储
            article_contents.append({
                'title': article['title'],
                'link': article['link'],
                'date': article['date'],
                'content': paragraphs
            })
    except Exception as e:
        print(f"无法处理文章：{article['title']} ({article['link']}) - 错误: {e}")

# 保存结果为JSON文件
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(article_contents, f, ensure_ascii=False, indent=4)

print(f"文章内容提取完成，已保存到 {output_file}")

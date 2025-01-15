import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm

# 定义输入和输出文件
input_file = 'articles.json'  # 存储文章链接的 JSON 文件
output_file = 'article_contents.json'  # 保存文章内容的 JSON 文件

# 加载文章链接
with open(input_file, 'r', encoding='utf-8') as f:
    articles = json.load(f)

# 存储所有文章内容
all_contents = []

# 遍历文章链接
for article in tqdm(articles, desc="文章内容爬取进度"):
    try:
        # 发送请求获取文章页面
        response = requests.get(article['link'], timeout=10)
        response.encoding = 'utf-8'

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找 <div id="zoomFont" class="wzy_bd">
        content_div = soup.find('div', id='zoomFont', class_='wzy_bd')

        if content_div:
            # 提取 span 和 p 标签中的文字
            spans = [span.text.strip() for span in content_div.find_all('span')]
            paragraphs = [p.text.strip() for p in content_div.find_all('p')]

            # 合并所有内容
            content = '\n'.join(spans + paragraphs)
        else:
            content = "未找到文章内容"

        # 保存文章内容
        all_contents.append({
            'title': article['title'],
            'link': article['link'],
            'date': article['date'],
            'content': content
        })

    except Exception as e:
        print(f"爬取失败: {article['link']} -> {e}")
        all_contents.append({
            'title': article['title'],
            'link': article['link'],
            'date': article['date'],
            'content': f"爬取失败: {e}"
        })

# 保存为 JSON 文件
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(all_contents, f, ensure_ascii=False, indent=4)

print(f"共爬取 {len(all_contents)} 篇文章内容，已保存到 {output_file} 文件中。")

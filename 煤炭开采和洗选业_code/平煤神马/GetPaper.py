import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

# 读取之前保存的 JSON 文件
input_file = "articles.json"
output_file = "article_contents.json"

# 加载文章数据
with open(input_file, 'r', encoding='utf-8') as f:
    articles = json.load(f)

# 存储爬取到的文章内容
article_contents = []

# 定义爬取单篇文章内容的函数
def fetch_article_content(article):
    link = article['link']
    title = article['title']
    date = article['date']
    try:
        # 请求文章链接
        response = requests.get(link, timeout=10)
        response.encoding = 'utf-8'
        html_content = response.text

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # 查找 <div class_="articleshow"> 标签
        articleshow_div = soup.find('div', class_='articleshow')
        if articleshow_div:
            content = articleshow_div.get_text(strip=True)  # 提取纯文字内容
        else:
            content = "未找到文章内容"
    except Exception as e:
        content = f"获取文章失败，错误: {e}"

    # 返回文章信息
    return {
        'title': title,
        'link': link,
        'date': date,
        'content': content
    }

# 使用多线程爬取文章内容
print("开始爬取文章内容...")
with ThreadPoolExecutor(max_workers=5) as executor:
    # 使用 tqdm 显示进度条
    results = list(tqdm(executor.map(fetch_article_content, articles), total=len(articles)))

# 保存所有文章内容到 JSON 文件
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=4)

print(f"所有文章内容已保存到 {output_file}")

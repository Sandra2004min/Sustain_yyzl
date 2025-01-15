import requests
from bs4 import BeautifulSoup
import json

def scrape_article_content(url):
    try:
        # 发送 HTTP 请求获取网页内容
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功

        # 解析网页内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 定位目标 <div>
        article_div = soup.find('div', class_='article-con', style='padding-top:20px;')

        if not article_div:
            print("未找到目标内容。")
            return None

        # 提取所有 <p> 标签的文字内容
        paragraphs = article_div.find_all('p')
        content = [p.get_text(strip=True) for p in paragraphs]

        return '\n'.join(content)

    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None

def update_articles_with_content(json_file):
    try:
        # 读取 JSON 文件
        with open(json_file, 'r', encoding='utf-8') as file:
            articles = json.load(file)

        # 遍历每篇文章，补充内容为空的文章
        for article in articles:
            if not article.get('content') and article.get('link'):
                print(f"正在补充文章内容: {article['title']}")
                content = scrape_article_content(article['link'])
                if content:
                    article['content'] = content

        # 写回更新后的 JSON 文件
        with open(json_file, 'w', encoding='utf-8') as file:
            json.dump(articles, file, ensure_ascii=False, indent=4)

        print("文章内容补充完成！")

    except FileNotFoundError:
        print(f"文件 {json_file} 未找到。")
    except json.JSONDecodeError:
        print("JSON 文件格式错误。")

# 示例使用
json_file = "articles_with_content.json"
update_articles_with_content(json_file)

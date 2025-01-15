import requests
import json
from bs4 import BeautifulSoup

# 读取之前保存的 articles.json
with open('articles.json', 'r', encoding='utf-8') as f:
    articles = json.load(f)

# 定义请求头，模拟浏览器
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 更新文章内容和发布时间
for article in articles:
    try:
        # 请求文章详情页
        response = requests.get(article['link'], headers=headers)
        response.encoding = 'utf-8'

        if response.status_code != 200:
            print(f"请求失败，状态码: {response.status_code}，链接: {article['link']}")
            continue

        # 解析 HTML 内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 提取文章内容
        content_div = soup.find('div', class_='e_box p_articles', data_ename='资讯详细描述')
        if content_div:
            # 提取所有 span 和 font 标签的文字内容并拼接
            spans = content_div.find_all(['span', 'font'])
            article['content'] = ''.join(tag.get_text(strip=True) for tag in spans)
        else:
            article['content'] = ""

        # 提取发布时间
        date_li = soup.find('div', class_='e_box p_topBox').find('li', class_='date')
        if date_li:
            article['publish_time'] = date_li.get_text(strip=True).replace('发布时间：', '')

        print(f"已更新文章: {article['title']}")

    except Exception as e:
        print(f"处理文章时出错: {article['title']}，错误: {e}")

# 保存更新后的文章信息到新的 JSON 文件
with open('updated_articles.json', 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=4)

print("所有文章信息已更新并保存到 updated_articles.json 文件。")

import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm  # 用于显示进度条

# 读取之前保存的JSON文件
input_file = "articles.json"
output_file = "article_contents.json"

# 加载文章链接信息
with open(input_file, "r", encoding="utf-8") as f:
    articles = json.load(f)

# 存储每篇文章的内容
article_contents = []

# 遍历每篇文章的链接，并显示进度条
for article in tqdm(articles, desc="Fetching Articles"):
    try:
        url = article["link"]
        title = article["title"]
        publish_date = article["publish_date"]
        
        # 发送GET请求获取文章内容
        response = requests.get(url)
        response.encoding = "utf-8"
        html_content = response.text
        
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(html_content, "html.parser")
        
        # 提取<div id="zoomFont" class="wzy_bd article">下的文字信息
        content_div = soup.find("div", id="zoomFont", class_="wzy_bd article")
        if content_div:
            # 提取<p>标签内的所有文本内容
            paragraphs = content_div.find_all("p")
            text_content = ""
            for p in paragraphs:
                # 获取<p>标签直接的文字内容
                if p.text:
                    text_content += p.get_text(strip=True) + "\n"
            
            # 添加到结果列表
            article_contents.append({
                "title": title,
                "link": url,
                "publish_date": publish_date,
                "content": text_content.strip()
            })
        else:
            print(f"无法找到内容区域: {url}")
    except Exception as e:
        print(f"获取文章失败: {article['link']}, 错误: {e}")

# 将文章内容保存到JSON文件
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(article_contents, f, ensure_ascii=False, indent=4)

print(f"文章内容已保存到 {output_file}")

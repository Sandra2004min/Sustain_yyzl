import requests
from bs4 import BeautifulSoup
import json
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# 输入文件名
input_file = "D:/大工学习资料/ym大三资料整理/供应链方向/新闻/demo/大屯能源/articles.json"
# 输出文件名
output_file = "article_contents.json"

# 模拟浏览器请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

def fetch_article_content(article):
    url = article["link"]
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            # 找到指定的 <div id="zoomFont" class="wzy_bd article">
            content_div = soup.find("div", id="zoomFont", class_="wzy_bd article")
            if content_div:
                return {
                    "title": article["title"],
                    "link": article["link"],
                    "publish_date": article["publish_date"],
                    "content": content_div.get_text(strip=True)
                }
            else:
                print(f"未找到文章内容: {url}")
                return {
                    "title": article["title"],
                    "link": article["link"],
                    "publish_date": article["publish_date"],
                    "content": ""
                }
        else:
            print(f"请求失败，状态码: {response.status_code}, URL: {url}")
            return {
                "title": article["title"],
                "link": article["link"],
                "publish_date": article["publish_date"],
                "content": ""
            }
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}, URL: {url}")
        return {
            "title": article["title"],
            "link": article["link"],
            "publish_date": article["publish_date"],
            "content": ""
        }

# 主函数
if __name__ == "__main__":
    # 读取文章链接文件
    with open(input_file, "r", encoding="utf-8") as f:
        articles = json.load(f)

    article_contents = []

    # 使用多线程爬取
    max_threads = 10  # 设置最大线程数
    with ThreadPoolExecutor(max_threads) as executor:
        futures = {executor.submit(fetch_article_content, article): article for article in articles}

        # 使用 tqdm 显示进度条
        for future in tqdm(as_completed(futures), total=len(futures), desc="爬取进度"):
            try:
                result = future.result()
                article_contents.append(result)
            except Exception as e:
                print(f"处理文章时发生错误: {e}")

    # 保存结果为 JSON 文件
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(article_contents, f, ensure_ascii=False, indent=4)

    print(f"爬取完成，共保存 {len(article_contents)} 篇文章内容，结果已保存到 {output_file}")

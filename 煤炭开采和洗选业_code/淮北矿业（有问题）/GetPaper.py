import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import time

# 从 articles.json 文件中读取文章链接
def load_article_links(file_name="articles_fixed.json"):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            articles = json.load(f)
        return articles
    except FileNotFoundError:
        print(f"File {file_name} not found.")
        return []

# 获取文章内容
def fetch_article_content(link):
    for attempt in range(10):  # 最多重试三次
        try:
            response = requests.get(link, timeout=10)
            response.encoding = 'utf-8'

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                content_div = soup.find('div', class_='v_news_content')
                if content_div:
                    return content_div.get_text(strip=True)
                else:
                    print(f"Content not found for link: {link}")
                    return ""
            elif response.status_code == 502:
                print(f"502 Bad Gateway for {link}. Retrying ({attempt + 1}/10)...")
                time.sleep(5)  # 等待5秒后重试
            else:
                print(f"Failed to retrieve the article: {link}. Status code: {response.status_code}")
                return ""
        except Exception as e:
            print(f"Request failed for {link}: {e}")
            time.sleep(5)  # 等待5秒后重试

    return ""  # 如果三次尝试都失败，返回空字符串

# 主程序
if __name__ == "__main__":
    articles = load_article_links()

    if articles:
        # 使用多线程和进度条来优化
        with ThreadPoolExecutor(max_workers=1) as executor:
            results = list(tqdm(executor.map(lambda article: {
                **article,
                "content": fetch_article_content(article.get("link"))
            }, articles), total=len(articles), desc="Fetching article content"))

        # 保存更新后的文章信息
        with open("articles_with_content.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=4)

        print("Content fetching complete. Data saved to articles_with_content.json.")

"""
Fetching article content: 100%|██████████████████████████████████| 11140/11140 [1:23:05<00:00,  2.23it/s]
Traceback (most recent call last):
  File "d:\大工学习资料\ym大三资料整理\供应链方向\新闻\demo\淮北矿业\GetPaper.py", line 59, in <module>   
    json.dump(results, f, ensure_ascii=False, indent=4)
  File "D:\app\python\Lib\json\__init__.py", line 180, in dump
    fp.write(chunk)
UnicodeEncodeError: 'utf-8' codec can't encode characters in position 1-2: surrogates not allowed
PS D:\大工学习资料\ym大三资料整理\供应链方向\新闻\demo> & D:/app/python/python.exe d:/大工学习资料/ym大三
资料整理/供应链方向/新闻/demo/淮北矿业/articlesFix.py
JSON 文件格式错误: Expecting value: line 9444 column 20 (char 1318496)
No data to process.
"""
import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import time

# 基础URL和初始页面
base_url = "http://www.hbcoal.com/xwdt/"
home_url = "http://www.hbcoal.com/xwdt.htm"
base_article_url = "http://www.hbcoal.com"

# 爬取单个页面的文章信息
def scrape_page(url):
    for attempt in range(3):  # 尝试最多三次
        try:
            response = requests.get(url, timeout=10)
            response.encoding = 'utf-8'  # 根据网页的编码设置

            articles = []

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                page_div = soup.find('div', class_='page')

                if page_div:
                    for tr in page_div.find_all('tr', height="35"):
                        try:
                            a_tag = tr.find('a', class_='c195417')
                            if a_tag:
                                relative_link = a_tag['href']
                                full_link = base_article_url + relative_link[2:]  # 补全链接
                                title = a_tag.text.strip()

                                time_tag = tr.find('span', class_='timestyle195417')
                                publish_time = time_tag.text.strip() if time_tag else ""

                                articles.append({
                                    'title': title,
                                    'link': full_link,
                                    'publish_time': publish_time
                                })
                        except Exception as e:
                            print(f"Error parsing an article: {e}")
                return articles
            else:
                print(f"Failed to retrieve the page: {url}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Request failed for {url}: {e}")
            time.sleep(2)  # 等待2秒后重试

    return []  # 如果三次都失败，返回空列表

# 爬取多个页面的文章信息
def scrape_all_pages():
    all_articles = []

    # 准备所有要爬取的URL
    urls = [home_url] + [f"{base_url}{page_num}.htm" for page_num in range(1, 1114)]

    # 使用多线程爬取
    with ThreadPoolExecutor(max_workers=3) as executor:
        # 使用tqdm显示进度条
        results = list(tqdm(executor.map(scrape_page, urls), total=len(urls), desc="Scraping pages"))

    # 合并结果
    for result in results:
        all_articles.extend(result)

    return all_articles

# 主程序
if __name__ == "__main__":
    articles = scrape_all_pages()

    # 保存为JSON文件
    with open("articles.json", "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)

    print("Scraping complete. Data saved to articles.json.")

# 这个代码有一些问题，跑出来的第一页的文章链接是错误的格式：http://www.hbcoal.comfo
# 因此编写了LinkFix.py文件对链接进行修正，最终得到了articles_fixed.json文件
# 最后将articles_fixed.json文件放入GetPaper.py进行爬取

import requests
from bs4 import BeautifulSoup
import json

# 单独爬取 http://www.hbcoal.com/xwdt.htm 的文章信息
def scrape_home_page():
    url = "http://www.hbcoal.com/xwdt.htm"
    base_article_url = "http://www.hbcoal.com"

    try:
        response = requests.get(url, timeout=10)
        response.encoding = 'utf-8'

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
        else:
            print(f"Failed to retrieve the page: {url}. Status code: {response.status_code}")

        return articles
    except Exception as e:
        print(f"Request failed for {url}: {e}")
        return []

# 将新数据追加到 articles.json 文件中
def append_to_json_file(new_data, file_name="articles.json"):
    try:
        # 读取现有数据
        with open(file_name, "r", encoding="utf-8") as f:
            existing_data = json.load(f)
    except FileNotFoundError:
        existing_data = []

    # 合并数据
    existing_data.extend(new_data)

    # 保存回文件
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    print("Scraping the home page...")
    home_articles = scrape_home_page()

    print(f"Scraped {len(home_articles)} articles from the home page.")

    print("Appending to articles.json...")
    append_to_json_file(home_articles)

    print("Done. Home page articles added to articles.json.")

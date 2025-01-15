from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import json
import random

# 保存结果的文件名
output_file = "articles.json"

# 配置 Selenium
chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# 替换为你的 ChromeDriver 路径
service = Service(executable_path="C:/Program Files/Google/Chrome/Application/chromedriver.exe")

def scrape_page(driver, page_num):
    url = f"https://sdtny.chinacoal.com/col/col2970/index.html?uid=12177&pageNum={page_num}"
    articles = []

    try:
        driver.get(url)
        time.sleep(random.uniform(2, 4))  # 随机延迟防止被反爬

        # 找到包含文章的 div
        div_tag = driver.find_element(By.CLASS_NAME, "lmy_right_b")
        li_tags = div_tag.find_elements(By.TAG_NAME, "li")

        for li in li_tags:
            try:
                a_tag = li.find_element(By.TAG_NAME, "a")
                span_tag = li.find_element(By.TAG_NAME, "span")

                link = a_tag.get_attribute("href")
                title = a_tag.get_attribute("title")
                publish_date = span_tag.text.strip()

                # 如果链接是相对路径，补全为绝对路径
                if not link.startswith("http"):
                    link = "https://sdtny.chinacoal.com" + link

                articles.append({
                    "title": title,
                    "link": link,
                    "publish_date": publish_date
                })
            except Exception as e:
                print(f"解析文章时出现错误: {e}")

    except Exception as e:
        print(f"爬取第 {page_num} 页时出错: {e}")

    return articles

def scrape_all_pages(start_page, end_page):
    driver = webdriver.Chrome(service=service, options=chrome_options)
    all_articles = []

    try:
        for page_num in range(start_page, end_page + 1):
            print(f"正在爬取第 {page_num} 页...")
            articles = scrape_page(driver, page_num)
            all_articles.extend(articles)
            time.sleep(random.uniform(1, 3))  # 每页爬取后随机延迟
    finally:
        driver.quit()

    return all_articles

# 主函数
if __name__ == "__main__":
    start_page = 1
    end_page = 47

    # 爬取所有页面
    all_articles = scrape_all_pages(start_page, end_page)

    # 保存为 JSON 文件
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=4)

    print(f"爬取完成，共保存 {len(all_articles)} 篇文章，结果已保存到 {output_file}")

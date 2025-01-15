from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import json
from tqdm import tqdm

# 设置 Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # 无头模式
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

service = Service('C:/Program Files/Google/Chrome/Application/chromedriver.exe')  # 替换为你的 chromedriver 路径
driver = webdriver.Chrome(service=service, options=chrome_options)

# 定义目标网页 URL
base_url = "https://www.chinacoal.com"
base_page_url = "https://www.chinacoal.com/col/col31/index.html?uid=19791&pageNum={}"  # 占位符页码

# 存储所有文章信息
all_articles = []

# 遍历第 1 到第 336 页
for page_num in tqdm(range(1, 337), desc="爬取进度"):
    page_url = base_page_url.format(page_num)

    # 打开目标网页
    driver.get(page_url)
    time.sleep(3)  # 等待页面加载完成

    # 获取动态加载后的页面源代码
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    # 找到存放文章信息的 <div class="lmy_tylb">
    articles_div = soup.find('div', class_='lmy_tylb')

    # 如果找到了对应的 div
    if articles_div:
        # 找到所有的 <li> 标签
        articles = articles_div.find_all('li')

        # 遍历每个 <li> 标签
        for article in articles:
            # 提取 <a> 标签中的链接和标题
            a_tag = article.find('a')
            if a_tag:
                href = a_tag['href']
                title = a_tag.text.strip()

                # 补全链接
                full_url = base_url + href

                # 提取 <span> 标签中的发布时间
                span_tag = article.find('span')
                date = span_tag.text.strip() if span_tag else None

                # 将信息添加到列表
                all_articles.append({
                    'title': title,
                    'link': full_url,
                    'date': date
                })
    else:
        print(f"第 {page_num} 页未找到文章信息的 div 标签！")

# 关闭浏览器
driver.quit()

# 保存为 JSON 文件
with open('articles.json', 'w', encoding='utf-8') as f:
    json.dump(all_articles, f, ensure_ascii=False, indent=4)

print(f"共爬取 {len(all_articles)} 篇文章，已保存到 articles.json 文件中。")
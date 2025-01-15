import requests
from bs4 import BeautifulSoup
import json

def extract_and_save_data(url, output_file):
    # 请求网页内容
    response = requests.get(url, verify=False)
    response.encoding = 'utf-8'
    response.raise_for_status()  # 如果请求失败，会抛出异常
    
    # 使用 BeautifulSoup 解析网页
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('div', class_='environment_item vx_news')
    
    # 用来保存提取的文章数据
    article_data = []
    
    # 假设每篇文章是一个 <article> 标签，标题在 <h2> 标签，链接在 <a> 标签，发布时间在 <time> 标签中
    for article in articles:
        link = article.find('a')['href']
        title = article.find('h3').get_text()
        date = article.find('span').get_text()
        
        # 保存为字典
        article_data.append({
            "title": title,
            "url": link,
            "publish_time": date
        })
    
    # 保存为 JSON 文件
    with open(output_file, "w", encoding="utf-8") as json_file:
        json.dump(article_data, json_file, ensure_ascii=False, indent=4)
    
    print(f"数据已保存到 {output_file} 文件中")

# 调用函数进行数据提取并保存
url = "https://dyny.hnecgc.com.cn/xwdt2/"  # 替换为你需要抓取的实际 URL
output_file = "articles.json"  # 保存的文件名
extract_and_save_data(url, output_file)

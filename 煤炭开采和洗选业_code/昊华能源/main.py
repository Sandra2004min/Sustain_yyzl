import requests
from bs4 import BeautifulSoup
import json

# 定义基础 API 地址
base_url = "https://www.bjhhny.com/comp/portalResNews/list.do"

# 定义请求头，模拟浏览器
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 定义查询参数
params = {
    'compId': 'portalResNews_list-15793360180659466',
    'cid': '11',
    'pageSize': '10',  # 每页显示的文章数量
    'currentPage': 1   # 当前页码，从1开始
}

# 用于存储所有结果
all_results = []

# 遍历页面，抓取第1到第8页的数据
for page in range(1, 9):
    params['currentPage'] = page
    response = requests.get(base_url, headers=headers, params=params)
    response.encoding = 'utf-8'

    # 检查响应状态码
    if response.status_code != 200:
        print(f"请求失败，状态码: {response.status_code}")
        break

    # 解析 HTML 内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到存放文章信息的标签
    articles_div = soup.find('div', class_='p_news')
    if not articles_div:
        print("未找到包含文章信息的标签。")
        break

    # 提取文章信息
    articles = articles_div.find_all('div', class_='newList')
    if not articles:
        print("未找到更多文章。")
        break

    for article in articles:
        # 提取发布时间
        time_span = article.find('div', class_='leftTime').find('span', class_='newTime')
        publish_time = time_span.text.strip() if time_span else ""

        # 提取标题
        title_tag = article.find('h3', class_='newTitle').find('a', class_='newTitleLink')
        title = title_tag.text.strip() if title_tag else ""

        # 提取链接，并补全 URL
        href = title_tag['href'] if title_tag and 'href' in title_tag.attrs else ""
        full_link = f"https://www.bjhhny.com{href}" if href else ""

        # 存储结果
        all_results.append({
            'publish_time': publish_time,
            'title': title,
            'link': full_link
        })

    # 打印当前页结果
    print(f"已抓取第 {page} 页的信息。")

# 保存为 JSON 文件
with open('articles.json', 'w', encoding='utf-8') as f:
    json.dump(all_results, f, ensure_ascii=False, indent=4)

print("所有结果已保存为 articles.json 文件。")
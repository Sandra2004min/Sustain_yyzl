import requests
from bs4 import BeautifulSoup

# 要爬取的网页地址
url = "http://www.hbcoal.com/xwdt/1090.htm"
base_url = "http://www.hbcoal.com"

# 发起HTTP请求
response = requests.get(url)
response.encoding = 'utf-8'  # 根据网页的编码设置

# 检查请求是否成功
if response.status_code == 200:
    # 使用BeautifulSoup解析HTML内容
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到存放文章信息的<div>标签
    page_div = soup.find('div', class_='page')

    # 存储结果的列表
    articles = []

    # 遍历所有文章的<tr>标签
    for tr in page_div.find_all('tr', height="35"):
        try:
            # 获取文章链接和标题
            a_tag = tr.find('a', class_='c195417')
            if a_tag:
                relative_link = a_tag['href']
                full_link = base_url + relative_link[2:]  # 补全链接
                title = a_tag.text.strip()

            # 获取发布时间
            time_tag = tr.find('span', class_='timestyle195417')
            publish_time = time_tag.text.strip() if time_tag else ""

            # 将信息保存到字典中
            articles.append({
                'title': title,
                'link': full_link,
                'publish_time': publish_time
            })
        except Exception as e:
            print(f"Error parsing an article: {e}")

    # 打印所有爬取到的文章信息
    for article in articles:
        print(f"标题: {article['title']}")
        print(f"链接: {article['link']}")
        print(f"发布时间: {article['publish_time']}\n")

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")
import requests
from bs4 import BeautifulSoup
import json

# 定义基础 URL 和总页数
base_url = "http://www.zgpmsm.com.cn"
page_url_template = "http://www.zgpmsm.com.cn/newsinformation/291/{}.html"
total_pages = 283  # 总页数

# 存储所有文章信息
all_articles = []

# 遍历所有页码
for page in range(1, total_pages + 1):
    # 构造当前页的 URL
    page_url = page_url_template.format(page)
    
    # 发送 GET 请求并获取网页内容
    response = requests.get(page_url)
    response.encoding = 'utf-8'  # 设置编码格式
    html_content = response.text

    # 使用 BeautifulSoup 解析 HTML 内容
    soup = BeautifulSoup(html_content, 'html.parser')

    # 查找包含文章列表的主区域
    frame_list_right = soup.find('div', class_='frame_list_right')
    if frame_list_right:
        # 遍历所有文章的容器
        articles_info = frame_list_right.find_all('div', class_='frame_list_wenz')
        
        for article_info in articles_info:
            # 提取日期部分
            date_div = article_info.find('div', class_='date')
            if date_div:
                day = date_div.find('h1').text.strip()  # 日期
                year_month = date_div.find('li').text.strip()  # 年份和月份
                date = f"{year_month}-{day}"  # 格式化为 YYYY-MM-DD
                
                # 提取文章标题和链接
                title_tag = article_info.find('div', class_='box_body_news').find('h1').find('a')
                if title_tag:
                    title = title_tag.text.strip()  # 文章标题
                    relative_link = title_tag['href']  # 相对链接
                    full_link = base_url + relative_link  # 补全完整链接
                    
                    # 将提取的信息存储到字典中
                    all_articles.append({
                        'title': title,
                        'link': full_link,
                        'date': date
                    })

    print(f"第 {page} 页处理完成...")  # 打印当前页码处理进度

# 保存为 JSON 文件
output_file = "articles.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(all_articles, f, ensure_ascii=False, indent=4)

print(f"所有文章信息已保存到 {output_file}")

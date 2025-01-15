import requests
import json

# API 的基本URL
base_url = "https://lnenergy.com.cn/api/contactData/type?type=1&pageSize=8&pageNum={}"

# 存储所有文章的信息
article_data = []

# 请求的页面数量（总共三页）
total_pages = 3

# 模拟请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# 遍历所有页面
for page_num in range(1, total_pages + 1):
    # 构造完整的API请求URL
    url = base_url.format(page_num)
    
    # 发送请求
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()  # 假设返回的是 JSON 格式的数据
        
        # 提取每篇文章的数据
        for article in data.get("data", []):
            title = article.get("title", "标题缺失")
            content = article.get("content", "内容缺失")
            date = article.get("pubTime", "时间缺失")
            
            # 存储数据
            article_data.append({
                "标题": title,
                "内容": content,
                "发布时间": date
            })
    else:
        print(f"请求失败：{url}, 状态码：{response.status_code}")
        break

# 打印获取的文章数据
for article in article_data:
    print("标题:", article['标题'])
    print("内容:", article['内容'])
    print("发布时间:", article['发布时间'])
    print("-" * 40)

# 将数据保存到 JSON 文件
output_file = 'articles.json'
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(article_data, f, ensure_ascii=False, indent=4)

print(f"数据已保存到 {output_file} 文件")

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import json

# 定义目标接口URL
base_url = "https://xinji.chinacoal.com"
api_url = "/module/web/jpage/dataproxy.jsp"
params = {
    "page": 1,  # 当前页码
    "webid": 41,
    "path": "/",
    "columnid": 3699,
    "unitid": 17823,
    "webname": "中煤新集能源股份有限公司",
    "permissiontype": 0,
}

# 发送请求获取数据
response = requests.get(urljoin(base_url, api_url), params=params)
response.encoding = "utf-8"  # 根据编码设置
html_content = response.text

# 使用BeautifulSoup解析HTML
soup = BeautifulSoup(html_content, "html.parser")

# 查找数据存储位置
articles = []
records = soup.find_all("record")
for record in records:
    # 使用CDATA解析内容
    record_data = BeautifulSoup(record.text, "html.parser")
    a_tag = record_data.find("a")
    if a_tag:
        href = a_tag.get("href")
        title = a_tag.get("title")
        full_link = urljoin(base_url, href)
    span_tag = record_data.find("span")
    if span_tag:
        publish_date = span_tag.text.strip()

    articles.append({
        "title": title,
        "link": full_link,
        "publish_date": publish_date,
    })

# 保存结果到JSON文件
output_file = "articles.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(articles, f, ensure_ascii=False, indent=4)

# 打印结果
print(f"数据已保存到 {output_file}")

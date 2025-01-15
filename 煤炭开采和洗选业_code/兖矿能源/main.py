import requests
import json

# 请求头设置，模拟浏览器访问
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
}

# 爬取多页内容
def scrape_pages(start_page, end_page):
    articles = []  # 存放所有页面的文章信息

    for page in range(start_page, end_page + 1):
        url = f"https://app.litenews.cn/v1/app/article/common/json?page={page}&cateid=77913&_orgid_=309&cqcallback=jQuery36006277440827284333_1734745674541&_={1734745674543 + page}"
        print(f"Scraping page {page}: {url}")

        # 发送请求并获取网页内容
        response = requests.get(url, headers=headers)
        response_text = response.text

        # 提取 JSON 数据
        try:
            json_start = response_text.index('({') + 1
            json_end = response_text.rindex('})') + 1
            json_data = json.loads(response_text[json_start:json_end])

            # 提取文章信息
            infos = json_data.get('data', {}).get('infos', [])
            for info in infos:
                articles.append({
                    'title': info.get('title', ''),
                    'url': info.get('url', ''),
                    'publish_at': info.get('publish_at', ''),
                })

        except Exception as e:
            print(f"Error parsing JSON on page {page}: {e}")

    return articles

# 设置起始和结束页码
start_page = 1
end_page = 269

# 爬取数据
all_articles = scrape_pages(start_page, end_page)

# 保存数据到 JSON 文件
with open('articles.json', 'w', encoding='utf-8') as f:
    json.dump(all_articles, f, ensure_ascii=False, indent=4)

print(f"Scraping completed. {len(all_articles)} articles saved to 'articles.json'.")

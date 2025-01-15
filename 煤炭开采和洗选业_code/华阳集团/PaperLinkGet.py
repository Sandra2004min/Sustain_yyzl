import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import json
from concurrent.futures import ThreadPoolExecutor
import time

# 基础 URL 和请求参数
base_url = "https://www.foryougroup.com/comp/portalResNews/list.do"
domain_url = "https://www.foryougroup.com"  # 用于补全不完整链接
params = {
    "compId": "portalResNews_list-16171901936713570",
    "cid": "2",
    "pageSize": "5",  # 每页新闻数量
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
}

# 最大页数
total_pages = 87

# 存储结果
all_results = []

# 爬取单页内容的函数
def fetch_page(page):
    params["currentPage"] = page
    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(response.text, "html.parser")
        articles = soup.find_all("div", class_="e_box p_articles borderB_default")

        # 提取每篇文章的信息
        page_results = []
        for article in articles:
            title_tag = article.find("div", class_="js_coverUrlTitle item_hide")
            title = title_tag.text.strip() if title_tag else "标题未找到"

            link_tag = article.find("a", class_="e_link")
            if link_tag:
                link = link_tag["href"].strip()
                # 判断链接是否需要补全
                if not link.startswith("http"):
                    link = f"{domain_url}{link}"
            else:
                link = "链接未找到"

            date_tag = article.find("h6", class_="color_assist")
            publish_date = date_tag.text.strip() if date_tag else "时间未找到"

            page_results.append({"标题": title, "链接": link, "发布时间": publish_date})
        return page_results

    except Exception as e:
        print(f"第 {page} 页出错: {e}")
        return []

# 使用多线程爬取
def main():
    with ThreadPoolExecutor(max_workers=10) as executor:  # 使用 10 个线程
        # 使用 tqdm 显示进度条
        pages = list(range(1, total_pages + 1))
        results = list(tqdm(executor.map(fetch_page, pages), total=total_pages, desc="爬取进度"))

        # 合并所有结果
        for page_results in results:
            all_results.extend(page_results)

# 执行爬取任务
start_time = time.time()
main()
end_time = time.time()

# 保存结果为 JSON 文件
output_file = "news_articles.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_results, f, ensure_ascii=False, indent=4)

print(f"爬取完成！共爬取 {len(all_results)} 篇文章，耗时 {end_time - start_time:.2f} 秒。")
print(f"结果已保存到 {output_file}")

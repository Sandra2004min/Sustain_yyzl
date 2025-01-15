import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import json
from concurrent.futures import ThreadPoolExecutor

# 输入和输出文件
input_file = "news_articles.json"
output_file = "article_contents_new.json"

# 请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
}

# 清理微信文章内容的函数
def clean_wechat_content(content):
    """
    清理微信文章开头到 ADAYO华阳集团\n 的内容。
    """
    marker = "ADAYO华阳集团\n"
    if marker in content:
        return content.split(marker, 1)[1]  # 删去 marker 之前的内容
    return content

# 提取文章内容的函数
def fetch_article_content(article):
    url = article["链接"]
    try:
        # 请求页面内容
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # 根据链接类型提取内容
        if url.startswith("https://mp.weixin.qq.com/"):
            # 微信文章内容
            content_div = soup.find("div", class_="rich_media_area_primary_inner")
            if content_div:
                content = [
                    span.text.strip()
                    for span in content_div.find_all("span")
                    if span.text.strip()  # 忽略空内容
                ]
                full_content = "\n".join(content)
                return clean_wechat_content(full_content)  # 清理开头内容
        elif url.startswith("https://www.foryougroup.com/"):
            # 华阳集团文章内容
            content_div = soup.find("div", class_="reset_style js-reset_style js-adapMobile")
            if content_div:
                content = [
                    p.text.strip()
                    for p in content_div.find_all("p")
                    if p.text.strip()  # 忽略空内容
                ]
                return "\n".join(content)
        return "未找到内容"
    except Exception as e:
        print(f"处理文章 {url} 时出错: {e}")
        return "获取内容失败"

# 多线程处理文章
def process_articles(articles):
    results = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        # 使用 tqdm 显示进度条
        futures = {executor.submit(fetch_article_content, article): article for article in articles}
        for future in tqdm(futures, total=len(articles), desc="提取文章内容"):
            article = futures[future]
            try:
                content = future.result()
                results.append({
                    "标题": article["标题"],
                    "链接": article["链接"],
                    "发布时间": article["发布时间"],
                    "内容": content,
                })
            except Exception as e:
                print(f"文章处理失败: {e}")
    return results

# 主函数
def main():
    # 读取 JSON 文件
    with open(input_file, "r", encoding="utf-8") as f:
        articles = json.load(f)

    print(f"共加载了 {len(articles)} 篇文章")

    # 使用多线程提取文章内容
    article_contents = process_articles(articles)

    # 保存结果为 JSON 文件
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(article_contents, f, ensure_ascii=False, indent=4)

    print(f"所有文章内容已保存到 {output_file}")

# 执行主函数
if __name__ == "__main__":
    main()

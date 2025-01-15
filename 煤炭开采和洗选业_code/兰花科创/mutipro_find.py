import requests
from bs4 import BeautifulSoup
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm  # 进度条库

# 基础 URL
base_url = "http://www.chinalanhua.com"
list_url_template = "http://www.chinalanhua.com/News/ListNewsMore.aspx?id=4&page={page}"

def get_links_from_list_page(url):
    """获取单页的所有新闻链接"""
    response = requests.get(url)
    response.encoding = 'utf-8'

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        span_tag = soup.find('span', id='lbListNews')
        if span_tag:
            links = []
            for a_tag in span_tag.find_all('a', href=True):
                href = a_tag['href']
                # 拼接完整的链接
                full_url = href if href.startswith("http") else f"{base_url}/{href}"
                links.append(full_url)
            return links
    return []

def get_article_content(article_url):
    """提取单篇文章内容"""
    try:
        response = requests.get(article_url, timeout=10)
        response.encoding = 'utf-8'

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            # 提取标题
            title_span = soup.find('span', id='lbTit')
            title = title_span.get_text(strip=True) if title_span else "无标题"

            # 提取文章内容
            content_span = soup.find('span', id='LbCon')
            paragraphs = []
            if content_span:
                # 检查是否有 <p> 标签
                p_tags = content_span.find_all('p')
                if p_tags:
                    for p_tag in p_tags:
                        paragraphs.append(p_tag.get_text(strip=True))
                else:
                    # 没有 <p> 标签时，直接提取内容，按 <br> 分割
                    raw_text = content_span.decode_contents()
                    paragraphs = [line.strip() for line in raw_text.split('<br>') if line.strip()]

            return {"title": title, "content": paragraphs}
    except Exception as e:
        print(f"请求错误：{e}，跳过 {article_url}")
    return None

def fetch_links_from_all_pages(start_page, end_page):
    """并发获取所有页面的新闻链接"""
    all_links = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {
            executor.submit(get_links_from_list_page, list_url_template.format(page=page)): page
            for page in range(start_page, end_page + 1)
        }
        for future in tqdm(as_completed(futures), total=end_page - start_page + 1, desc="提取新闻链接"):
            page = futures[future]
            try:
                links = future.result()
                if links:
                    all_links.extend(links)
                print(f"第 {page} 页提取完成，共 {len(links)} 个链接。")
            except Exception as e:
                print(f"第 {page} 页提取失败：{e}")
    return all_links

def fetch_articles_from_links(links):
    """并发获取所有文章内容"""
    all_articles = []
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = {
            executor.submit(get_article_content, link): link
            for link in links
        }
        for future in tqdm(as_completed(futures), total=len(links), desc="提取文章内容"):
            link = futures[future]
            try:
                article = future.result()
                if article:
                    all_articles.append(article)
            except Exception as e:
                print(f"文章提取失败：{e}，跳过 {link}")
    return all_articles

def main():
    # 获取所有新闻链接
    print("开始提取所有新闻链接...")
    news_links = fetch_links_from_all_pages(1, 273)
    print(f"所有新闻链接提取完成，共 {len(news_links)} 个链接。")

    # 提取每篇文章的内容
    print("开始提取所有文章内容...")
    all_articles = fetch_articles_from_links(news_links)

    # 保存到 JSON 文件
    with open("all_articles.json", "w", encoding="utf-8") as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=4)

    print("所有文章已保存到 all_articles.json 文件中。")

if __name__ == "__main__":
    main()


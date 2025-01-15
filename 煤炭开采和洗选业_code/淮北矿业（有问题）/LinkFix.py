import json

# 正确的基础 URL
BASE_URL = "http://www.hbcoal.com/info"

# 加载 articles.json 文件
def load_articles(file_name="articles.json"):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File {file_name} not found.")
        return []
    except json.JSONDecodeError as e:
        print(f"JSON 文件格式错误: {e}")
        return []

# 检查并修复链接
def fix_link(link):
    if not link.startswith(BASE_URL):
        # 修正错误的域名拼写或路径
        corrected_link = link.replace("http://www.hbcoal.comfo", BASE_URL)
        print(f"修正链接: {link} -> {corrected_link}")
        return corrected_link
    return link

# 遍历并修复 articles.json 中的链接
def fix_articles_links(input_file="articles.json", output_file="articles_fixed.json"):
    articles = load_articles(input_file)

    if not articles:
        print("No articles found to process.")
        return

    for article in articles:
        link = article.get("link")
        if link:
            article["link"] = fix_link(link)

    # 保存修复后的数据
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=4)

    print(f"Links fixed and saved to {output_file}.")

if __name__ == "__main__":
    fix_articles_links()

import json

# 加载已爬取的文章数据
input_file = "GZNYJT_Articles.json"
with open(input_file, "r", encoding="utf-8") as file:
    articles = json.load(file)

# 分离文章
no_content_articles = []
valid_content_articles = []

for article in articles:
    content = article.get("content", "").strip()
    if not content or content == "No valid content found":
        no_content_articles.append(article)
    else:
        valid_content_articles.append(article)

# 保存到两个文件
output_no_content = "No_Content_Articles.json"
output_valid_content = "Valid_Content_Articles.json"

with open(output_no_content, "w", encoding="utf-8") as file:
    json.dump(no_content_articles, file, ensure_ascii=False, indent=4)

with open(output_valid_content, "w", encoding="utf-8") as file:
    json.dump(valid_content_articles, file, ensure_ascii=False, indent=4)

print(f"分离完成！")
print(f"内容为空或无效的文章已保存到: {output_no_content}")
print(f"有效内容的文章已保存到: {output_valid_content}")

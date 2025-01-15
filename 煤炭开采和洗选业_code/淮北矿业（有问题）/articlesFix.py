import json

# 加载 JSON 文件
def load_json(file_name):
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"File {file_name} not found.")
        return []
    except json.JSONDecodeError as e:
        print(f"JSON 文件格式错误: {e}")
        return []

# 修复 Unicode 问题
def fix_unicode(input_file="articles_with_content.json", output_file="articles_with_content_fixed.json"):
    data = load_json(input_file)

    if not data:
        print("No data to process.")
        return

    # 确保所有字符串使用 UTF-8 编码
    fixed_data = []
    for item in data:
        fixed_item = {}
        for key, value in item.items():
            if isinstance(value, str):
                fixed_item[key] = value.encode("utf-8", "surrogatepass").decode("utf-8")
            else:
                fixed_item[key] = value
        fixed_data.append(fixed_item)

    # 保存修复后的数据
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(fixed_data, f, ensure_ascii=False, indent=4)

    print(f"Unicode issues fixed. Data saved to {output_file}.")

if __name__ == "__main__":
    fix_unicode()

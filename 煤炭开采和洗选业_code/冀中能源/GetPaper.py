from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from tqdm import tqdm
import json
import re
import time

# Selenium 配置
def init_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 无界面运行
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    service = Service(executable_path="C:\Program Files\Google\Chrome\Application\chromedriver.exe")  # 替换为你的 chromedriver 路径
    return webdriver.Chrome(service=service, options=chrome_options)

# 提取函数
def extract_content_with_selenium(driver, link):
    try:
        driver.get(link)
        time.sleep(2)  # 等待动态加载完成

        # 尝试查找<div class="editorlightgallery">
        try:
            content_div = driver.find_element(By.CLASS_NAME, 'editorlightgallery')
        except:
            # 如果未找到，尝试查找<div class="met-editor lazyload clearfix">
            content_div = driver.find_element(By.CLASS_NAME, 'met-editor.lazyload.clearfix')

        # 提取文本内容
        raw_text = content_div.text
        # 提取中文、标点符号和数字
        extracted_text = ''.join(re.findall(r'[\u4e00-\u9fa5，。？！、；：“”‘’（）《》——……【】0-9]', raw_text))
        return extracted_text

    except Exception as e:
        return f"获取内容时出错: {e}"

# 主程序
def main():
    input_file = 'articles.json'
    output_file = 'articles_with_content.json'

    try:
        # 读取articles.json文件
        with open(input_file, 'r', encoding='utf-8') as f:
            articles = json.load(f)

        # 初始化Selenium驱动
        driver = init_driver()

        # 使用tqdm添加进度条
        for article in tqdm(articles, desc="提取文章内容进度"):
            link = article.get('link')
            if link:
                article['content'] = extract_content_with_selenium(driver, link)
            else:
                article['content'] = "无链接"

        # 关闭浏览器
        driver.quit()

        # 将结果写入新的JSON文件
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=4)

        print(f"处理完成，结果已写入 {output_file}")

    except Exception as e:
        print(f"运行出错: {e}")

if __name__ == '__main__':
    main()

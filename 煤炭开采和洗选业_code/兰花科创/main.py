
from DrissionPage import ChromiumPage

import datetime
import csv

def get_data():
    for i in range(1):  # 下滑页面
        print(f"正在下滑第{i}次")
        driver.scroll.to_bottom()  # 滑动到页面底部

        resp = driver.listen.wait()  # 等待数据簿加载

        json_data= resp.response.body

        com = json_data["comments"]

        for i in com:
            text = i["text"]
            nickname = i["user"]["nickname"]
            create_time = i["create_time"]
            date = datetime.datetime.fromtimestamp(create_time)
            date = str(date)

            dict = {"nickname": nickname,
                    "text": text, 
                    "date": date
            }


if __name__ == "__main__":
    # 创建一个ChromiumPage对象
    driver = ChromiumPage()

    # 打开多个网页
    urls = ["https://www.douyin.com/video/7436988240130886927",
    ""]

    driver.listen.start("aweme/v1/web/comment/list/")  # 监听数据簿加载

    driver.get(urls[0])
    # get_data()
    for i in range(10):  # 下滑页面
        print(f"正在下滑第{i}次")

        button = driver.ele('.:parent-route-container route-scroll-container IhmVuo1S')
        driver.actions.scroll(500,0,button)

        resp = driver.listen.wait()  # 等待数据簿加载

        json_data= resp.response.body

        com = json_data["comments"]

        for i in com:
            text = i["text"]
            ip_add = i["ip_label"]
            nickname = i["user"]["nickname"]
            create_time = i["create_time"]
            date = datetime.datetime.fromtimestamp(create_time)
            date = str(date)

            dict = {"nickname": nickname,
                    "text": text, 
                    "date": date,
                    "ip_add": ip_add
            }
            print(dict)

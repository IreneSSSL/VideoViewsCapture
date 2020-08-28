import threading

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import requests
import pandas as pd


def play():
    # url = "";  如使用ip代理，此处为api地址，并将其他注释代码一并取消注释。如测试使用，无需代理，现在即可执行
    # result = requests.get(url)
    # print(result)
    #
    # PROXY_HOST = str(result.text).split(":")[0]
    # PROXY_PORT = str(result.text).split(":")[1]
    profile = webdriver.FirefoxProfile()
    # profile.set_preference("network.proxy.type", 1)
    # profile.set_preference("network.proxy.http", PROXY_HOST)
    # profile.set_preference("network.proxy.http_port", int(PROXY_PORT))

    # profile.set_preference('useAutomationExtension', False)
    profile.update_preferences()
    # 以下为Firefox的驱动geckodriver的地址以及Firefox的地址，请根据个人电脑配置进行更改
    driver = webdriver.Firefox(executable_path='D:\\xxx\\geckodriver.exe',
                               firefox_profile=profile,
                               firefox_binary='D:\\Program Files\\Mozilla Firefox\\firefox.exe')


    try:
        driver.get("https://d.weibo.com/231650")  # wb热搜地址
        time.sleep(5)
        driver.get("https://d.weibo.com/231650")
        hot = []
        for i in range(4):   #看前i页热搜
            time.sleep(2)
            names = driver.find_element(By.XPATH, "//*[contains(@class,\"pt_ul clearfix\")]")  # 当前页15个热搜的父元素
            sub = names.find_elements(By.XPATH, "//.[contains(@class,\"title W_autocut\")]")   # sub为一个list，包含15个热搜
            for name in sub:
                title = str(name.text).split('#')[1]   # 热搜格式是 #xxx#，因此用#号分开取第2个即为热搜本体
                hot.append(title)
            ele = driver.find_element(By.XPATH, "//*[contains(@class,\"page next S_txt1 S_line1\")]")  # 点击“下一步”看下一页
            ele.click()

        file = r'D:\\xxx\\hot.csv'   #此处为从github里一并下载的CSV文件，存在本地的地址
        data = pd.read_csv(file)
        data = pd.DataFrame(data)
        data1 = pd.DataFrame(hot)

        current = time.localtime(time.time())

        data[str(current.tm_hour) + ':' + str(current.tm_min)] = data1  # 将新列的名字设置为当前时间
        data.to_csv(file, index=False, encoding='utf_8_sig')   #结果写入CSV
    finally:
        driver.close()


while (True):
    try:
        t = threading.Thread(target=play, name="play")
        t.setDaemon(True)
        t.start()
    except:
        print()
    finally:
        time.sleep(60 * 10)  # 每10min执行一次

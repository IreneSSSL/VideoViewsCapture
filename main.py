from selenium import webdriver
import csv
import datetime
import calendar
import pandas as pd
import numpy as np


def createCSV():
    date = str(datetime.datetime.now().year) + '-' + str(datetime.datetime.now().month)
    path = "biliCount-" + date + ".csv"
    csv_head = []
    csv_head.append("id")
    csv_head.append("title")
    cal = calendar.Calendar()
    for day in cal.itermonthdates(datetime.datetime.now().year, datetime.datetime.now().month):
        day = day.strftime("%Y-%m-%d")
        csv_head.append(day)

    with open(path, 'w') as f:
        csv_write = csv.writer(f)
        csv_write.writerow(csv_head)


def addCSV(dics):
    day = datetime.datetime.now().day
    if day == 1:
        createCSV()

    date = str(datetime.datetime.now().year) + '-' + str(datetime.datetime.now().month)
    path = "biliCount-" + date + ".csv"

    data = pd.read_csv(path, encoding='utf-8')
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    backtoday = str(datetime.datetime.now().year) + '/' + str(datetime.datetime.now().month) + '/' + str(
        datetime.datetime.now().day)

    videoIdIndex = []
    for element in dics:
        if int(element['id']) not in data['id'].tolist():
            print(data)
            if data['id'].size == 0:
                data = pd.DataFrame(0, index=np.arange(1), columns=data.columns)
            else:
                data.loc[data['id'].size] = 0
            # print(data)
            data['id'][data['id'].size - 1] = element['id']
            data['title'][data['id'].size - 1] = element['title']
            videoIdIndex.append(data['id'].size - 1)
            # print(data)
        else:
            # print(element['id'])
            index = data[(data['id'].isin([element['id']]))].index.tolist()
            videoIdIndex.append(index)
    i = 0
    for dic in dics:
        id = dic['id']
        play = dic['play']
        try:
            data[today][videoIdIndex[i]] = play
        except:
            data[backtoday][videoIdIndex[i]] = play
        i = i + 1
        print(data)
    data.to_csv(path, encoding='utf_8_sig', index=False)


def start():
    # createCSV()
    driver = webdriver.Chrome(executable_path='D:\\workspace\\python\\BiliCount\\chromedriver.exe')
    driver.get("https://space.bilibili.com/390902621")

    parent = driver.find_element_by_css_selector("[class='section video']")
    sections = parent.find_elements_by_css_selector("[class='small-item fakeDanmu-item']")
    count = 8
    i = 0

    dics = []
    for i in range(8):
        id = sections[i].get_attribute("data-aid")
        play = sections[i].find_element_by_class_name("play").text
        title = sections[i].find_element_by_class_name("title").get_attribute("title")
        dic = {'id': id, 'title': title, 'play': play}
        dics.append(dic)
        print(id + " " + title + ' ' + play)
    addCSV(dics)


start()

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = 'winsert@163.com'

import requests
import time
from bs4 import BeautifulSoup
import itchat

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def getPM25(cityname):
    url = 'http://www.pm25.com/' + cityname + '.html'
    headers = {'User-Agent':"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"}
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.text, "html.parser")
    city = soup.find(class_='bi_loaction_city')  # 城市名称
    aqi = soup.find("a", {"class", "bi_aqiarea_num"})  # AQI指数
    quality = soup.select(".bi_aqiarea_right span")  # 空气质量等级
    result = soup.find("div", class_='bi_aqiarea_bottom')  # 空气质量描述
    output=city.text + u'AQI指数：' + aqi.text + u'\n空气质量：' + quality[0].text + result.text
    print output
    print time.ctime()
    return output

itchat.auto_login(enableCmdQR=2)

Help="""
友情提示：
请输入城市拼音获取天气结果，如果无法识别，自动返回首都记录
"""

itchat.send(Help,toUserName='filehelper')

@itchat.msg_register(itchat.content.TEXT)
def getcity(msg):
    if msg['ToUserName'] != 'filehelper':
        return
    print(msg['Text'])
    cityname=msg['Text']
    result=getPM25(cityname)
    #print result
    itchat.send(result,'filehelper')
    
if __name__ == '__main__':
    itchat.run()

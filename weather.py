# -*- coding: utf-8-*-

# 查询天气实况信息的模块。
import requests, lxml, os, sys
from bs4 import BeautifulSoup

# 引入Speech SDK
from aip import AipSpeech

__author__ = 'winsert@163.com'


reload(sys)
sys.setdefaultencoding('utf8')

# 用于解析URL页面:
def getSoup(url):
    soup_url = url 
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' 'Chrome/51.0.2704.63 Safari/537.36'}
    content = requests.get(soup_url, headers=headers) 
    soup = BeautifulSoup(content.text, 'lxml')
    return soup

# 获取天气实况:
def getWeather():

    try:
        weather_url = "http://jnqx.jinan.gov.cn/jnszfqxj/front/zdz/list.do?type=1"
        soup = getSoup(weather_url)
        result = soup.find('div', align="center").find_all('td')

        wlist = []
        for w in result:
            wlist.append(w.get_text())
        #print wlist[18]

        weather_msg = u'主人,当前室外温度'+str(wlist[18].strip().strip('.'))+u'摄氏度,湿度是百分之'+str(wlist[19].strip())+','+str(wlist[20].strip())+u',风速每秒'+str(wlist[21].strip())+u'米.'

        #print weather_msg
        return weather_msg

    except Exception, e:
        weather_msg = '抱歉主人，气象台的数据有问题，我查不到天气数据，请稍后再试'

def handle():

    # 定义常量
    APP_ID = "9969837"
    API_KEY = "8G8Y0VYv9yeXQIUAKvaHY51c"
    SECRET_KEY = "916d07ff585ceef514bd2be57dbd070f"

    # 初始化AipSpeech对象
    aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    text = getWeather()
    print text
    result = aipSpeech.synthesis(text, 'zh', 1, {'vol':5, 'per':0, 'pit':5, 'spd':5})
    #vol:语速，取值0-15，默认为5中语速
    #per:发音人选择, 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女
    #pit:音调，取值0-9，默认为5中语调
    #spd:语速，取值0-9，默认为5中语速

    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open('weather.mp3', 'wb') as f:
            f.write(result)

    #os.system('mpg123 weather.mp3')

if __name__ == '__main__':
    handle()

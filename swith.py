#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 用于测试yeelink开关

__author__ = 'winsert@163.com'

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

import requests
import time
import os

#apikey为用户id
apiheaders = {'U-ApiKey':'ada679ed152da2419e450917fe58ed44'}

# 开关设备swith1
apiurl = 'http://api.yeelink.net/v1.0/device/357785/sensor/406230/datapoints'
temp = 0

while True:
    r = requests.get(apiurl,headers=apiheaders)
    print r.text
    swith = r.json()

    if swith['value'] == 1:
        temp = 1
        print "minidlna is on."
        os.system('sudo service minidlna start')
    elif swith['value'] == 0 and temp == 1:
        os.system('sudo service minidlna stop')
        print "minidlna is off."
        temp = 0
    else:
        print "minidlna is off."

    time.sleep(5)

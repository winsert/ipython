#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 百度在线语音合成

__author__ = 'winsert@163.com'

import sys, os
reload(sys)
sys.setdefaultencoding("utf-8")

# 引入Speech SDK
from aip import AipSpeech

# 定义常量
APP_ID = "xxxx"
API_KEY = "xxxx"
SECRET_KEY = "xxxx"

# 初始化AipSpeech对象
aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

while 1:
    text = raw_input("您想说什么？0 => EXIT :")
    if text == '0':
        sys.exit(0)

    result = aipSpeech.synthesis(text, 'zh', 1, {'vol':5, 'per':0, 'pit':5, 'spd':5})
    #vol:语速，取值0-15，默认为5中语速
    #per:发音人选择, 0为女声，1为男声，3为情感合成-度逍遥，4为情感合成-度丫丫，默认为普通女
    #pit:音调，取值0-9，默认为5中语调
    #spd:语速，取值0-9，默认为5中语速

# 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open('auido.mp3', 'wb') as f:
            f.write(result)

    os.system('mpg123 auido.mp3')

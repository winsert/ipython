#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 向指定QQ好友送信息

__author__ = 'winsert@163.com'

import sys, time
reload(sys)
sys.setdefaultencoding("utf-8")

from qqbot import _bot as bot

tt = time.asctime(time.localtime(time.time()))
print "测试时间：", tt
print

bot.Login(['-q', '1569701115'])
bl = bot.List('buddy', 'andy_python')
if bl:
    b = bl[0]
    bot.SendTo(b, tt)

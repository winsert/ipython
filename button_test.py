#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 用于测试ReSpeaker Button

__author__ = 'winsert@163.com'

import sys, time
reload(sys)
sys.setdefaultencoding("utf-8")

count = 0

while count < 50:
    count = count + 1
    if count == 1:
        print '='*40
    elif count == 49:
        sys.exit()
    print "Count = ", count
    time.sleep(0.5)

#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = 'winsert@163.com'

import itchat

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

itchat.auto_login(enableCmdQR=2)

Help="Hello"

itchat.send(Help,toUserName='filehelper')

account = itchat.get_friends()
#print account
for user in account:
    print user
    if user['NickName'] == 'Andy':
        userName = user['UserName']
        print 'userName = ', userName
        itchat.send(Help,toUserName = userName)
        print 'Send is OK'


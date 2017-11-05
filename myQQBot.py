#! /usr/bin/env python
# -*- coding: UTF-8 -*-
# 测试QQ自动应答

__author__ = 'winsert@163.com'

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from qqbot import QQBotSlot as qqbotslot, RunBot

@qqbotslot
def onQQMessage(bot, contact, member, content, resendOn1202=True):

    print 'content:', content
    print type(content)
    print

    if content == 'hello':
        bot.SendTo(contact, '你好，我是QQ机器人')
    elif content == 'hi':
        bot.SendTo(contact, 'hi')
    elif content == '-stop':
        bot.SendTo(contact, 'QQ机器人已关闭')
        bot.Stop()

if __name__ == '__main__':
    RunBot()

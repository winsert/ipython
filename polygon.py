#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#用turtle模块画正N边形

__author__ = 'winsert@163.com'

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import turtle

def Polygon(n, head):
    turtle.st()
    turtle.goto(0,0)
    turtle.pd()
    for i in range (n):
        turtle.fd(50)
        turtle.delay(50)
        turtle.left(head)

if __name__ == '__main__':

    while 1:

        try:
            n = int(raw_input("要画正N边形？N<3 to EXIT:"))

            if n <= 2:
                sys.exit()

            else:
                head = round(360.0/n, 2)
                Polygon(n, head)
                text = str(n)+' ploygon is done. Head is: '+str(head)
                turtle.up()
                turtle.ht()
                turtle.goto(0,-15*n)
                turtle.pd()
                turtle.write(text, True, align='left')
                turtle.up()

        except Exception,e:
            print "请输入整数。"

#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#模拟鸟儿的无序飞行

__author__ = 'winsert@163.com'

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import turtle
from random import randint

boxsize = 200

b1 = turtle.Turtle()

b1.penup()

while 1:
    x = randint(1,5)
    y = randint(1,5)
    
    b1.goto(b1.xcor()+x, b1.ycor()+y)

#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 用turtle模块编写猫和老鼠游戏

__author__ = 'winsert@163.com'

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import time
import turtle

boxsize = 200
caught = False
score = 0

#老鼠前进

def up():
    mouse.forward(20)
    checkbound()

#老鼠左转
def left():
    mouse.left(45)

#老鼠右转
def right():
    mouse.right(45)

#老鼠后退
def back():
    mouse.backward(10)
    checkbound()

#结束游戏
def quitTurtle():
    window.bye()

#检测老鼠是否跑过界
def checkbound():
    global boxsize
    if mouse.xcor() > boxsize:
        mouse.goto(boxsize, mouse.ycor())
    if mouse.xcor() < -boxsize:
        mouse.goto(-boxsize, mouse.ycor())
    if mouse.ycor() > boxsize:
        mouse.goto(mouse.xcor(), boxsize)
    if mouse.ycor() < -boxsize:
        mouse.goto(mouse.xcor, -boxsize)

window=turtle.Screen()
mouse = turtle.Turtle()
cat = turtle.Turtle()
mouse.penup() #将老鼠的画笔提起，使不会出现轨迹
mouse.goto(100,100) #老鼠的初始地址坐标

window.onkey(up,"Up")  #按动方向键Up则执行函数up
window.onkey(left, 'Left')
window.onkey(right, 'Right')
window.onkey(back, 'Down')
window.onkey(quitTurtle, 'Escape')

#产生一个输入难度的对话框
#difficulty = window.numinput("难度", "请输入游戏的难度(1-5)", 2, minval=1, maxval=5)
difficulty = 0.5

#窗体监听按键
window.listen()

while not caught:
    cat.setheading(cat.towards(mouse)) #猫调整自己方向，使自己正对老鼠
    cat.forward(8+difficulty)
    score += 1
    if cat.distance(mouse) < 5: #老鼠与猫的距离少于5个像素就输了
        caught = True
    time.sleep(0.2 - (0.01*difficulty)) #难度越高，运行速度越快
window.textinput("GAME OVER", "游戏得分:"+str(score*difficulty))
print "GAME OVER"
#print  "游戏得分:"+str(score*difficulty))

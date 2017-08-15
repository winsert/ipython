#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 模拟森林火灾

__author__ = 'winsert@163.com'

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import sys, pygame
from random import *
from sys import exit
from pygame.locals import *

def Forest(position, forest): #随机生成森林
    p = position
    f = forest
    for i in range(f):
        t = randint(0, len(p)-1)
        if p[t][2] == 0:
            p[t][2] = 1
    return p

def Tree(position): #随机生成tree的座标
    p = position
    tf = 1
    while tf:
        t = randint(0, len(p)-1)
        if p[t][2] == 0:
            p[t][2] = 1
            tf = 0
    return p

def Fire(position): #随机生成fire的座标
    p = position
    f = randint(0, len(p)-1)
    p[f][3] = 1
    return p

def BigFire(position, num): #检测是否生成大火
    p = position
    n = num
    list1 = []
    list1.append(p[num])
    list2 = []
    bigfire = [] #用于保存着火座标

    while len(list1) != 0:
        list2 = list1.pop(0)
        tem = p.index(list2)

        #print 'New Fire Pot:', p[tem]
        #print 'left:', p[(tem-1)]
        #print 'right:', p[(tem+1)]
        #print 'Up:', p[(tem-100)]
        #print 'Down:', p[(tem+100)]
        #print

        if ((tem-1)%100+1) >= 0: #向左检测
            if p[(tem-1)] not in bigfire:
                if p[(tem-1)][2] == 1:
                    bigfire.append(p[(tem-1)])
                    list1.append(p[(tem-1)])
                    #print 'Left done'
                #else: print 'p[(tem-1)][2]=', p[(tem-1)][2]
            #else: print 'list2 in bigfire'
        #else: print '(tem-1) < min_cn'

        if tem != 9999 and (tem+1)%100+1 < 99: #向右检测
            if p[(tem+1)] not in bigfire:
                if p[(tem+1)][2] == 1:
                    bigfire.append(p[(tem+1)])
                    list1.append(p[(tem+1)])

        if (tem-100) >= 0 and p[(tem-100)] not in bigfire and p[(tem-100)][2] == 1: #向上检测
            bigfire.append(p[(tem-100)])
            list1.append(p[(tem-100)])

        if (tem+100) <= 9999 and p[(tem+100)] not in bigfire and p[(tem+100)][2] == 1: #向下检测
            bigfire.append(p[(tem+100)])
            list1.append(p[(tem+100)])

        #print 'bigfire:', bigfire
        #print 'list1:', list1

    return bigfire

if __name__ == '__main__': #主程序

    #pygame.init()
    #pygame.display.set_caption("Fire !")

    #screen = pygame.display.set_mode((700, 700))
    #screen.fill((255,255,255,))

    #clock = pygame.time.Clock()
    #clock.tick(30)

    width = 5 #格子宽
    height = 5 #格子高
    pos = [] #存储格子座标+属性
    fires = 0 #记录fire数量
    bigfires = 0 #记录bigfire数量
    max_bigfire = 0 #记录最大的bigfire
    times = 0 #记录循环次数
    max_trees = 0 #记录最大trees数
    min_trees = 5000 #记录最小trees数

    for row in range(1, 101): #生成单元座标+属性(默认[0,0],无tree无fire)
        for col in range(1, 101):
            position = [7*(col-1), 7*(row-1)]
            position = position + [0, 0] #[tree=0, fire=0]属性
            pos.append(position)

    forest = 5000 #森林中树木的数量
    pos = Forest(pos, forest) #生成森林

    xmin_trees = 0
    xmax_bigfire = 0
    xlist = []
    ylist = []

    #while 1:
    for x in range(5):
        for y in range(3):
            times += 1 #记录循环次数
            trees = 0 #记录tree数量
            now_bigfire = 0 #记录当前的bigfire

            pos = Tree(pos) #生成一棵tree
            pos = Fire(pos) #生成一个fire

            for p in pos:
                if p[2] == 0 and p[3] == 0: #无tree无fire空地
                    p[3] = 0 # 恢复为无火状态
                elif p[2] == 1 and p[3] == 0: #有tree无fire 空地种树
                    trees = trees + 1
                elif p[2] == 1 and p[3] == 1: #有tree有fire 树木着火
                    num = pos.index(p) #计算索引位置
                    #print 'fire point:', pos[num]
                    fires = fires + 1
                    trees = trees - 1
                    pos[num][2] = 0 #恢复为无tree状态
                    pos[num][3] = 0 #恢复为无fire状态

                    bigfire = BigFire(pos, num) #检测是否点着大火
                    #print 'bigfire = ', len(bigfire)
                    if len(bigfire) != 0:
                        #print bigfire
                        bigfires = bigfires + 1
                        now_bigfire = len(bigfire)
                        trees = trees - now_bigfire
                        if now_bigfire > max_bigfire:
                            max_bigfire = now_bigfire
                        for bgp in bigfire:
                            pn = pos.index(bgp)
                            pos[pn][2] = 0 #恢复为无tree状态
                            pos[pn][3] = 0 #恢复为无fire状态


            if trees > max_trees:
                max_trees = trees
            if trees < min_trees:
                min_trees = trees

            #print "Times:%r, Trees:%r" % (times, trees)
            #print "Max_Trees:%r, Min_trees:%r" % (max_trees, min_trees)
            #print "Max_BigFire:%r, Now_BigFire:%r, BigFires:%r" % (max_bigfire, now_bigfire, bigfires)
        xlist.append(min_trees)
        print xlist
        ylist.append(max_bigfire)
        print ylist

        print x
        aa = 0
        for a in xlist:
            aa = aa + a

        bb = 0
        for b in ylist:
            bb = bb + b
        print 'Trees:%r, BigFire:%r, Max_bigfire:%r' %(round(float(aa)/len(xlist), 3), round(float(bb)/len(ylist), 3), max(ylist))

        #print 'x=%r, xMin_trees:%r, xMax_BigFire:%r' %(x, xmin_trees, xmax_bigfire)

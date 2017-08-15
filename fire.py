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

def Park(width, height, position):
    w = width
    h = height
    p = position
    for pos in p:
        pygame.draw.rect(screen, [255, 255, 0], [pos[0], pos[1], w ,h], 0)
    
def Tree(width, height, position):
    w = width
    h = height
    p = position
    t_pos = choice(p)
    pygame.draw.rect(screen, [0, 255, 0], [t_pos[0], t_pos[1], w ,h], 0)
    return t_pos

def Fire(width, height, position):
    w = width
    h = height
    p = position
    f_pos = choice(p)
    pygame.draw.rect(screen, [255, 0, 0], [f_pos[0], f_pos[1], w ,h], 0)
    return f_pos
    

if __name__ == '__main__':

    pygame.init()
    #pygame.key.set_repeat(100, 50) #键盘延时时长
    pygame.display.set_caption("Fire !")

    width = 500
    height = 500
    screen = pygame.display.set_mode((width, height))
    screen.fill((255,255,255,))

    clock = pygame.time.Clock()
    clock.tick(25)

    pos_width = 5
    pos_height = 10
    pos = []
    tree = []

    for row in range(1, 42):
        for col in range(1, 72):
            position = [2+7*(col-1), 4+12*(row-1)]
            #print pos
            pos.append(position)

    Park(pos_width, pos_height, pos)
    #Tree(pos_width, pos_height, pos)
    pygame.display.flip()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
                
        tree.append(Tree(pos_width, pos_height, pos))
        print "Tree: %r" % int(len(tree)) 
        fire = Fire(pos_width, pos_height, pos)
        print fire
        pygame.time.delay(1000)
        pygame.display.flip()

        if fire not in tree:
            pygame.draw.rect(screen, [255, 255, 0], [fire[0], fire[1], pos_width, pos_height], 0)
        else:
            print "Fire !"*8

        #pygame.display.flip()

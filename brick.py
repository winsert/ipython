#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# 打砖块游戏

__author__ = 'winsert@163.com'

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import sys, pygame
from random import *
from sys import exit
from pygame.locals import *

class Brick(pygame.sprite.Sprite):

    def __init__(self, bric_w, bric_h, bric_pos):
        pygame.sprite.Sprite.__init__(self)
        image_surface = pygame.surface.Surface((bric_w, bric_h))
        image_surface.fill((randint(50,200), randint(50,200), randint(50,200)))
        self.image = image_surface.convert()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = bric_pos

class Paddle(pygame.sprite.Sprite):

    def __init__(self, pd_w, pd_h, pd_pos):
        pygame.sprite.Sprite.__init__(self)
        image_surface = pygame.surface.Surface((pd_w, pd_h))
        image_surface.fill((randint(0,50), randint(0,50), randint(0,50)))
        self.image = image_surface.convert()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = pd_pos

class Ball(pygame.sprite.Sprite):
    
    def __init__(self, ball_w, ball_h, location, speed):
        pygame.sprite.Sprite.__init__(self)
        image_surface = pygame.surface.Surface((ball_w, ball_h))
        image_surface.fill((255, randint(0,55), randint(0,55)))
        self.image = image_surface.convert()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.speed = speed

    def move(self, life):
        self.rect = self.rect.move(self.speed)
        if self.rect.left <= screen.get_rect().left or self.rect.right >= screen.get_rect().right:
            self.speed[0] = -self.speed[0]
        if self.rect.top <= 0: 
            self.speed[1] = -self.speed[1]
        if self.rect.bottom >= screen.get_rect().bottom:
            life = life - 1
            self.rect.left = paddle.rect.centerx
            self.rect.top = paddle.rect.centery-12
            print life
            pygame.time.delay(1000)
            return life
        newpos = self.rect.move(self.speed)
        self.rect = newpos
        return life

def animate(group, dirction, point, life):
    screen.fill((255,255,255))

    for brick in group:
        #print point
        if pygame.sprite.spritecollide(ball, group, True):
            ball.speed[0] = -ball.speed[0]
            ball.speed[1] = -ball.speed[1]
            point = point + 1
            #print point
        screen.blit(brick.image, brick.rect)
        score_text = font.render(str(point), 1, (0,0,0))

    life = ball.move(life)
    life_text = font.render(str(life), 1, (0,0,0))
    if life == 0 :
        #print point
        final_text1 = "Game Over"
        final_text2 = "Your final score is : "+str(point)
        ft1_font = pygame.font.Font(None, 70)
        ft1_surf = ft1_font.render(final_text1, 1, (0,0,0))
        screen.blit(ft1_surf, [screen.get_width()/2 - ft1_surf.get_width()/2, 300])
        ft2_font = pygame.font.Font(None, 40)
        ft2_surf = ft2_font.render(final_text2, 1, (0,0,0))
        screen.blit(ft2_surf, [screen.get_width()/2 - ft2_surf.get_width()/2, 400])
        pygame.display.flip()
        pygame.time.delay(3000)
        exit()

    if pygame.sprite.collide_rect(ball, paddle):
        ball.speed[0] = -ball.speed[0]*dirction
        ball.speed[1] = -ball.speed[1]
        
    #ball.move()
    screen.blit(ball.image, ball.rect)
    screen.blit(paddle.image, paddle.rect)
    screen.blit(score_text, score_pos)
    screen.blit(life_text, life_pos)
    pygame.display.flip()
    pygame.time.delay(15)
    return point, life

    
if __name__ == '__main__':

    pygame.init()
    pygame.key.set_repeat(100, 50) #键盘延时时长
    pygame.display.set_caption("Brick !")

    width = 400
    height = 600
    screen = pygame.display.set_mode((width, height))
    screen.fill((255,255,255,))

    clock = pygame.time.Clock()
    clock.tick(25)

    brick_width = 70
    brick_height = 20
    brick_pos = []

    group = pygame.sprite.Group()
    for row in range(1,6):
        for col in range(1, 6):
            brick_pos = [18+73*(col-1), 40+brick_height*row+3*row]
            #print brick_pos
            brick = Brick(brick_width, brick_height, brick_pos)
            group.add(brick)

    paddle_width = 80
    paddle_height = 5
    paddle_pos = [(width-paddle_width)/2, 500]
    paddle = Paddle(paddle_width, paddle_height, paddle_pos)

    ball_width = 12
    ball_height = 12
    ball_pos = [(width-ball_width)/2, 500-ball_height]
    ball_speed = [choice([-1,1]), 2]
    ball_dirction = 1
    ball = Ball(ball_width, ball_height, ball_pos, ball_speed)

    lives = 3
    points = 0
    font = pygame.font.Font(None, 50)
    score_text = font.render(str(points), 1, (0,0,0))
    score_pos = [10,10]
    life_text = font.render(str(lives), 1, (0,0,0))
    life_pos = [(screen.get_rect().right-30), 10]

    for bric in group:
        screen.blit(bric.image, bric.rect)

    screen.blit(paddle.image, paddle.rect)
    screen.blit(ball.image, ball.rect)
    screen.blit(score_text, score_pos)
    screen.blit(life_text, life_pos)
    pygame.display.flip()
    pygame.time.delay(1000)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #frame_rate = clock.get_fps()
                #print "Frame_rate = ", frame_rate
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    paddle.rect.left = paddle.rect.left-10
                    ball_dirction = -1
                    if paddle.rect.left <= 0 : paddle.rect.left=0
                elif event.key == pygame.K_RIGHT:
                    paddle.rect.right = paddle.rect.right+10
                    ball_dirction = 1
                    if paddle.rect.right >= screen.get_rect().right :
                        paddle.rect.right = screen.get_rect().right

        points, lives = animate(group, ball_dirction, points, lives)

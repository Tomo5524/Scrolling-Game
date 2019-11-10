import pygame
from pygame.locals import *
import os
import random
import sys
import math

pygame.init()

W, H = 800, 447
win = pygame.display.set_mode((W, H))
pygame.display.set_caption('Side Scroller')

bg = pygame.image.load(os.path.join('images', 'bg.png')).convert() # what does convert do?
bgx = 0
bgx2 = bg.get_width()

clock = pygame.time.Clock()


class player():
    run = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(8, 16)]
    jump = [pygame.image.load(os.path.join('images', str(x) + '.png')) for x in range(1, 8)]
    slide = [pygame.image.load(os.path.join('images', 'S1.png')), pygame.image.load(os.path.join('images', 'S2.png')),
             pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')),
             pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')),
             pygame.image.load(os.path.join('images', 'S2.png')), pygame.image.load(os.path.join('images', 'S2.png')),
             pygame.image.load(os.path.join('images', 'S3.png')), pygame.image.load(os.path.join('images', 'S4.png')),
             pygame.image.load(os.path.join('images', 'S5.png'))]

    # len(jumplist) = 109
    jumpList = [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4,
                4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1,
                -1, -1, -1, -1, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -2, -3, -3, -3, -3, -3, -3, -3, -3, -3, -3,
                -3, -3, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4, -4]

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.jumping = False
        self.sliding = False
        self.slideCount = 0
        self.jumpCount = 0
        self.runCount = 0
        self.slideUp = False

    def draw(self, win):
        if self.jumping:
            self.y -= self.jumpList[self.jumpCount] * 1.2
            win.blit(self.jump[self.jumpCount // 18], (self.x, self.y))
            self.jumpCount += 1
            if self.jumpCount > 108:
                self.jumpCount = 0
                self.jumping = False
                self.runCount = 0
            self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 10)
        elif self.sliding or self.slideUp:
            if self.slideCount < 20:
                self.y += 1
            elif self.slideCount == 80:
                self.y -= 19
                self.sliding = False
            elif self.slideCount > 20 and self.slideCount < 80: # its sliding
                self.hitbox = (self.x, self.y+3, self.width - 8, self.height - 35)
            if self.slideCount >= 110:
                self.slideCount = 0
                self.slideUp = False
                self.runCount = 0
                self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 10)
            win.blit(self.slide[self.slideCount // 10], (self.x, self.y))
            self.slideCount += 1

        else:
            if self.runCount > 42:
                self.runCount = 0
            win.blit(self.run[self.runCount // 6], (self.x, self.y))
            self.runCount += 1
            self.hitbox = (self.x + 4, self.y, self.width - 24, self.height - 13)

        pygame.draw.rect(win,(255,0,0),self.hitbox,2) # draw hitbox
        # pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0],64,self.hitbox[2],64), 2)
        # pygame.draw.rect(win, (255, 0, 0), (self.hitbox[0]+self.hitbox[2], 64, self.hitbox[2], 64), 2)

class Saw:
    image = [pygame.image.load(os.path.join('images', 'SAW0.png')),
             pygame.image.load(os.path.join('images', 'SAW1.png')),
             pygame.image.load(os.path.join('images', 'SAW2.png')),
             pygame.image.load(os.path.join('images', 'SAW3.png'))]

    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hitbox = (x,y,width,height)
        self.count = 0


    def draw(self,win):
        self.hitbox = (self.x + 10, self.y + 5, self.width - 30, self.height)
        if self.count >= 8:
            self.count = 0
        win.blit(pygame.transform.scale(self.image[self.count//2],(64,64)),(self.x,self.y))
        self.count += 1
        pygame.draw.rect(win, (255,0,0),self.hitbox,2)

    def collide(self, runner):# rect is runner, self is saw
        # runner[0] + runner[2] represents right edge of runner's hit box
        if runner[0] + runner[2] > self.hitbox[0]:# if runner overrides saw hitbox
            # runner is in between left edge(as it is inside hitbox as if statement above passed) of hit box and righ edge of hitbox
            if runner[0] < self.hitbox[0] + self.hitbox[2]: # if runner is within the right edge of saw hitbox
                if self.hitbox[1] < runner[1] + runner[3]: # check if runner's feet is below the top of saw
                    # no need to check runner's head is above saw's bottom as it is rooted into ground
                    return True

        return False



class Spike(Saw): #subclass of saw
    image = pygame.image.load(os.path.join('images', 'spike.png'))
    def draw(self,win):
        self.hitbox = (self.x + 10, self.y, 15, 315)
        if self.count >= 8:
            self.count = 0
        win.blit(self.image,(self.x,self.y))
        self.count +=1
        pygame.draw.rect(win, (255,0,0), self.hitbox,2)

    def collide(self, runner):# rect is runner, self is spike
        if runner[0] + runner[2] > self.hitbox[0] and runner[0] < self.hitbox[0] + self.hitbox[2]:
                if runner[1] < self.hitbox[3]: # if runner's head is closer to the celling
                                                # that means runner's head is overiding spike
                    return True
        return False

def redrawWindow():
    win.blit(bg,(bgx,0))
    win.blit(bg, (bgx2, 0))
    runner.draw(win)
    # spike.draw(win)
    # saw.draw(win)
    # font = pygame.font.SysFont("comicsans", 30)
    # text = font.render("Score: " + str(score),1,(255,255,255))
    # win.blit(text,(700,10))
    for obj in objects:
        obj.draw(win)
    pygame.display.update()

def endScreen(score):
    # how to go back to the game # set reset objects and other?
    # how to keep max score
    global objects, speed, max_score # this resets everything and go back to the beginning
    speed = 80 # reset speed
    objects = []
    max_score = max(max_score,score)
    run = True
    while run:
        pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

        win.blit(bg,(0,0))# reset background
        largeFont = pygame.font.SysFont("comicsans", 80)
        pre_score = largeFont.render("Max Score: " + str(max_score), 1, (255,255,255))
        win.blit(pre_score, (W//2 - pre_score.get_width()//2,200))
        largeFont = pygame.font.SysFont("comicsans", 80)
        newScore = largeFont.render("Score: " + str(score), 1, (255,255,255))
        win.blit(newScore, (W // 2 - pre_score.get_width() // 2, 320))
        pygame.display.update()


    score = 0

runner = player(200,313,64,64)
objects = []
# spike = Spike(300,0,64,64)
# saw = Saw(300,300,64,64)
pygame.time.set_timer(USEREVENT+1,500) # userevent happens every 5 seconds
pygame.time.set_timer(USEREVENT+2,random.randint(2000,3500))
speed = 80
run = True
max_score = 0
while run:

    score = (speed // 5) - 16
    for obj in objects:
        if obj.collide(runner.hitbox):
            endScreen(score)

        obj.x -= 1.4
        if obj.x < obj.width * -1:
            objects.remove(obj)

    bgx -= 1.4
    bgx2 -= 1.4
    if bgx < bg.get_width() * -1:
        bgx = bg.get_width()

    if bgx2 < bg.get_width() * -1:
        bgx2 = bg.get_width()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()


        if event.type == USEREVENT+1: # every half second,  it will be true
            speed += 1

        if event.type == USEREVENT+2:
            r = random.randint(0,2)
            if r == 0:
                objects.append(Saw(810,310,64,64))

            else:
                objects.append(Spike(810, 0, 48, 320))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        if not runner.jumping:
            runner.jumping = True

    if keys[pygame.K_DOWN]:
        if not runner.sliding:
            runner.sliding = True

    clock.tick(speed)
    redrawWindow()
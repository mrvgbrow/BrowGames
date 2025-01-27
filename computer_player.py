#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import os
import sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide' 
#os.environ['SDL_VIDEO_WINDOW_POS']="%d,%d" % (0,0)
import pygame
import ticker
import sprite_path
import time
import genutils as genu
import aifunctions as aif
import random

class ComputerPlayer:
    def __init__(self,name,sprite,movestep=None,maxdepth=200,checkstep=20,
                 decide_frames=10,random_step_frames=5,redecide_frames=30):
        self.name=name
        self.sprite=sprite
        self.decided=False
        self.movestep=movestep
        self.decide_frames=decide_frames
        self.tickers=None
        self.add_ticker('Decide',decide_frames,loop=0)
        self.add_ticker('Redecide',redecide_frames,loop=0)
        self.add_ticker('Random',random_step_frames,loop=0)
        self.maxdepth=maxdepth
        self.checkstep=checkstep
        self.path=None
        self.directions=['up','down','left','right']

    def decide_path(self,maze_surf,target):
        if not self.decided and self.tickers['Decide'].is_finished():
            maze_px=pygame.surfarray.pixels_red(maze_surf)
            time1=time.time()
            path=aif.find_path(maze_px,(self.sprite.rect.centerx,self.sprite.rect.centery),
                               (target.rect.centerx,target.rect.centery),maxsteps=self.maxdepth,
                               blockval=255,step=self.checkstep,
                               halfwidth=[round(self.sprite.rect.width/2),
                               round(self.sprite.rect.height/2)])
#            print(path)
#            print(time.time()-time1)
            if path:
                self.path=sprite_path.sprite_path(path)
                self.path_index=0
                self.decided=True
            else:
                self.tickers['Random'].finish()
                self.force_decide()

    def force_decide(self):
        self.decided=False
        self.tickers['Decide'].reset()
        self.tickers['Redecide'].reset()
        self.path=None

    def decide_direction(self):
        if self.path and self.path_index<len(self.path.path):
            direction=None
            target=self.path.path[self.path_index]
            vector_to=(target[0]-self.sprite.position.x,target[1]-self.sprite.position.y)
            if abs(vector_to[0])<self.movestep and abs(vector_to[1])<self.movestep:
                self.path_index+=1
                if self.path_index<len(self.path.path):
                    target=self.path.path[self.path_index]
                    vector_to=(target[0]-self.sprite.position.x,target[1]-self.sprite.position.y)
            if abs(vector_to[0])>abs(vector_to[1]) and vector_to[0]>0 and abs(vector_to[0])>=self.movestep:
                direction='right'
            elif abs(vector_to[0])>abs(vector_to[1]) and vector_to[0]<0 and abs(vector_to[0])>=self.movestep:
                direction='left'
            elif abs(vector_to[0])<abs(vector_to[1]) and vector_to[1]<0 and abs(vector_to[1])>=self.movestep:
                direction='up'
            elif abs(vector_to[0])<abs(vector_to[1]) and vector_to[1]>0 and abs(vector_to[1])>=self.movestep:
                direction='down'
            return direction
        else:
            self.decided=False
            if self.tickers['Random'].is_finished():
                direction=random.choice(self.directions)
                self.tickers['Random'].reset()
                return direction
            return None

    def update_tickers(self):
        if self.tickers:
            for ticker_i in self.tickers:
                self.tickers[ticker_i].update()

    def play(self,computer_keys,maze_surf,target):
        self.update_tickers()
        if self.tickers['Redecide'].is_finished():
            self.force_decide()
        self.decide_path(maze_surf,target)
        direction=self.decide_direction()
        if direction:
            computer_keys[self.name][direction]=True

    def add_ticker(self,name,count,loop=0):
        if not self.tickers:
            self.tickers={}
        self.tickers[name]=ticker.Ticker(name,count,loop=loop)

def build_keys(controllers):
    computer_keys={}
    for controller_i in controllers:
        computer_keys[controller_i.name] = {
                'up': False,
                'down': False,
                'left' : False,
                'right' : False,
        }
    return computer_keys

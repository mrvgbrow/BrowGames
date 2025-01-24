#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import pygame
import random
import math
import genutils
from . import quadrapong_gameconstants as gc


class Ball(pygame.sprite.Sprite):
    def __init__(self,ball_id):
        super(Ball,self).__init__()
        self.surf=pygame.Surface((2*gc.BALL_RADIUS,2*gc.BALL_RADIUS))
        self.surf.fill(gc.SCREEN_COLOR)
        self.surf.set_colorkey(gc.SCREEN_COLOR,gc.RLEACCEL)
        pygame.draw.circle(self.surf, gc.BALL_COLOR,(gc.BALL_RADIUS,gc.BALL_RADIUS),gc.BALL_RADIUS)
        self.mask=pygame.mask.from_surface(self.surf)
        self.speed=gc.BALL_SPEED
        self.base_speed=gc.BALL_SPEED
        self.ball_id=ball_id
        self.player_hit=-1
        angle=random.random()*math.pi*2-math.pi/4
        self.speedx,self.speedy=genutils.angle_to_coords(angle,self.speed)
        self.x=gc.SCREEN_WIDTH/2
        self.y=gc.SCREEN_HEIGHT/2
        self.rect = self.surf.get_rect(
            center=(
                self.x,
                self.y,
            )
        )

    def update(self,score):
        player_scored=None
        if self.rect.bottom <= gc.SCREEN_PAD-gc.WALL_WIDTH/2:
            score[1]-=1
            player_scored=1
            self.kill()
        elif self.rect.right < gc.SCREEN_PAD-gc.WALL_WIDTH/2:
            score[0]-=1
            player_scored=0
            self.kill()
        elif self.rect.left>gc.SCREEN_WIDTH-gc.SCREEN_PAD+gc.WALL_WIDTH/2:
            score[2]-=1
            player_scored=2
            self.kill()
        elif self.rect.top > gc.SCREEN_HEIGHT-gc.SCREEN_PAD+gc.WALL_WIDTH/2:
            score[3]-=1
            player_scored=3
            self.kill()
        self.x+=self.speedx
        self.y+=self.speedy
        self.rect.move_ip(self.x-self.rect.centerx,self.y-self.rect.centery)
        return player_scored

    def bounce_wall(self,direction):
        if direction=='left': 
            self.speedx=-abs(self.speedx)
        if direction=='right':
            self.speedx=abs(self.speedx)
        if direction=='up': 
            self.speedy=-abs(self.speedy)
        if direction=='down': 
            self.speedy=abs(self.speedy)
        pygame.mixer.music.play(loops=1)

    def anglechange(self,angle_change):
        angle_old,speed=genutils.coords_to_angle(self.speedx,self.speedy)
        angle=angle_old+angle_change
        self.speedx,self.speedy=genutils.angle_to_coords(angle,speed)

    def set_angle(self,angle_set):
        angle_old,speed=genutils.coords_to_angle(self.speedx,self.speedy)
        self.base_speed+=gc.BALL_SPEED_INCREASE
        speed=min(self.base_speed,gc.BALL_MAX_SPEED)
        self.speedx,self.speedy=genutils.angle_to_coords(angle_set,speed)

    def compute_intercept(self,position,axis):
        if axis=='x':
            intercept=genutils.find_intercept(self.speedx,self.speedy,self.rect.centerx,self.rect.centery,position)
        else:
            intercept=genutils.find_intercept(self.speedy,self.speedx,self.rect.centery,self.rect.centerx,position)
        return intercept

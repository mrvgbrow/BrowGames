#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import pygame
import random
import math
import genutils
from . import rebound_gameconstants as gc


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball,self).__init__()
        self.surf=pygame.Surface((2*gc.BALL_RADIUS,2*gc.BALL_RADIUS))
        if gc.BALL_SQUARE:
            self.surf.fill(gc.BALL_COLOR)
        else:
            self.surf.fill(gc.SCREEN_COLOR)
        self.surf.set_colorkey(gc.SCREEN_COLOR,gc.RLEACCEL)
        pygame.draw.circle(self.surf, gc.BALL_COLOR,(gc.BALL_RADIUS,gc.BALL_RADIUS),gc.BALL_RADIUS)
        self.mask=pygame.mask.from_surface(self.surf)
        self.speed=gc.BALL_SPEED
        self.acceleration=gc.GRAVITY
        angle=random.random()*math.pi/2-math.pi/4
        self.speedx,self.speedy=genutils.angle_to_coords(angle,self.speed)
        self.speedx=genutils.sign(random.random()-0.5)*self.speedx
        self.x=0.5*gc.SCREEN_WIDTH
        self.y=0.2*gc.SCREEN_HEIGHT
        self.rect = self.surf.get_rect(
            center=(
                self.x,
                self.y,
            )
        )

    def update(self):
        if self.rect.left <= 0:
            self.bounce_wall('right')
        if self.rect.right >= gc.SCREEN_WIDTH:
            self.bounce_wall('left')
        if self.rect.bottom >= gc.SCREEN_HEIGHT:
            self.kill()
        self.speedy+=self.acceleration
        self.x+=self.speedx
        self.y+=self.speedy
        self.rect.move_ip(self.x-self.rect.centerx,self.y-self.rect.centery)

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
        if abs(angle) < gc.BALL_MINANGLE_RADIANS:
            angle=genutils.sign(angle_old)*gc.BALL_MINANGLE_RADIANS
        if abs(math.pi-angle) < gc.BALL_MINANGLE_RADIANS:
            angle=math.pi-genutils.sign(math.pi-angle_old)*gc.BALL_MINANGLE_RADIANS
        if abs(-math.pi-angle) < gc.BALL_MINANGLE_RADIANS:
            angle=-math.pi-genutils.sign(math.pi-angle_old)*gc.BALL_MINANGLE_RADIANS
        speed=(2*self.acceleration*(gc.PLAYER_Y_POSITION-0.2*gc.SCREEN_HEIGHT))**0.5
        self.speedx,self.speedy=genutils.angle_to_coords(angle,speed)

    def compute_intercept(self,y_ground,acceleration):
        intercept=genutils.find_ballistic(self.speedx,self.speedy,self.rect.centerx,self.rect.centery,y_ground,self.acceleration)
        if gc.AI_CORRECT_BOUNCE:
            if intercept>gc.SCREEN_WIDTH:
                intercept=gc.SCREEN_WIDTH-(intercept-gc.SCREEN_WIDTH)
            if intercept<0:
                intercept=-intercept
        return intercept

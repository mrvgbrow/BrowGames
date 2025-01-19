#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import pygame
import random
import math
import genutils
from . import pong_gameconstants as gc


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball,self).__init__()
        self.surf=pygame.Surface((2*gc.BALL_RADIUS,2*gc.BALL_RADIUS))
        self.surf.set_colorkey(gc.SCREEN_COLOR,gc.RLEACCEL)
        if gc.BALL_SQUARE:
            self.surf.fill(gc.BALL_COLOR)
        else:
            self.surf.fill(gc.SCREEN_COLOR)
            pygame.draw.circle(self.surf, gc.BALL_COLOR,(gc.BALL_RADIUS,gc.BALL_RADIUS),gc.BALL_RADIUS)
        self.mask=pygame.mask.from_surface(self.surf)
        angle=random.random()*math.pi/2-math.pi/4+random.random()-0.5
        self.base_speed=gc.BALL_SPEED
        self.speedx,self.speedy=genutils.angle_to_coords(angle,self.base_speed)
        self.speedx=math.copysign(1,random.random()-0.5)*self.speedx # Randomize the direction of the serve
        self.anglechange(0.0)
        self.player_hit=0
        if gc.BALL_RANDOMIZE_XSTART:
            self.x=((random.random()-0.5)*0.2+0.5)*gc.SCREEN_WIDTH
        else:
            self.x=0.5*gc.SCREEN_WIDTH
#        print(self.speedx, self.speedy,angle)
        self.y=random.random()*(gc.SCREEN_HEIGHT-4*gc.WALL_WIDTH)+2*gc.WALL_WIDTH
        self.rect = self.surf.get_rect(
            center=(
                self.x,
                self.y,
            )
        )

    def update(self):
        status=0
        if self.rect.top <= gc.WALL_WIDTH:
            self.bounce_wall('down')
            status=2
        if self.rect.bottom >= gc.SCREEN_HEIGHT-gc.WALL_WIDTH:
            self.bounce_wall('up')
            status=2
        if self.rect.left >= gc.SCREEN_WIDTH:
            self.reset_speed()
            return 1
        self.x+=self.speedx
        self.y+=self.speedy
        if not gc.DISCRETE_STEPS:
            self.rect.move_ip(self.x-self.rect.centerx,self.y-self.rect.centery)
        else:
            self.rect.move_ip(self.speedx,self.speedy)
        if self.rect.right < 0:
            self.reset_speed()
            return -1
#        self.update_intercept(intercept)
        return status

    def shoot(self,target,speed,distance,direction):
        self.base_speed=speed
        direction=direction*math.pi/180
        self.speedx,self.speedy=genutils.angle_to_coords(direction,speed)
        self.x=target[0]-distance*math.cos(direction)
        self.rect.centerx=self.x
        self.y=target[1]-distance*math.sin(direction)
        self.rect.centery=self.y

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
        angle=genutils.angle_to_atan2_range(angle_old+angle_change)
        angle_mid=angle
        if abs(math.pi/2-angle) < gc.BALL_MINANGLE_DEGREES*math.pi/180.0:
            angle=math.pi/2+math.copysign(1,angle-math.pi/2)*gc.BALL_MINANGLE_DEGREES*math.pi/180.0
        if abs(-math.pi/2-angle) < gc.BALL_MINANGLE_DEGREES*math.pi/180.0:
            angle=-math.pi/2+math.copysign(1,angle+math.pi/2)*gc.BALL_MINANGLE_DEGREES*math.pi/180.0
        if math.copysign(1,math.cos(angle_old)) != math.copysign(1,math.cos(angle)):
            angle=angle_old
        self.base_speed+=gc.BALL_SPEED_INCREASE
        speed=min(self.base_speed,gc.BALL_MAX_SPEED)
#        print('before/middle/after ',angle*180/math.pi,angle_mid*180/math.pi,angle_old*180/math.pi)
        if gc.BALL_FIX_XSPEED:
            speed=speed*abs(1/math.cos(angle))
        self.speedx,self.speedy=genutils.angle_to_coords(angle,speed)

    def set_angle(self,angle_set):
        angle_old,speed=genutils.coords_to_angle(self.speedx,self.speedy)
        self.base_speed+=gc.BALL_SPEED_INCREASE
        speed=min(self.base_speed,gc.BALL_MAX_SPEED)
        if gc.BALL_FIX_XSPEED:
            speed=speed*abs(1/math.cos(angle_set))
        self.speedx,self.speedy=genutils.angle_to_coords(angle_set,speed)

    def reset_speed(self):
        self.base_speed=gc.BALL_SPEED

    def update_intercept(self,x_position):
        self.intercept=genutils.find_intercept(self.speedx,self.speedy,self.rect.centerx,self.rect.centery,x_position)
        if (self.intercept < gc.WALL_WIDTH or self.intercept > gc.SCREEN_HEIGHT-gc.WALL_WIDTH) and gc.AI_PREDICT_BOUNCE:
            intercept_x_0=genutils.find_intercept(self.speedy,self.speedx,self.rect.centery,self.rect.centerx,gc.WALL_WIDTH)
            intercept_x_1=genutils.find_intercept(self.speedy,self.speedx,self.rect.centery,self.rect.centerx,gc.SCREEN_HEIGHT-gc.WALL_WIDTH)
            if self.speedx>0:
                if intercept_x_1 > intercept_x_0:
                    self.intercept=genutils.find_intercept(self.speedx,-self.speedy,intercept_x_1,gc.SCREEN_HEIGHT-gc.WALL_WIDTH,x_position)
                else:
                    self.intercept=genutils.find_intercept(self.speedx,-self.speedy,intercept_x_0,gc.WALL_WIDTH,x_position)
            else:
                if intercept_x_1 < intercept_x_0:
                    self.intercept=genutils.find_intercept(self.speedx,-self.speedy,intercept_x_1,gc.SCREEN_HEIGHT-gc.WALL_WIDTH,x_position)
                else:
                    self.intercept=genutils.find_intercept(self.speedx,-self.speedy,intercept_x_0,gc.WALL_WIDTH,x_position)
            if self.intercept < 0 or self.intercept > gc.SCREEN_HEIGHT:
                self.intercept=-1

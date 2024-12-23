#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import pygame
import random
import math
import physics
import gameconstants as gc


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball,self).__init__()
        self.surf=pygame.Surface((2*gc.BALL_RADIUS,2*gc.BALL_RADIUS))
        self.surf.fill(gc.SCREEN_COLOR)
        self.surf.set_colorkey(gc.SCREEN_COLOR,gc.RLEACCEL)
        pygame.draw.circle(self.surf, gc.BALL_COLOR,(gc.BALL_RADIUS,gc.BALL_RADIUS),gc.BALL_RADIUS)
        self.mask=pygame.mask.from_surface(self.surf)
        angle=random.random()*math.pi/2-math.pi/4
        self.speed=gc.BALL_SPEED
        self.speedx,self.speedy=physics.angle_to_coords(angle,self.speed)
        if self.speedx<0:
            self.player_active=1
        else:
            self.player_active=2
        self.x=((random.random()-0.5)*0.2+0.5)*gc.SCREEN_WIDTH
#        self.x=0.5*gc.SCREEN_WIDTH
#        print(self.speedx, self.speedy,angle)
        self.y=random.random()*gc.SCREEN_HEIGHT
        self.rect = self.surf.get_rect(
            center=(
                self.x,
                self.y,
            )
        )

    def update(self,intercept):
        if self.rect.top <= 0:
            self.bounce_wall('down')
        if self.rect.bottom >= gc.SCREEN_HEIGHT:
            self.bounce_wall('up')
        if self.rect.right >= gc.SCREEN_WIDTH:
            self.kill()
        self.x+=self.speedx
        self.y+=self.speedy
        if not gc.DISCRETE_STEPS:
            self.rect.move_ip(self.x-self.rect.centerx,self.y-self.rect.centery)
        else:
            self.rect.move_ip(self.speedx,self.speedy)
        if self.rect.right < 0:
            self.kill()
        self.update_intercept(intercept)

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
        angle_old,speed=physics.coords_to_angle(self.speedx,self.speedy)
        angle=angle_old+angle_change
        if abs(math.pi/2-angle) < gc.BALL_MINANGLE_RADIANS:
            angle=math.pi/2+(angle_old-math.pi/2)/abs(angle_old-math.pi/2)*gc.BALL_MINANGLE_RADIANS
        if abs(-math.pi/2-angle) < gc.BALL_MINANGLE_RADIANS:
            angle=-math.pi/2+(angle_old+math.pi/2)/abs(angle_old+math.pi/2)*gc.BALL_MINANGLE_RADIANS
        self.speedx,self.speedy=physics.angle_to_coords(angle,speed)

    def update_intercept(self,x_position):
        self.intercept=physics.find_intercept(self.speedx,self.speedy,self.rect.centerx,self.rect.centery,x_position)
        if (self.intercept < 0 or self.intercept > gc.SCREEN_HEIGHT) and gc.AI_PREDICT_BOUNCE == 1:
            intercept_x_0=physics.find_intercept(self.speedy,self.speedx,self.rect.centery,self.rect.centerx,0)
            intercept_x_1=physics.find_intercept(self.speedy,self.speedx,self.rect.centery,self.rect.centerx,gc.SCREEN_HEIGHT)
            if self.player_active==2:
                if intercept_x_1 > intercept_x_0:
                    self.intercept=physics.find_intercept(self.speedx,-self.speedy,intercept_x_1,gc.SCREEN_HEIGHT,x_position)
                else:
                    self.intercept=physics.find_intercept(self.speedx,-self.speedy,intercept_x_0,0,x_position)
            else:
                if intercept_x_1 < intercept_x_0:
                    self.intercept=physics.find_intercept(self.speedx,-self.speedy,intercept_x_1,gc.SCREEN_HEIGHT,x_position)
                else:
                    self.intercept=physics.find_intercept(self.speedx,-self.speedy,intercept_x_0,0,x_position)
            if self.intercept < 0 or self.intercept > gc.SCREEN_HEIGHT:
                self.intercept=-1

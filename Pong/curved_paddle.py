#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import pygame
import random
import math
import gameconstants as gc


class CurvedPaddle(pygame.sprite.Sprite):
    def __init__(self,x_position,color):
        super(CurvedPaddle,self).__init__()
        self.surf=pygame.Surface((gc.PLAYER_RADIUS,gc.PLAYER_HEIGHT))
        self.target=-1        
        self.surf.set_colorkey(gc.SCREEN_COLOR)
        self.rect = self.surf.get_rect(
            center=(
                x_position,
                0.5*gc.SCREEN_HEIGHT,
            )
        )
        self.draw(color)

    def update(self, pressed_keys, control, target,target_speed_y):
        if control == 'player':
            if pressed_keys[gc.K_UP]:
                self.rect.move_ip(0,-gc.PLAYER_MOVESTEP)
            if pressed_keys[gc.K_DOWN]:
                self.rect.move_ip(0,gc.PLAYER_MOVESTEP)
        elif control == 'computer':
            error_distance=self.compute_error_distance(target_speed_y)
            if (abs(target-self.target)>error_distance and target>0 and target<gc.SCREEN_HEIGHT) or random.random()<gc.AI_RANDOM_ADJUST:
                self.target=target+2*(random.random()-0.5)*error_distance
            if self.target>-error_distance and self.target<gc.SCREEN_HEIGHT+error_distance:
                direction=self.target-self.rect.centery
                if abs(direction) > gc.PLAYER_MOVESTEP:
                    self.rect.move_ip(0,direction/abs(direction)*gc.PLAYER_MOVESTEP)

        if self.rect.top <= 0:
            self.rect.top=0
        if self.rect.bottom > gc.SCREEN_HEIGHT:
            self.rect.bottom=gc.SCREEN_HEIGHT

    def compute_anglechange(self,ballpos_y):
        location_on_paddle=ballpos_y-self.rect.centery
        if location_on_paddle<gc.PLAYER_RADIUS:
            nominal_change=math.asin(location_on_paddle/gc.PLAYER_RADIUS)
        else:
            nominal_change=0
        return nominal_change
    
    def draw(self,color):
        pygame.draw.circle(self.surf,color,(0,self.surf.get_height()/2),gc.PLAYER_RADIUS)
        pygame.draw.rect(self.surf,gc.SCREEN_COLOR,(0,0,self.surf.get_width()-2*gc.PLAYER_WIDTH,self.surf.get_height()))
        if self.rect.centerx>gc.SCREEN_WIDTH/2:
            self.surf=pygame.transform.flip(self.surf,True,False)
        self.mask=pygame.mask.from_surface(self.surf)

    def compute_error_distance(self,ball_speed_y):
        error_distance= gc.PLAYER_HEIGHT*gc.AI_ERROR_DISTANCE*(1+gc.AI_YSPEED_ERROR_FACTOR*abs(ball_speed_y)/gc.BALL_MAX_SPEED)
        return error_distance


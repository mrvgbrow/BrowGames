#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import pygame
import random
import math
import gameconstants as gc


class Player(pygame.sprite.Sprite):
    def __init__(self,x_position,color):
        super(Player,self).__init__()
        self.surf=pygame.Surface((gc.PLAYER_WIDTH,gc.PLAYER_HEIGHT))
        self.surf.fill(color)
        self.surf.set_colorkey(gc.SCREEN_COLOR)
        self.target=-1
        self.rect = self.surf.get_rect(
            center=(
                x_position,
                0.5*gc.SCREEN_HEIGHT,
            )
        )
        self.mask=pygame.mask.from_surface(self.surf)

    def update(self, pressed_keys, control, target):
        if control == 'arrows':
            if pressed_keys[gc.K_UP]:
                self.rect.move_ip(0,-gc.PLAYER_MOVESTEP)
            if pressed_keys[gc.K_DOWN]:
                self.rect.move_ip(0,gc.PLAYER_MOVESTEP)
        elif control == 'wasd':
            if pressed_keys[gc.K_w]:
                self.rect.move_ip(0,-gc.PLAYER_MOVESTEP)
            if pressed_keys[gc.K_s]:
                self.rect.move_ip(0,gc.PLAYER_MOVESTEP)
        elif control == 'computer':
            if abs(target-self.target)>gc.PLAYER_HEIGHT*gc.AI_ERROR_DISTANCE and target>0 and target<gc.SCREEN_HEIGHT:
                self.target=target+2*(random.random()-0.5)*gc.AI_ERROR_DISTANCE*(gc.PLAYER_HEIGHT+gc.BALL_RADIUS)
            if self.target > 0 and self.target < gc.SCREEN_HEIGHT:
                direction=self.target-self.rect.centery+gc.PLAYER_HEIGHT*gc.AI_PADDLE_SHIFT*(4.5-(self.target % 10))/10
                if abs(direction) > gc.PLAYER_MOVESTEP:
                    self.rect.move_ip(0,direction/abs(direction)*gc.PLAYER_MOVESTEP)

        if self.rect.top <= 0:
            self.rect.top=0
        if self.rect.bottom > gc.SCREEN_HEIGHT:
            self.rect.bottom=gc.SCREEN_HEIGHT

    def compute_anglechange(self,ballpos_y):
        location_on_paddle=ballpos_y-self.rect.centery
        nominal_change=location_on_paddle/gc.PLAYER_HEIGHT*math.pi
        adjusted_change=nominal_change*gc.PLAYER_CONTROL_FACTOR
        return adjusted_change

    def compute_original_angle(self,ballpos_y,speed_x):
        location_on_paddle=math.floor((ballpos_y-self.rect.centery)/gc.PLAYER_HEIGHT*8)
        if speed_x>0:
          original_angle=-math.pi/16*location_on_paddle-math.pi
        else:
          original_angle=math.pi/16*location_on_paddle
        return original_angle

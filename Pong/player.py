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

    def update(self, pressed_keys, control, target,target_speed_y):
        if control == 'arrows':
            if pressed_keys[gc.K_UP]:
                self.rect.move_ip(0,-gc.PLAYER_MOVESTEP)
            if pressed_keys[gc.K_DOWN]:
                self.rect.move_ip(0,gc.PLAYER_MOVESTEP)
            if gc.PADDLE_ALLOW_LEFTRIGHT:
                if pressed_keys[gc.K_LEFT]:
                    self.rect.move_ip(-gc.PLAYER_MOVESTEP,0)
                if pressed_keys[gc.K_RIGHT]:
                    self.rect.move_ip(gc.PLAYER_MOVESTEP,0)
        elif control == 'wasd':
            if pressed_keys[gc.K_w]:
                self.rect.move_ip(0,-gc.PLAYER_MOVESTEP)
            if pressed_keys[gc.K_s]:
                self.rect.move_ip(0,gc.PLAYER_MOVESTEP)
            if gc.PADDLE_ALLOW_LEFTRIGHT:
                if pressed_keys[gc.K_a]:
                    self.rect.move_ip(-gc.PLAYER_MOVESTEP,0)
                if pressed_keys[gc.K_d]:
                    self.rect.move_ip(gc.PLAYER_MOVESTEP,0)
        elif control == 'computer':
            error_distance=self.compute_error_distance(target_speed_y)
            if (abs(target-self.target)>error_distance and target>0 and target<gc.SCREEN_HEIGHT) or random.random()<gc.AI_RANDOM_ADJUST:
                self.target=target+2*(random.random()-0.5)*error_distance
            if self.target>-error_distance and self.target<gc.SCREEN_HEIGHT+error_distance:
                direction=self.target-self.rect.centery
                if abs(direction) > gc.PLAYER_MOVESTEP:
                    self.rect.move_ip(0,direction/abs(direction)*gc.PLAYER_MOVESTEP)

        if self.rect.top <= gc.WALL_WIDTH:
            self.rect.top=gc.WALL_WIDTH
        if self.rect.left <= gc.WALL_WIDTH:
            self.rect.left=gc.WALL_WIDTH
        if self.rect.bottom > gc.SCREEN_HEIGHT-gc.WALL_WIDTH:
            self.rect.bottom=gc.SCREEN_HEIGHT-gc.WALL_WIDTH
        if self.rect.right > gc.SCREEN_WIDTH-gc.WALL_WIDTH:
            self.rect.right=gc.SCREEN_WIDTH-gc.WALL_WIDTH

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

    def compute_error_distance(self,ball_speed_y):
        error_distance= gc.PLAYER_HEIGHT*gc.AI_ERROR_DISTANCE*(1+gc.AI_YSPEED_ERROR_FACTOR*abs(ball_speed_y)/gc.BALL_MAX_SPEED)
        return error_distance


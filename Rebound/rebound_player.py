#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import pygame
import random
import math
import controls as ctrl
import genutils
from . import rebound_gameconstants as gc


class Player(pygame.sprite.Sprite):
    def __init__(self,y_position,color,player_side,control,paddle_type):
        super(Player,self).__init__()
        real_length=min(gc.PADDLE_LENGTH,math.sqrt(gc.PADDLE_RADIUS**2-(gc.PADDLE_RADIUS-2*gc.PADDLE_WIDTH)**2)*2)
        ysize=gc.PADDLE_WIDTH if paddle_type=='normal' else gc.PADDLE_RADIUS
        xsize=gc.PADDLE_LENGTH if paddle_type=='normal' else real_length
        self.surf=pygame.Surface((xsize,ysize))
        if paddle_type=='normal': self.surf.fill(color)
        self.player_side=player_side
        self.surf.set_colorkey(gc.SCREEN_COLOR)
        self.target=-1
        self.control=control
        self.rect = self.surf.get_rect(
            center=(
                (0.25+(player_side-1)*0.5)*gc.SCREEN_WIDTH,
                y_position,
            )
        )
        if paddle_type=='curved': pf.curved_draw(self,color,gc.SCREEN_COLOR,gc.PADDLE_RADIUS,gc.PADDLE_WIDTH)
        self.mask=pygame.mask.from_surface(self.surf)

    def update(self, pressed_keys, target,mouse_relative):
        if self.control == 'Computer':
            if abs(target-self.target)>gc.PADDLE_LENGTH/8:
                self.target=target
            if self.target > 0 and self.target < gc.SCREEN_WIDTH:
                direction=self.target-self.rect.centerx+gc.PADDLE_LENGTH*gc.AI_PADDLE_SHIFT*(4.5-(self.target % 10))/10
                if abs(direction) > gc.PLAYER_MOVESTEP:
                    self.rect.move_ip(direction/abs(direction)*gc.PLAYER_MOVESTEP,0)
        elif self.control == 'Mouse':
            self.rect.move_ip(mouse_relative[1]*settings.sets['MOUSE_SENSITIVITY'],0)
        elif pressed_keys[ctrl.keycons[self.control]['right']]:
            self.rect.move_ip(gc.PLAYER_MOVESTEP,0)
        elif pressed_keys[ctrl.keycons[self.control]['left']]:
            self.rect.move_ip(-gc.PLAYER_MOVESTEP,0)

        if self.rect.left <= 0:
            self.rect.left=0
        if self.rect.right > gc.SCREEN_WIDTH:
            self.rect.right=gc.SCREEN_WIDTH
        if self.player_side==1:
            if self.rect.right>0.5*gc.SCREEN_WIDTH:
                self.rect.right=0.5*gc.SCREEN_WIDTH
        else:
            if self.rect.left<0.5*gc.SCREEN_WIDTH:
                self.rect.left=0.5*gc.SCREEN_WIDTH

    def compute_anglechange(self,ballpos_x):
        location_on_paddle=ballpos_x-self.rect.centerx
        nominal_change=genutils.sign(1-self.player_side)*location_on_paddle/gc.PADDLE_LENGTH*math.pi
        adjusted_change=nominal_change*gc.PADDLE_CONTROL_FACTOR
        return adjusted_change

    def compute_error_distance(self):
        error_distance= gc.PADDLE_LENGTH*gc.AI_ERROR_DISTANCE*(1+gc.AI_SPEED_ERROR_FACTOR*abs(self.target_ball_obj.base_speed)/gc.BALL_MAX_SPEED)
        return error_distance

    def curved_draw(self,color):
        pygame.draw.circle(self.surf,color,(self.surf.get_width()/2,0),gc.PADDLE_RADIUS)
        pygame.draw.rect(self.surf,gc.SCREEN_COLOR,(0,0,self.surf.get_width(),self.surf.get_height()-2*gc.PADDLE_WIDTH))
        self.mask=pygame.mask.from_surface(self.surf)


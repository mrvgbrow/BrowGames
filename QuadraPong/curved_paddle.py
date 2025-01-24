#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import pygame
import random
import math
import gameconstants as gc


class CurvedPaddle(pygame.sprite.Sprite):
    def __init__(self,x_position,color,player_number):
        super(CurvedPaddle,self).__init__()
        self.surf=pygame.Surface((gc.PLAYER_RADIUS,gc.PLAYER_HEIGHT))
        self.target=-1        
        self.surf.set_colorkey(gc.SCREEN_COLOR)
        self.player_number=player_number
        self.rect = self.surf.get_rect(
            center=(
                x_position,
                random.randint(0,gc.SCREEN_HEIGHT),
            )
        )
        self.draw(color)

    def update(self, pressed_keys, control, target):
        if control == 'player':
            if pressed_keys[gc.K_UP]:
                self.rect.move_ip(0,-gc.PLAYER_MOVESTEP)
            if pressed_keys[gc.K_DOWN]:
                self.rect.move_ip(0,gc.PLAYER_MOVESTEP)
        elif control == 'computer':
            if abs(target-self.target)>gc.PLAYER_HEIGHT/8:
                self.target=target
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
        nominal_change=math.asin(location_on_paddle/gc.PLAYER_RADIUS)
        return nominal_change
    
    def draw(self,color):
        pygame.draw.circle(self.surf,color,(0,self.surf.get_height()/2),gc.PLAYER_RADIUS)
        pygame.draw.rect(self.surf,gc.SCREEN_COLOR,(0,0,self.surf.get_width()-2*gc.PLAYER_WIDTH,self.surf.get_height()))
        if self.rect.centerx>gc.SCREEN_WIDTH/2:
            self.surf=pygame.transform.flip(self.surf,True,False)
        self.mask=pygame.mask.from_surface(self.surf)


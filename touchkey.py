#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import pygame
import random
import math
import gameconstants as gc


class TouchKey(pygame.sprite.Sprite):
    def __init__(self,position,characters,color=(0,0,0),size=60,place=1):        
        super(TouchKey,self).__init__()
        self.color=color
        self.change_key(characters,size=size)
        self.render_key()
        self.down=None
        self.place=place
        self.rect = self.surf.get_rect(
            center=(
                position[0],
                position[1],
            )
        )

    def render_key(self):
        self.surf.fill(self.color)
        pygame.draw.rect(self.surf,(255,255,255),(0,0,self.key_width-2,self.key_height-2),width=2,border_radius=5)
        self.surf.blit(self.label, (self.key_width/2-self.label.get_width()/2,self.key_height/2-self.label.get_height()/2))

    def update(self, pressed_buttons,mouse_pos):
        if pressed_buttons[0] and not self.down:
            if mouse_pos[0]>self.rect.left and mouse_pos[0]<self.rect.right and mouse_pos[1]>self.rect.top and mouse_pos[1]<self.rect.bottom:
                self.down=1
                self.surf.fill((255,255,255))
                return self.characters
        if not pressed_buttons[0]:
            self.down=None
        return None

    def change_key(self,characters,size=60):
        self.characters=characters
        self.key_width=int(size*len(characters)*0.8)
        self.key_height=size
        self.surf=pygame.Surface((self.key_width,self.key_height))
        self.surf.fill(self.color)
        font_text=pygame.font.Font(None,self.key_height)
        self.label=font_text.render(self.characters,True,(255,255,255))
        self.render_key()

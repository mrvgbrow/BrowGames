#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import pygame
import random
import math
import physics
import gameconstants as gc


class Wall(pygame.sprite.Sprite):
    def __init__(self,name,center_x,center_y,x_length,y_length):
        super(Wall,self).__init__()
        self.name=name
        self.surf=pygame.Surface((x_length,y_length))
        self.surf.fill(gc.WALL_COLOR)
        self.surf.set_colorkey(gc.SCREEN_COLOR,gc.RLEACCEL)
        self.mask=pygame.mask.from_surface(self.surf)
        self.rect = self.surf.get_rect(
            center=(
                center_x,
                center_y,
            )
        )


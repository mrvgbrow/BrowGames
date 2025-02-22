#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import pygame
from . import quadrapong_gameconstants as gc


class Wall(pygame.sprite.Sprite):
    def __init__(self,side,corner,center=False):
        super(Wall,self).__init__()
        if side==2 or side==4:
            self.orientation='horizontal'
            ysize=gc.WALL_WIDTH
            if center:
                xsize=gc.SCREEN_WIDTH-2*gc.SCREEN_PAD-2*gc.WALL_LENGTH
                position=[gc.SCREEN_WIDTH/2,gc.SCREEN_PAD+(side-2)/2*(gc.SCREEN_HEIGHT-2*gc.SCREEN_PAD)]
            else:
                xsize=gc.WALL_LENGTH
                position=[gc.SCREEN_PAD+gc.WALL_WIDTH/2+xsize/2+(corner-1)*(gc.SCREEN_WIDTH-2*gc.SCREEN_PAD-xsize-gc.WALL_WIDTH),gc.SCREEN_PAD+(side-2)/2*(gc.SCREEN_HEIGHT-2*gc.SCREEN_PAD)]
        else:
            self.orientation='vertical'
            xsize=gc.WALL_WIDTH
            if center:
                ysize=gc.SCREEN_HEIGHT-2*gc.SCREEN_PAD-2*gc.WALL_LENGTH
                position=[gc.SCREEN_PAD+(side-1)/2*(gc.SCREEN_WIDTH-2*gc.SCREEN_PAD),gc.SCREEN_HEIGHT/2]
            else:
                ysize=gc.WALL_LENGTH
                position=[gc.SCREEN_PAD+(side-1)/2*(gc.SCREEN_WIDTH-2*gc.SCREEN_PAD),gc.SCREEN_PAD+ysize/2+gc.WALL_WIDTH/2+(corner-1)*(gc.SCREEN_HEIGHT-2*gc.SCREEN_PAD-ysize-gc.WALL_WIDTH)]
        collision_directions=['right','down','left','up']
        self.collision_direction=collision_directions[side-1]
        self.surf=pygame.Surface((xsize,ysize))
        self.surf.fill(gc.WALL_COLOR)
        self.surf.set_colorkey(gc.SCREEN_COLOR,gc.RLEACCEL)
        self.mask=pygame.mask.from_surface(self.surf)
        self.rect = self.surf.get_rect(
            center=(
                position[0],
                position[1],
            )
        )


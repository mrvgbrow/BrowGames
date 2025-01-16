#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import pygame
import spacerace_gameconstants as gc


class Timer(pygame.sprite.Sprite):
    def __init__(self,position,dimensions,duration,orientation='left',color=(255,255,255)):
        super(Timer,self).__init__()
        self.dimensions=dimensions
        self.orientation=orientation
        if orientation=='down' or orientation=='right':
            self.anchor_position=(position[0]+dimensions[0],position[1]+dimensions[1])
        self.surf=pygame.Surface((dimensions[0],dimensions[1]))
        self.surf.fill(color)
        self.duration=duration
        self.position=position
        self.time_left=duration
        self.paused=True
        self.rect = self.surf.get_rect(
            center=(
                position[0]+dimensions[0]/2,
                position[1]+dimensions[1]/2,
            )
        )        

    def reset(self):
        self.time_left=duration

    def stop(self):
        self.paused=True

    def start(self):
        self.paused=False

    def update(self):
        if not self.paused and self.time_left>0:
            self.time_left-=1
        if self.orientation=='left':
            self.surf=pygame.transform.scale(self.surf,(self.dimensions[0]*self.time_left/self.duration,self.dimensions[1]))
        elif self.orientation=='up':
            self.surf=pygame.transform.scale(self.surf,(self.dimensions[0],self.dimensions[1]*self.time_left/self.duration))
        elif self.orientation=='down':
            self.surf=pygame.transform.scale(self.surf,(self.dimensions[0],self.dimensions[1]*self.time_left/self.duration))
            self.rect.centery=self.position[1]+self.dimensions[1]/2+self.dimensions[1]*(1-self.time_left/self.duration)
        elif self.orientation=='right':
            self.surf=pygame.transform.scale(self.surf,(self.dimensions[0]*self.time_left/self.duration,self.dimensions[1]))
            self.rect.centerx=self.position[0]+self.dimensions[0]/2+self.dimensions[0]*(1-self.time_left/self.duration)

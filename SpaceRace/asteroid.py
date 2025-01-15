#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import pygame
import random
import math
import physics
import gameobject as go
import gameconstants as gc


class Asteroid(go.GameObject):
    def __init__(self,sprite_name,position,color=None,scale=None,velocity=None,boundary=None):
        super(Asteroid,self).__init__(sprite_name,position,color=color,scale=scale,velocity=velocity,boundary=boundary)
        self.init_position=position
        self.init_velocity=velocity

    def kill(self,fullkill=False):
        if fullkill:
            super(Asteroid,self).kill()
        else:
            self.reset()

    def reset(self):
        random_offset=random.random()*100
        if self.init_velocity[0]>0:
            self.position.x=self.boundary.left-random_offset
        else:
            self.position.x=self.boundary.right+random_offset
        self.position.y=self.init_position[1]
        self.velocity.x=self.init_velocity[0]+(random.random()-0.5)*gc.gc['ASTEROID_SPEED_SPREAD']
        self.velocity.y=self.init_velocity[1]


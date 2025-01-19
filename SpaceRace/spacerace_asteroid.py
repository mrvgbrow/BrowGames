#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import random
import math
import gameobject as go
from . import spacerace_gameconstants as gc


class Asteroid(go.GameObject):
    def __init__(self,sprite_name,position,color=None,scale=None,velocity=None,boundary=None,image_path=''):
        super(Asteroid,self).__init__(sprite_name,position,color=color,scale=scale,velocity=velocity,boundary=boundary,image_path=image_path)
        self.init_position=position
        self.init_velocity=velocity
        self.id=random.randint(1,30000)

    def kill(self,fullkill=False):
        if fullkill:
            super(Asteroid,self).kill()
        else:
            self.reset()

    def reset(self):
        start_offset=0.0
        if self.init_velocity[0]>0:
            self.position.x=self.boundary.left-start_offset
        else:
            self.position.x=self.boundary.right+start_offset
        self.position.y=self.init_position[1]
        self.velocity.x=self.init_velocity[0]+(random.random()-0.5)*gc.gc['ASTEROID_SPEED_SPREAD']
        self.velocity.y=self.init_velocity[1]


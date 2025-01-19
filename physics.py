#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import math
import pygame

class Particle():
    def __init__(self,position,angle=None,speed=None,velocity=[0,0]):
        self.position=pygame.math.Vector2(position)
        self.angle=angle
        self.speed=speed
        if angle and speed:
            velocity=[speed*math.sin(angle),speed*math.cos(angle)]
        self.velocity=pygame.math.Vector2(velocity)

    def update_motion(self,impulse=None,thrust=None):
        if thrust:
            self.speed+=thrust
            self.velocity.x=self.speed*math.sin(angle)
            self.velocity.y=self.speed*math.cos(angle)
        if impulse:
            self.velocity.x+=self.impulse[0]
            self.velocity.y+=self.impulse[1]

    def update_position(self,step=None):
        self.position.x+=self.velocity.x
        self.position.y+=self.velocity.y
        if step:
            self.position.x+=step[0]
            self.position.y+=step[1]

    def update(self,impulse=None,thrust=None,step=None):
        self.update_motion(impulse=impulse,thrust=thrust)
        self.update_position(step=step)

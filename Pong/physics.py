#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import math


def angle_to_coords(angle,amplitude):
    return amplitude*math.cos(angle),amplitude*math.sin(angle)

def angle_to_atan2_range(angle):
    return math.atan2(math.sin(angle),math.cos(angle))

def coords_to_angle(coordx,coordy):
    return math.atan2(coordy,coordx),(coordx*coordx+coordy*coordy)**0.5

def find_intercept(speedx,speedy,x,y,x0):
    return y+(x0-x)*speedy/speedx

def sign(value):
    if value<0:
        return -1
    else:
        return 1

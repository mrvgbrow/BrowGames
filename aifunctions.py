#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import os
import sys
import math
import numpy as np
import spritefunctions as sf
import pygame
import genutils as genu
from collections import deque

def check_steps(sprite_move,sprites_avoid,movestep,nsteps=1):
    prect=[sprite_move.rect.left,sprite_move.rect.right,sprite_move.rect.top,sprite_move.rect.bottom]
    for sprite_avoid in sprites_avoid:
        for step in range(nsteps):
            erect=sprite_avoid.rect
            if erect.left+step*sprite_avoid.velocity.x<=prect[1]+step*movestep[0] and erect.right+step*sprite_avoid.velocity.x>=prect[0]+step*movestep[0] and erect.top<=prect[3]+step*movestep[1] and erect.bottom>=prect[2]+step*movestep[1]:
                return sprite_avoid
    return None

def decide_move(sprite_move,sprites_avoid,movestep,nsteps=1,color_avoid=False):
    if color_avoid:
        for sprite_avoid in sprites_avoid:
            sf.fill(sprite_avoid.surf,(255,255,255,255))
    collide_risk=check_steps(sprite_move,sprites_avoid,movestep,nsteps=nsteps)
    if collide_risk:
        if color_avoid:
            sf.fill(collide_risk.surf,(255,0,0,255))
        collide_risk2=check_steps(sprite_move,sprites_avoid,(0.0,0.0),nsteps=nsteps)
    else:
        return movestep
    if collide_risk2:
        if color_avoid:
            sf.fill(collide_risk2.surf,(255,0,0,255))
        collide_risk3=check_steps(sprite_move,sprites_avoid,(-movestep[0],-movestep[1]),nsteps=nsteps)
    else:
        return (0.0,0.0)
    if collide_risk3:
        if color_avoid:
            sf.fill(collide_risk3.surf,(255,0,0,255))
        return movestep
    else:
        return (-movestep[0],-movestep[1])

class Cell:
    def __init__(self,position,parent,nsteps):
        self.position=position
        self.parent=parent
        self.nsteps=nsteps

def find_path(grid,start,target,step=1,blockval=255,maxsteps=10000,halfwidth=None):
    if grid[start]==blockval or grid[target]==blockval:
        return None
    grid_visited=np.zeros_like(grid,dtype=bool)
    grid_visited[start]=True
    cell_check=deque()
    cell_check.append(Cell(start,None,0))

    # Determine the steps being explored from each cell
    steps=[[step,0],[-step,0],[0,step],[0,-step]]

    # Account for the size of the object moving through the maze by
    # checking the maze one halfwidth away from each cell
    if halfwidth:
        steps_hw=[[halfwidth[0],halfwidth[1]],[-halfwidth[0],halfwidth[1]],
              [halfwidth[0],-halfwidth[1]],[-halfwidth[0],-halfwidth[1]]]
    while cell_check:

        # Get the next cell in the stack
        cell_i=cell_check.popleft()
        position_i=cell_i.position
        nsteps_i=cell_i.nsteps

        # If we have reached the target, then reconstruct the path by going 
        # backwards through the cells
        if (abs(position_i[0]-target[0])<step and \
                abs(position_i[1]-target[1])<step) or nsteps_i==maxsteps:
            cell_check=cell_i
            path=[]
            while cell_check.parent:
                path.insert(0,cell_check.position)
                cell_check=cell_check.parent
            return path

        # Loop through the adjacent cells
        for idx,step_i in enumerate(steps):
            position=(position_i[0]+step_i[0],position_i[1]+step_i[1])

            # Check that the cell has not been visited and that it's within
            # the array
            if genu.check_array_coords(grid,position) and  \
                    not grid_visited[position]:

                # If accounting for the width of the object, then account for 
                # all four of its corners
                grid_check_full=True
                if halfwidth:
                    for step_hw_i in steps_hw:
                        position_edge=(position_i[0]+step_i[0]+step_hw_i[0],
                                       position_i[1]+step_hw_i[1]+step_i[1])
                        if not genu.check_array_coords(grid,position_edge) \
                                or grid[position_edge]==blockval:
                            grid_check_full=False
                            break
                else:
                    grid_check_full=not grid[position]

                if grid_check_full:
                    grid_visited[position]=True
                    cell_check.append(Cell(position,cell_i,nsteps_i+1))
    return None


#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import os
import sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide' 
#os.environ['SDL_VIDEO_WINDOW_POS']="%d,%d" % (0,0)
import pygame
import genutils as genu
import random
import gameconstants as gc
import gameobject as go

def make_full_mazes(width,height,top,thick,back_color,maze_color,nx,ny,image_path=None):
    maze=[]
    for i in range(2):
        maze.append(pygame.Surface((width-2*thick,height-2*thick)).convert_alpha())
        maze[i].set_colorkey(back_color)
    maze_rect=[]
    maze_sprites=[]
    y_scale=(height-thick*2)/ny/16*1.0
    maze_scale=round(y_scale)

    for k in range(2):
        maze_piece=go.GameObjectSimple((0,0),sprite_name='Tile'+str(k+1),scale=maze_scale,color=maze_color,image_path=image_path)
        for i in range(nx):
            for j in range(ny):
                x_position=i*maze_scale*14
                y_position=j*maze_scale*16
                maze_piece_rect=maze_piece.surf.get_rect(left=x_position,top=y_position)
                maze[k].blit(maze_piece.surf,maze_piece_rect)
        maze_rect.append(maze[k].get_rect(left=0,top=0))
        maze_mask=pygame.mask.from_surface(maze[k])
        maze_sprites.append(go.GameObjectSimple((0,0),surface=maze[k],mask=maze_mask,image_path=image_path))
        maze_sprites[k].rect=maze_rect[k]
    return maze_sprites

def make_maze_pieces(width,height,top,thick,back_color,maze_color,nx,ny):
    maze=[]
    for i in range(2):
        maze.append(pygame.Surface((width-2*thick,height-2*thick)).convert_alpha())
        maze[i].set_colorkey(back_color)
    maze_rect=[]
    maze_sprites=[]
    y_scale=(height-thick*2)/ny/16*1.0
    maze_scale=round(y_scale)

    for k in range(2):
        for i in range(nx):
            for j in range(ny):
                maze_piece=go.GameObjectSimple((0,0),sprite_name='Tile'+str(k+1),scale=maze_scale,color=maze_color)
                x_position=i*maze_scale*14
                y_position=j*maze_scale*16
                maze_piece.rect=maze_piece.surf.get_rect(left=x_position+thick,top=top+thick+y_position)
                maze_sprites.append(maze_piece)
    return maze_sprites


def make_combined_maze(maze_sprites,maze_srect,maze_line_1,maze_line_2,back_color,image_path=None):
    mazepart_sprites=[]
    boxes,maze_types=get_maze_boxes(maze_line_1,maze_line_2,maze_srect)
    mazepart=[]
    mazepart_rect=[]
    j=0
    for i in range(len(boxes)):
        if boxes[i][0] != None:
            mazepart.append(pygame.Surface((boxes[i][1]-boxes[i][0],boxes[i][3]-boxes[i][2])))
            mazepart_rect.append(mazepart[j].get_rect(left=boxes[i][0],top=boxes[i][2]))
            if maze_types[i] != -1:
                maze_sprites[maze_types[i]].rect=maze_sprites[maze_types[i]].surf.get_rect(left=0,top=-boxes[i][2]+maze_srect.top)
            mazepart[j].blit(maze_sprites[maze_types[i]].surf,maze_sprites[maze_types[i]].rect)
            mazepart[j].set_colorkey(back_color)
            mazemask=pygame.mask.from_surface(mazepart[j])
            mazepart_sprites.append(go.GameObjectSimple((0,0),surface=mazepart[j],mask=mazemask,image_path=image_path))
            mazepart_sprites[j].rect=mazepart_rect[j]
            j+=1
    return mazepart_sprites

def get_maze_boxes(maze_line_1,maze_line_2,maze_srect):
    box_y=[(None,None),(None,None),(None,None)]
    maze_bottom=maze_srect.height*0.965
    if maze_line_1<=0 or maze_line_1>=maze_bottom:
        box_y[0]=(None,None)
        box_y[1]=(0,maze_line_2)
        box_y[2]=(maze_line_2,maze_bottom)
        maze_types=[None,1,0]
    elif maze_line_2<=0 or maze_line_2>=maze_bottom:
        box_y[0]=(0,maze_line_1)
        box_y[1]=(maze_line_1,maze_bottom)
        box_y[2]=(None,None)
        maze_types=[0,1,None]
    elif maze_line_2>0 and maze_line_2<maze_bottom and maze_line_1>0 and maze_line_1<maze_bottom and maze_line_1>maze_line_2:
        box_y[0]=(maze_line_2,maze_line_1)
        box_y[1]=(maze_line_1,maze_bottom)
        box_y[2]=(0,maze_line_2)
        maze_types=[0,1,1]
    elif maze_line_2>0 and maze_line_2<maze_bottom and maze_line_1>0 and maze_line_1<maze_bottom and maze_line_1<maze_line_2:
        box_y[0]=(0,maze_line_1)
        box_y[1]=(maze_line_1,maze_line_2)
        box_y[2]=(maze_line_2,maze_bottom)
        maze_types=[0,1,0]
    boxes=[]
    for y in box_y:
        if y[0] != None:
            boxes.append([maze_srect.left,maze_srect.right,maze_srect.top+y[0],maze_srect.top+y[1]])
        else:
            boxes.append([None,None,None,None])
    return boxes,maze_types


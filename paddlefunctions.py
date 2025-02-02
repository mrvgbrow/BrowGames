#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import os
import sys
import math
import pygame
import genutils as genu

def compute_original_angle(paddle,ball,paddle_length,angles=[0,math.pi/6,math.pi/4,math.pi/3],angle_increment=math.pi/16):
    location_on_paddle=compute_paddle_location(paddle,ball,paddle_length)
    if abs(location_on_paddle)>=len(angles):location_on_paddle=math.copysign(1,location_on_paddle)*(len(angles)-1)
    if location_on_paddle<0:
        base_angle=-angles[-int(location_on_paddle)]
    else:
        base_angle=angles[int(location_on_paddle)]
    if paddle.orientation=='vertical':
        if ball.speedx>0:
          original_angle=-base_angle-math.pi
        else:
          original_angle=base_angle
    else:
        if ball.speedy<0:
          original_angle=-base_angle+math.pi/2
        else:
          original_angle=base_angle-math.pi/2
    return original_angle

def compute_paddle_location(paddle,ball,paddle_length):
    ball_coord=ball.rect.centery if paddle.orientation=='vertical' else ball.rect.centerx
    paddle_coord=paddle.rect.centery if paddle.orientation=='vertical' else paddle.rect.centerx
    location_on_paddle=math.floor((ball_coord-paddle_coord)/paddle_length*8)
    return location_on_paddle

def compute_anglechange(paddle,ball,radius=None,paddle_length=None,paddle_control_factor=None):
    if paddle.orientation=='vertical':
        location_on_paddle=ball.rect.centery-paddle.rect.centery
    else:
        location_on_paddle=ball.rect.centerx-paddle.rect.centerx
    if paddle.type=='curved':
        if location_on_paddle>radius:
            location_on_paddle=radius
        elif location_on_paddle<-radius:
            location_on_paddle=-radius
        nominal_change=2*math.asin(location_on_paddle/radius)
        if paddle.player_side==2 or paddle.player_side==3:
            nominal_change*=-1
        adjusted_change=nominal_change
    else:
        nominal_change=location_on_paddle/paddle_length*math.pi
        if paddle.player_side==2 or paddle.player_side==3:
            nominal_change*=-1
        adjusted_change=nominal_change*paddle_control_factor
    return adjusted_change

def curved_draw(paddle,color,screen_color,radius,width):
    if paddle.orientation=='vertical':
        pygame.draw.circle(paddle.surf,color,(0,paddle.surf.get_height()/2),radius)
        pygame.draw.rect(paddle.surf,screen_color,(0,0,paddle.surf.get_width()-2*width,paddle.surf.get_height()))
    else:
        pygame.draw.circle(paddle.surf,color,(paddle.surf.get_width()/2,0),radius)
        pygame.draw.rect(paddle.surf,screen_color,(0,0,paddle.surf.get_width(),paddle.surf.get_height()-2*width))
    if paddle.player_side==3:
        paddle.surf=pygame.transform.flip(paddle.surf,True,False)
    elif paddle.player_side==4:
        paddle.surf=pygame.transform.flip(paddle.surf,False,True)
    paddle.mask=pygame.mask.from_surface(paddle.surf)

def choose_target(paddle,balls,screen_height,screen_width,paddle_limit,paddle_movestep,paddle_length,ai_try_all=False):
    ball_choice=[screen_width,None,-1]
    for ball_i in balls:
        if paddle.orientation=='vertical':
            relative_position=paddle.rect.centerx-ball_i.rect.centerx
            if ball_i.speedx!=0:
                ball_distance=relative_position/ball_i.speedx
                target=ball_i.compute_intercept(paddle.rect.centerx,'x')
            else:
                ball_distance=screen_width
                target=-1000
            player_distance=abs(paddle.rect.centery-target)/paddle_movestep
        else:
            relative_position=paddle.rect.centery-ball_i.rect.centery
            if ball_i.speedy!=0:
                ball_distance=relative_position/ball_i.speedy
                target=ball_i.compute_intercept(paddle.rect.centery,'y')
            else:
                ball_distance=screen_height
                target=-1000
            player_distance=abs(paddle.rect.centerx-target)/paddle_movestep
        if ai_try_all:
            player_distance=0.0
        if player_distance<ball_distance and target>paddle_limit and target<screen_height-paddle_limit and ball_distance>0:
            if (abs(target-paddle.target)>paddle_length/8 or paddle.target==-1) and ball_distance<ball_choice[0]:
                ball_choice=[ball_distance,ball_i,target]
    if ball_choice[1]:
        paddle.target=ball_choice[2]
        paddle.target_ball=ball_choice[1].ball_id
        paddle.target_ball_obj=ball_choice[1]
        return ball_choice[1]
    else:
        return False


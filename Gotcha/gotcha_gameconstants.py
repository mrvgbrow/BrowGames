#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import pygame
import math
import re

def make_shortcuts(gmdict):
    allkeys=list(gmdict.keys())
    sdict={}
    for key in allkeys:
        shortcut_string=key[0]
        keypattern=re.findall("_([A-Z])",key)
        if keypattern:
            for match in range(len(keypattern)):
                shortcut_string+=keypattern[match]
        if shortcut_string in gmdict:
            shortcut_string+='2'
            i=2
            while shortcut_string in gmdict:
                i+=1
                shortcut_string=shortcut_string[:-1]+str(i)
        gmdict[shortcut_string]=gmdict[key]
        sdict[shortcut_string]=key
    return gmdict,sdict

def process_game_arguments(args,gmdict,sdict):
    if len(args)>0:
        for arg in args:
            varmatch=re.match("(.*)=(.*)",arg)
            if varmatch:
                key=(varmatch.group(1)).upper()
                value=varmatch.group(2)
                try:
                    value=int(value)
                except:
                    try:
                        value=float(value)
                    except:
                        value=str(value)
                        if value.lower()=='true':
                            value=True
                        elif value.lower()=='false':
                            value=False
                gmdict[key]=value
                if key in sdict:
                    gmdict[sdict[key]]=value
        return gmdict
    else:
        return None


gc={}
# General
gc['SCREEN_HEIGHT']=975
gc['SCREEN_WIDTH']=1025
gc['GAME_HEIGHT']=0.872
gc['GAME_WIDTH']=1.0
gc['FONT_SIZE']=54
gc['SCREEN_COLOR']=(0,0,0)
gc['START_COUNTDOWN']=0
gc['PANEL_COLOR']=(0,0,0,255)
gc['BORDER_THICK']=0.012

# Timing
gc['TICK_FRAMERATE']=60
gc['TIMER_DURATION']=60
gc['TIMER_POSITION_X']=0.7
gc['TIMER_POSITION_Y']=0.17
gc['TIMER_WIDTH']=0.078
gc['TIMER_LENGTH']=0.094
gc['TIMER_COLOR']=(255,255,255)
gc['TIMER_LENGTH']=0.9

# Scoring 
gc['SCORE_COLOR']=(255,255,255)
gc['SCORE_CATCH']=1
gc['WAIT_POINTSCORED']=1

# Player properties
gc['PLAYER_NUMBER']=5
gc['PLAYER_MOVESPEED']=240
gc['PLAYER_VELSTEP']=0.2
gc['PLAYER_SCALE']=2
gc['PLAYER1_START_X']=0.5
gc['PLAYER2_START_X']=0.9
gc['PLAYER3_START_X']=0.1
gc['PLAYER4_START_X']=0.1
gc['PLAYER5_START_X']=0.9
gc['PLAYER1_START_Y']=0.5
gc['PLAYER2_START_Y']=0.9
gc['PLAYER3_START_Y']=0.9
gc['PLAYER4_START_Y']=0.1
gc['PLAYER5_START_Y']=0.1
gc['PLAYER1_CONTROL']='Arrows'
gc['PLAYER2_CONTROL']='Computer1'
gc['PLAYER3_CONTROL']='Computer2'
gc['PLAYER4_CONTROL']='Computer3'
gc['PLAYER5_CONTROL']='Computer4'
gc['PLAYER_MAZE_BUMP']=0.015

# Maze properties
gc['MAZE_COLOR']=(255,255,255,255)
gc['MAZE_CHANGE_SPEED']=1
gc['NUMBER_TILES_X']=5
gc['NUMBER_TILES_Y']=3

def scale_parameters():
    global gc
    gc['GAME_WIDTH']*=int(gc['GAME_WIDTH']*gc['SCREEN_WIDTH'])
    gc['GAME_HEIGHT']=int(gc['GAME_HEIGHT']*gc['SCREEN_HEIGHT'])
    gc['TOP']=gc['SCREEN_HEIGHT']-gc['GAME_HEIGHT']
    gc['LEFT']=gc['SCREEN_WIDTH']-gc['GAME_WIDTH']
    gc['TIMER_DURATION']*=gc['TICK_FRAMERATE']
    gc['TIMER_LENGTH']*=gc['GAME_WIDTH']
    gc['TIMER_POSITION_X']*=gc['GAME_WIDTH']
    gc['TIMER_POSITION_Y']=gc['TIMER_POSITION_Y']*gc['GAME_HEIGHT']
    gc['TIMER_WIDTH']*=gc['GAME_WIDTH']
    gc['TIMER_LENGTH']*=gc['GAME_HEIGHT']
    gc['PLAYER_MOVESTEP']=int(gc['PLAYER_MOVESPEED']/gc['TICK_FRAMERATE'])
    gc['PLAYER_MAZE_BUMP']*=gc['GAME_WIDTH']
    gc['PLAYER1_START_X']=int(gc['PLAYER1_START_X']*gc['GAME_WIDTH'])
    gc['PLAYER2_START_X']=int(gc['PLAYER2_START_X']*gc['GAME_WIDTH'])
    gc['PLAYER3_START_X']=int(gc['PLAYER3_START_X']*gc['GAME_WIDTH'])
    gc['PLAYER4_START_X']=int(gc['PLAYER4_START_X']*gc['GAME_WIDTH'])
    gc['PLAYER5_START_X']=int(gc['PLAYER5_START_X']*gc['GAME_WIDTH'])
    gc['PLAYER1_START_Y']=int(gc['TOP']+gc['PLAYER1_START_Y']*gc['GAME_HEIGHT'])
    gc['PLAYER2_START_Y']=int(gc['TOP']+gc['PLAYER2_START_Y']*gc['GAME_HEIGHT'])
    gc['PLAYER3_START_Y']=int(gc['TOP']+gc['PLAYER3_START_Y']*gc['GAME_HEIGHT'])
    gc['PLAYER4_START_Y']=int(gc['TOP']+gc['PLAYER4_START_Y']*gc['GAME_HEIGHT'])
    gc['PLAYER5_START_Y']=int(gc['TOP']+gc['PLAYER5_START_Y']*gc['GAME_HEIGHT'])
    gc['BORDER_THICK']=int(gc['BORDER_THICK']*gc['SCREEN_WIDTH'])

# Import pygame.locals for easier access to key coordinates,
# Updated to conform to flake8 and black standards,
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_RETURN,
    K_RIGHTBRACKET,
    K_a,
    K_p,
    K_z,
    K_c,
    K_s,
    K_q,
    K_d,
    K_w,
    KEYDOWN,
    KEYUP,
    QUIT,
    MOUSEMOTION,
    MOUSEBUTTONDOWN,
    K_LCTRL,
    K_RCTRL,
    K_LSHIFT,
    K_RSHIFT,
)

def set_preset(preset_dict):
    global gc
    for parameter in preset_dict:
        gc[parameter]=preset_dict[parameter]

def get_parameters(parameter_list):
    global gc
    pars_dict={}
    for par in parameter_list:
       value=gc[par]
       pars_dict[par]=value
    return pars_dict

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
gc['SCREEN_HEIGHT']=1000
gc['SCREEN_WIDTH']=1446
gc['FONT_SIZE']=54
gc['SCREEN_COLOR']=(0,0,0)
gc['SOUND_VOLUME']=1.0
gc['GRAVITY']=0.1
gc['START_COUNTDOWN']=3

# Timing
gc['TICK_FRAMERATE']=60
gc['TIMER_DURATION']=60
gc['TIMER_COLOR']=(255,255,255)
gc['TIMER_WIDTH']=0.01
gc['TIMER_BOTTOM']=0.01
gc['TIMER_TOP']=0.01

# Scoring 
gc['SCORE_P1_XPOS']=0.2
gc['SCORE_YPOS']=0.9
gc['SCORE_P2_XPOS']=0.8
gc['SCORE_COLOR']=(255,255,255)

# Player properties
gc['PLAYER_SPEED']=3
gc['PLAYER_ACCELERATION']=0.2
gc['PLAYER_SCALE']=6.0
gc['PLAYER_Y_START']=0.9
gc['PLAYER1_CONTROL']='WASD'
gc['PLAYER1_X_POSITION']=0.25
gc['PLAYER2_X_POSITION']=0.75
gc['PLAYER2_CONTROL']='arrows'
gc['PLAYER1_STEPS_ANTICIPATE']=20
gc['PLAYER2_STEPS_ANTICIPATE']=20
gc['PLAYER_ANIM_PACE']=4
gc['POWERUP_TIME']=3.0
gc['PLAYER_COLLISION_RESET']=True
gc['PLAYER_ANIMATE']=False

# Asteroid properties
gc['ASTEROID_SPEED']=180
gc['ASTEROID_SPEED_SPREAD']=1.0
gc['ASTEROID_SEPARATION']=0.013
gc['ASTEROID_HORIZONTAL_IMPULSE']=0.0
gc['ASTEROID_COLOR']=(200,200,200,255)
gc['ASTEROID_SCALE']=5.0
gc['ASTEROID_OLD_TYPE']=True
gc['ASTEROID_MAX_HEIGHT']=0.03
gc['ASTEROID_REVIVE_TIME']=3.0

# Canister properties
gc['CANISTER_SPEED']=1.0
gc['CANISTER_FRACTION']=0.22
gc['CANISTER_COLOR']=(255,255,255,255)
gc['CANISTER_SCALE']=3.0

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

def scale_parameters():
    global gc
    gc['GAME_HEIGHT']=gc['SCREEN_HEIGHT']
    gc['GAME_WIDTH']=gc['SCREEN_WIDTH']
    gc['TOP']=gc['SCREEN_HEIGHT']-gc['GAME_HEIGHT']
    gc['LEFT']=gc['SCREEN_WIDTH']-gc['GAME_WIDTH']
    gc['PLAYER_Y_START']=gc['TOP']+gc['GAME_HEIGHT']*gc['PLAYER_Y_START']
    gc['PLAYER1_X_POSITION']*=gc['GAME_WIDTH']
    gc['PLAYER2_X_POSITION']*=gc['GAME_WIDTH']
    gc['TIMER_BOTTOM']*=gc['GAME_HEIGHT']
    gc['TIMER_TOP']*=gc['GAME_HEIGHT']
    gc['TIMER_POSITION']=[gc['SCREEN_WIDTH']*0.5,gc['TIMER_TOP']]
    gc['TIMER_DIMENSIONS']=[gc['TIMER_WIDTH']*gc['GAME_WIDTH'],gc['TIMER_BOTTOM']-gc['TIMER_TOP']]
    gc['TIMER_DURATION']*=gc['TICK_FRAMERATE']
    gc['SCORE_P1_XPOS']*=gc['GAME_WIDTH']
    gc['SCORE_P2_XPOS']*=gc['GAME_WIDTH']
    gc['SCORE_YPOS']*=gc['GAME_HEIGHT']
    gc['GRAVITY']/=gc['TICK_FRAMERATE']**2
    gc['PLAYER_ACCELERATION']/=gc['TICK_FRAMERATE']**2
    gc['CANISTER_SPEED']*=gc['ASTEROID_SPEED']
    gc['ASTEROID_SPEED']/=gc['TICK_FRAMERATE']
    gc['ASTEROID_SPEED_SPREAD']/=gc['TICK_FRAMERATE']
    gc['CANISTER_SPEED']/=gc['TICK_FRAMERATE']
    gc['PLAYER_SPEED']/=gc['TICK_FRAMERATE']
    gc['POWERUP_TIME']*=gc['TICK_FRAMERATE']
    gc['ASTEROID_HORIZONTAL_IMPULSE']/=gc['TICK_FRAMERATE']
    gc['ASTEROID_MAX_HEIGHT']*=gc['GAME_HEIGHT']
    gc['ASTEROID_SEPARATION']*=gc['GAME_HEIGHT']
    gc['ASTEROID_REVIVE_TIME']=int(gc['TICK_FRAMERATE']*gc['ASTEROID_REVIVE_TIME'])

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

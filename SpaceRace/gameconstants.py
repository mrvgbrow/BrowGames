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
gc['FULL_HEIGHT']=1000
gc['FULL_WIDTH']=1446
gc['SCREEN_HEIGHT']=900
gc['SCREEN_WIDTH']=1446
gc['TOP']=gc['FULL_HEIGHT']-gc['SCREEN_HEIGHT']
gc['LEFT']=gc['FULL_WIDTH']-gc['SCREEN_WIDTH']
gc['FONT_SIZE']=54
gc['SCREEN_COLOR']=(0,0,0)
gc['SOUND_VOLUME']=1
gc['GRAVITY']=0.1
gc['START_COUNTDOWN']=3

# Timing
gc['TICK_FRAMERATE']=60
gc['TIMER_DURATION']=gc['TICK_FRAMERATE']*60
gc['TIMER_POSITION']=[gc['SCREEN_WIDTH']*0.5,gc['TOP']+gc['FULL_HEIGHT']/10]
gc['TIMER_DIMENSIONS']=[15,gc['FULL_HEIGHT']-gc['TIMER_POSITION'][1]]
gc['TIMER_COLOR']=(255,255,255)
gc['TIMER_LENGTH']=gc['SCREEN_WIDTH']*0.9

# Scoring 
gc['SCORE_XPOS']=250
gc['SCORE_YPOS']=25
gc['SCORE_COLOR']=(255,255,255)
gc['SCORE_TOP']=1
gc['SCORE_CANISTER']=0

# Player properties
gc['PLAYER_MOVESTEP']=3
gc['PLAYER_VELSTEP']=0.2
gc['PLAYER_SCALE']=6
gc['PLAYER_Y_START']=gc['TOP']+gc['SCREEN_HEIGHT']*0.9
gc['PLAYER1_CONTROL']='asdw'
gc['PLAYER2_CONTROL']='arrows'
gc['PLAYER1_COLOR']=(255,255,255,255)
gc['PLAYER2_COLOR']=(255,255,255,255)
gc['PLAYER1_STEPS_ANTICIPATE']=20
gc['PLAYER2_STEPS_ANTICIPATE']=20
gc['PLAYER_ANIM_PACE']=4
gc['POWER_STEPS']=180

# Asteroid properties
gc['ASTEROID_SPEED']=3
gc['ASTEROID_SPEED_SPREAD']=1
gc['ASTEROID_SEPARATION']=22
gc['ASTEROID_IMPULSE']=0
gc['ASTEROID_COLOR']=(200,200,200,255)
gc['ASTEROID_SCALE']=5

# Canister properties
gc['CANISTER_SPEED']=gc['ASTEROID_SPEED']
gc['CANISTER_FRACTION']=0.22
gc['CANISTER_COLOR']=(255,255,255,255)
gc['CANISTER_SCALE']=3

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


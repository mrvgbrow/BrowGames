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
gc['FULL_HEIGHT']=800
gc['FULL_WIDTH']=800
gc['SCREEN_HEIGHT']=800
gc['SCREEN_WIDTH']=800
gc['TOP']=gc['FULL_HEIGHT']-gc['SCREEN_HEIGHT']
gc['LEFT']=gc['FULL_WIDTH']-gc['SCREEN_WIDTH']
gc['SCREEN_COLOR']=(0,0,0)
gc['PAUSE']=False
gc['GRAVITY']=0.01

# Timing
gc['TICK_FRAMERATE']=60

# Player properties
gc['PLAYER_MOVESTEP']=3
gc['PLAYER_SCALE']=4
gc['PLAYER_Y_OFFSET']=gc['SCREEN_WIDTH']/15
gc['PLAYER_CONTROL']='arrows'
gc['PLAYER_COLOR']=(0,255,0,255)

# Object properties
gc['OBJECT_SPEED']=10
gc['OBJECT_SCALE']=16
gc['OBJECT_COLOR']=(255,255,255,255)
gc['OBJECT_PACE']=4

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
    K_i,
    K_j,
    K_k,
    K_l,
    K_r,
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


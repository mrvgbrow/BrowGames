#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import pygame

# General
NUMBER_DIGITS=9
NUMBER_REVERSES=4
SCREEN_COLOR=(0,0,0)
SCREEN_WIDTH=600
SCREEN_HEIGHT=300
FONT_SIZE=40
DIGIT_FONT_SIZE=80
TICK_FRAMERATE=60

# Scoring 
SCORE_MAX=100
SCORE_DECREMENT=1
SCORE_XPOS=0.17
SCORE_YPOS=0.17

# Touchkey
TOUCHKEY_HEIGHT=0.2
TOUCHKEY_COLOR=(0,0,0)

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_ESCAPE,
    K_RETURN,
    K_BACKSPACE,
    KEYDOWN,
    KEYUP,
    QUIT,
)

def scale_parameters():
    global SCORE_XPOS,SCORE_YPOS,TOUCHKEY_HEIGHT
    SCORE_XPOS*=SCREEN_WIDTH
    SCORE_YPOS*=SCREEN_HEIGHT
    TOUCHKEY_HEIGHT*=SCREEN_HEIGHT

def set_preset(preset_dict):
    for parameter in preset_dict:
        globals()[parameter]=preset_dict[parameter]

def get_parameters(parameter_list):
    pars_dict={}
    for par in parameter_list:
       value=globals()[par]
       pars_dict[par]=value
    return pars_dict


#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import pygame
import math

# General
SCREEN_HEIGHT=600
SCREEN_WIDTH=800
FONT_SIZE=36
SCREEN_COLOR=(0,0,0)
SOUND_VOLUME=1

# Timing
TICK_FRAMERATE=60

# Scoring 
SCORE_XPOS=10
SCORE_YPOS=10
SCORE_HIDE=True
TIME_XPOS=10
TIME_YPOS=700
TIME_HIDE=False
CENTER_LINE_HIDE=False

# Paddle properties
PLAYER_MOVESPEED=600
PLAYER1_CONTROL='wasd'
PLAYER2_CONTROL='arrows'
PLAYER1_X_POSITION=0.05
PLAYER2_X_POSITION=0.95
PLAYER_WIDTH=0.016
PLAYER_HEIGHT=0.1
PLAYER1_COLOR=(0,150,150)
PLAYER2_COLOR=(200,200,0)
PLAYER_CONTROL_FACTOR=0.5
PLAYER_RADIUS=0.5
PADDLE_TYPE='normal'

# Ball properties
BALL_NUMBER=10
BALL_SPEED=600
BALL_SPEED_INCREASE=100
BALL_MAX_SPEED=900
BALL_RADIUS=7
BALL_COLOR=(100,200,100)
BALL_MINANGLE_DEGREES=22.5

# AI Properties
AI_PREDICT_BOUNCE=True
AI_ERROR_DISTANCE=0.65

# Bug demos
DISCRETE_STEPS=False

# Bug Demos
ORIGINAL_BOUNCE=True

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_LEFTBRACKET,
    K_RIGHTBRACKET,
    KEYDOWN,
    KEYUP,
    K_p,
    K_w,
    K_s,
    QUIT,
)

def scale_parameters():
    global PLAYER_HEIGHT,PLAYER_WIDTH,PLAYER1_X_POSITION,PLAYER2_X_POSITION,PLAYER_RADIUS,BALL_SPEED,PLAYER_MOVESTEP,TICK_FRAMERATE,BALL_SPEED_INCREASE,BALL_MAX_SPEED
    PLAYER_HEIGHT=PLAYER_HEIGHT*SCREEN_HEIGHT
    PLAYER_WIDTH*=SCREEN_WIDTH
    PLAYER1_X_POSITION*=SCREEN_WIDTH
    PLAYER2_X_POSITION*=SCREEN_WIDTH
    PLAYER_RADIUS*=PLAYER_WIDTH
    PLAYER_MOVESTEP=PLAYER_MOVESPEED/TICK_FRAMERATE
    BALL_SPEED/=TICK_FRAMERATE
    BALL_SPEED_INCREASE/=TICK_FRAMERATE
    BALL_MAX_SPEED/=TICK_FRAMERATE

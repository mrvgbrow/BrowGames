#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import os
import sys
import pygame
import random
import ticker
import sprite_path
import time
import genutils as genu
import aifunctions as aif
import computer_player as cp

class GotchaPlayer(cp.ComputerPlayer):
    def __init__(self,name,sprite,movestep=None,maxdepth=200,checkstep=20,decide_frames=10,
                 random_step_frames=5,redecide_frames=300,image_path=None):
        super(GotchaPlayer,self).__init__(name,sprite,movestep=movestep,maxdepth=maxdepth,
                                          checkstep=checkstep,decide_frames=decide_frames,
                                          random_step_frames=random_step_frames,
                                          redecide_frames=redecide_frames)


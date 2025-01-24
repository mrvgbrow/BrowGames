#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import pygame
import random
import controls as ctrl
import genutils
import math
from . import quadrapong_gameconstants as gc


class Player(pygame.sprite.Sprite):
    def __init__(self,color,player_side,control):
        super(Player,self).__init__()
        if player_side==2 or player_side==4:
            self.orientation='horizontal'
            ysize=gc.PADDLE_WIDTH
            xsize=gc.PADDLE_LENGTH
            position=[0.5*gc.SCREEN_WIDTH,math.copysign(1,3-player_side)*gc.PADDLE_WALL_OFFSET+gc.SCREEN_PAD+(player_side-2)/2*(gc.SCREEN_HEIGHT-2*gc.SCREEN_PAD)]
        else:
            self.orientation='vertical'
            xsize=gc.PADDLE_WIDTH
            ysize=gc.PADDLE_LENGTH
            position=[math.copysign(1,2-player_side)*gc.PADDLE_WALL_OFFSET+gc.SCREEN_PAD+(player_side-1)/2*(gc.SCREEN_WIDTH-2*gc.SCREEN_PAD),0.5*gc.SCREEN_HEIGHT]
        collision_directions=['right','down','left','up']
        self.collision_direction=collision_directions[player_side-1]
        self.surf=pygame.Surface((xsize,ysize))
        self.surf.fill(color)
        self.control=control
        self.surf.set_colorkey(gc.SCREEN_COLOR)
        self.reset_target()
        self.player_side=player_side
        self.rect = self.surf.get_rect(
            center=(
                position[0],
                position[1],
            )
        )
        self.mask=pygame.mask.from_surface(self.surf)

    def update(self, pressed_keys):
        if self.control == 'Computer':
            if self.target>0:
                if random.random()<gc.AI_RANDOM_ADJUST:
                    self.randomize_target_position()
                if self.orientation=='vertical':
                    direction=self.target_position-self.rect.centery
                    if abs(direction) > gc.PLAYER_MOVESTEP:
                        self.rect.move_ip(0,genutils.sign(direction)*gc.PLAYER_MOVESTEP)
                else:
                    direction=self.target_position-self.rect.centerx
                    if abs(direction) > gc.PLAYER_MOVESTEP:
                        self.rect.move_ip(genutils.sign(direction)*gc.PLAYER_MOVESTEP,0)
        elif pressed_keys[ctrl.keycons[self.control]['up']]:
            if self.orientation=='vertical': self.rect.move_ip(0,-gc.PLAYER_MOVESTEP)
        elif pressed_keys[ctrl.keycons[self.control]['down']]:
            if self.orientation=='vertical': self.rect.move_ip(0,gc.PLAYER_MOVESTEP)
        elif pressed_keys[ctrl.keycons[self.control]['right']]:
            if self.orientation=='horizontal': self.rect.move_ip(gc.PLAYER_MOVESTEP,0)
        elif pressed_keys[ctrl.keycons[self.control]['left']]:
            if self.orientation=='horizontal': self.rect.move_ip(-gc.PLAYER_MOVESTEP,0)

        if self.orientation=='vertical':
            if self.rect.top <= gc.PADDLE_LIMIT:
                self.rect.top=gc.PADDLE_LIMIT
            if self.rect.bottom > gc.SCREEN_HEIGHT-gc.PADDLE_LIMIT:
                self.rect.bottom=gc.SCREEN_HEIGHT-gc.PADDLE_LIMIT
        else:
            if self.rect.left <= gc.PADDLE_LIMIT:
                self.rect.left=gc.PADDLE_LIMIT
            if self.rect.right > gc.SCREEN_WIDTH-gc.PADDLE_LIMIT:
                self.rect.right=gc.SCREEN_WIDTH-gc.PADDLE_LIMIT

    def compute_error_distance(self):
        error_distance= gc.PADDLE_LENGTH*gc.AI_ERROR_DISTANCE*(1+gc.AI_YSPEED_ERROR_FACTOR*abs(self.target_ball_obj.speedy)/gc.BALL_MAX_SPEED)
        return error_distance

    def compute_original_angle(self,ballpos,ball_speed):
        location_on_paddle=self.compute_paddle_location(ballpos)
        if self.orientation=='vertical':
            if ball_speed[0]>0:
              original_angle=-math.pi/16*location_on_paddle-math.pi
            else:
              original_angle=math.pi/16*location_on_paddle
        else:
            if ball_speed[1]<0:
              original_angle=-math.pi/16*location_on_paddle+math.pi/2
            else:
              original_angle=math.pi/16*location_on_paddle-math.pi/2
        return original_angle

    def compute_paddle_location(self,ballpos):
        coord=ballpos[1] if self.orientation=='vertical' else ballpos[0]
        selfcoord=self.rect.centery if self.orientation=='vertical' else self.rect.centerx
        location_on_paddle=math.floor((coord-selfcoord)/gc.PADDLE_LENGTH*8)
        return location_on_paddle

    def compute_anglechange(self,ballpos):
        if self.orientation=='vertical':
            location_on_paddle=ballpos[1]-self.rect.centery
        else:
            location_on_paddle=ballpos[0]-self.rect.centerx
        nominal_change=location_on_paddle/gc.PADDLE_LENGTH*math.pi
        if self.player_side==2 or self.player_side==3:
            nominal_change*=-1
        adjusted_change=nominal_change*gc.PADDLE_CONTROL_FACTOR
        return adjusted_change

    def choose_target(self,balls):
        ball_choice=[gc.SCREEN_WIDTH,None,-1]
        for ball_i in balls:
            if self.orientation=='vertical':
                relative_position=self.rect.centerx-ball_i.rect.centerx
                if ball_i.speedx!=0:
                    ball_distance=relative_position/ball_i.speedx
                    target=ball_i.compute_intercept(self.rect.centerx,'x')
                else:
                    ball_distance=gc.SCREEN_WIDTH
                    target=-1000
                player_distance=abs(self.rect.centery-target)/gc.PLAYER_MOVESTEP
            else:
                relative_position=self.rect.centery-ball_i.rect.centery
                if ball_i.speedy!=0:
                    ball_distance=relative_position/ball_i.speedy
                    target=ball_i.compute_intercept(self.rect.centery,'y')
                else:
                    ball_distance=gc.SCREEN_HEIGHT
                    target=-1000
                player_distance=abs(self.rect.centerx-target)/gc.PLAYER_MOVESTEP
            if player_distance<ball_distance and target>gc.PADDLE_LIMIT and target<gc.SCREEN_HEIGHT-gc.PADDLE_LIMIT and ball_distance>0:
                if (abs(target-self.target)>gc.PADDLE_LENGTH/8 or self.target==-1) and ball_distance<ball_choice[0]:
                    ball_choice=[ball_distance,ball_i,target]
        if ball_choice[1]:
            self.target=ball_choice[2]
            self.target_ball=ball_choice[1].ball_id
            self.target_ball_obj=ball_choice[1]
            return ball_choice[1]
        else:
            return False

    def reset_target(self):
        self.target=-1
        self.target_ball=None
        self.target_ball_obj=None

    def randomize_target_position(self):
        error_distance=self.compute_error_distance()
        self.target_position=self.target+2*(random.random()-0.5)*error_distance

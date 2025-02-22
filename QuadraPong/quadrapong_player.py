#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import pygame
import random
import settings 
import paddlefunctions as pf
import controls as ctrl
import genutils
import math
from . import quadrapong_gameconstants as gc


class Player(pygame.sprite.Sprite):
    def __init__(self,color,player_side,control,paddle_type):
        super(Player,self).__init__()
        real_length=min(gc.PADDLE_LENGTH,math.sqrt(gc.PADDLE_RADIUS**2-(gc.PADDLE_RADIUS-2*gc.PADDLE_WIDTH)**2)*2)
        if player_side==2 or player_side==4:
            self.orientation='horizontal'
            ysize=gc.PADDLE_WIDTH if paddle_type=='normal' else gc.PADDLE_RADIUS
            xsize=gc.PADDLE_LENGTH if paddle_type=='normal' else real_length
            position=[0.5*gc.SCREEN_WIDTH,math.copysign(1,3-player_side)*gc.PADDLE_WALL_OFFSET+gc.SCREEN_PAD+(player_side-2)/2*(gc.SCREEN_HEIGHT-2*gc.SCREEN_PAD)]
        else:
            self.orientation='vertical'
            xsize=gc.PADDLE_WIDTH if paddle_type=='normal' else gc.PADDLE_RADIUS
            ysize=gc.PADDLE_LENGTH if paddle_type=='normal' else real_length
            position=[math.copysign(1,2-player_side)*gc.PADDLE_WALL_OFFSET+gc.SCREEN_PAD+(player_side-1)/2*(gc.SCREEN_WIDTH-2*gc.SCREEN_PAD),0.5*gc.SCREEN_HEIGHT]
        collision_directions=['right','down','left','up']
        self.collision_direction=collision_directions[player_side-1]
        self.type=paddle_type
        self.surf=pygame.Surface((xsize,ysize))
        if paddle_type=='normal': self.surf.fill(color)
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
        if paddle_type=='curved': pf.curved_draw(self,color,gc.SCREEN_COLOR,gc.PADDLE_RADIUS,gc.PADDLE_WIDTH)
        self.mask=pygame.mask.from_surface(self.surf)

    def update(self, pressed_keys,mouse_relative):
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
        elif self.control == 'Mouse':
            if self.orientation=='vertical':
                self.rect.move_ip(0,mouse_relative[1]*settings.sets['MOUSE_SENSITIVITY'])
            else:
                self.rect.move_ip(mouse_relative[1]*settings.sets['MOUSE_SENSITIVITY'],0)
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
        error_distance= gc.PADDLE_LENGTH*gc.AI_ERROR_DISTANCE*(1+gc.AI_SPEED_ERROR_FACTOR*abs(self.target_ball_obj.base_speed)/gc.BALL_MAX_SPEED)
        return error_distance

    def curved_draw(self,color):
        if self.orientation=='vertical':
            pygame.draw.circle(self.surf,color,(0,self.surf.get_height()/2),gc.PADDLE_RADIUS)
            pygame.draw.rect(self.surf,gc.SCREEN_COLOR,(0,0,self.surf.get_width()-2*gc.PADDLE_WIDTH,self.surf.get_height()))
        else:
            pygame.draw.circle(self.surf,color,(self.surf.get_width()/2,0),gc.PADDLE_RADIUS)
            pygame.draw.rect(self.surf,gc.SCREEN_COLOR,(0,0,self.surf.get_width(),self.surf.get_height()-2*gc.PADDLE_WIDTH))
        if self.player_side==3:
            self.surf=pygame.transform.flip(self.surf,True,False)
        elif self.player_side==4:
            self.surf=pygame.transform.flip(self.surf,False,True)
        self.mask=pygame.mask.from_surface(self.surf)

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
            if gc.AI_TRY_ALL:
                player_distance=0.0
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

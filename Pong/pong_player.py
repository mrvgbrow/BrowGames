#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import pygame
import random
import settings
import math
from . import pong_gameconstants as gc
import genutils


class Player(pygame.sprite.Sprite):
    def __init__(self,x_position,color,player_id,control,side,paddle_type):
        super(Player,self).__init__()
        self.type=paddle_type
        if paddle_type=='curved':
            self.real_height=min(gc.PLAYER_HEIGHT,math.sqrt(gc.PLAYER_RADIUS**2-(gc.PLAYER_RADIUS-2*gc.PLAYER_WIDTH)**2)*2) ###
            width=gc.PLAYER_RADIUS
        elif paddle_type=='split':
            width=gc.PLAYER_WIDTH
            self.real_height=(gc.SCREEN_HEIGHT-2*gc.WALL_WIDTH)/2+gc.PLAYER_HEIGHT
        else:
            self.real_height=gc.PLAYER_HEIGHT
            width=gc.PLAYER_WIDTH
        self.surf=pygame.Surface((width,self.real_height))
        if paddle_type == 'normal': self.surf.fill(color)
        self.surf.set_colorkey(gc.SCREEN_COLOR)
        self.side=side
        self.target=None
        self.target_position=None
        self.target_position_true=0.0
        self.target_position_x=x_position
        self.player_id=player_id
        self.control=control
        self.rect = self.surf.get_rect(
            center=(
                x_position,
                0.5*gc.SCREEN_HEIGHT,
            )
        )
        if self.type=='curved':
            self.curved_draw(color) 
        elif paddle_type=='split':
            self.split_draw(color) 
        else:
            self.mask=pygame.mask.from_surface(self.surf)

    def update(self, pressed_keys, mouse_relative,balls):
        if self.control == 'Arrows':
            if pressed_keys[gc.K_UP]:
                self.rect.move_ip(0,-gc.PLAYER_MOVESTEP)
            if pressed_keys[gc.K_DOWN]:
                self.rect.move_ip(0,gc.PLAYER_MOVESTEP)
            if gc.PADDLE_ALLOW_LEFTRIGHT:
                if pressed_keys[gc.K_LEFT]:
                    self.rect.move_ip(-gc.PLAYER_MOVESTEP,0)
                if pressed_keys[gc.K_RIGHT]:
                    self.rect.move_ip(gc.PLAYER_MOVESTEP,0)
        elif self.control == 'WASD':
            if pressed_keys[gc.K_w]:
                self.rect.move_ip(0,-gc.PLAYER_MOVESTEP)
            if pressed_keys[gc.K_s]:
                self.rect.move_ip(0,gc.PLAYER_MOVESTEP)
            if gc.PADDLE_ALLOW_LEFTRIGHT:
                if pressed_keys[gc.K_a]:
                    self.rect.move_ip(-gc.PLAYER_MOVESTEP,0)
                if pressed_keys[gc.K_d]:
                    self.rect.move_ip(gc.PLAYER_MOVESTEP,0)
        elif self.control == 'IJKL':
            if pressed_keys[gc.K_i]:
                self.rect.move_ip(0,-gc.PLAYER_MOVESTEP)
            if pressed_keys[gc.K_k]:
                self.rect.move_ip(0,gc.PLAYER_MOVESTEP)
            if gc.PADDLE_ALLOW_LEFTRIGHT:
                if pressed_keys[gc.K_j]:
                    self.rect.move_ip(-gc.PLAYER_MOVESTEP,0)
                if pressed_keys[gc.K_l]:
                    self.rect.move_ip(gc.PLAYER_MOVESTEP,0)
        elif self.control == 'Mouse':
            self.rect.move_ip(0,mouse_relative[1]*settings.sets['MOUSE_SENSITIVITY'])
            if gc.PADDLE_ALLOW_LEFTRIGHT:
                self.rect.move_ip(mouse_relative[0]*settings.sets['MOUSE_SENSITIVITY'],0)
        elif self.control == 'Computer':
            recompute=False
#            if not self.target or (gc.PADDLE_ALLOW_LEFTRIGHT and math.copysign(1,self.target.speedx) != math.copysign(1,self.target_position_x-self.target.rect.centerx)):
            if not self.target:
                if len(balls.sprites())==0:
                    return
                for ball in balls:
                    self.target=ball
                random_x=True if gc.PADDLE_ALLOW_LEFTRIGHT else False
                self.target_position_true,self.target_position_x=self.compute_target_position(random_x=random_x)
                recompute=True
            error_distance=self.compute_error_distance()
            if recompute or random.random()<gc.AI_RANDOM_ADJUST:
                self.target_position=self.target_position_true+2*(random.random()-0.5)*error_distance
            if self.target_position>-error_distance and self.target_position<gc.SCREEN_HEIGHT+error_distance:
                direction_y=self.compute_y_direction()
                direction_x=self.target_position_x-self.rect.centerx
                if abs(direction_y) > gc.PLAYER_MOVESTEP:
                    self.rect.move_ip(0,math.copysign(1,direction_y)*gc.PLAYER_MOVESTEP)
                if abs(direction_x) > gc.PLAYER_MOVESTEP and gc.PADDLE_ALLOW_LEFTRIGHT:
                    self.rect.move_ip(math.copysign(1,direction_x)*gc.PLAYER_MOVESTEP,0)

        self.enforce_boundaries()


    # If a player moves outside the game boundaries, move them back in. All movement kept within the walls.
    def enforce_boundaries(self):
        if self.rect.top <= gc.WALL_WIDTH:
            self.rect.top=gc.WALL_WIDTH
        if self.rect.left <= 0:
            self.rect.left=0
        if self.rect.bottom > gc.SCREEN_HEIGHT-gc.WALL_WIDTH:
            self.rect.bottom=gc.SCREEN_HEIGHT-gc.WALL_WIDTH
        if self.rect.right > gc.SCREEN_WIDTH:
            self.rect.right=gc.SCREEN_WIDTH
        if self.rect.left < gc.WALL_WIDTH or self.rect.right > gc.SCREEN_WIDTH-gc.WALL_WIDTH:
            top_wall=gc.WALL_WIDTH+(gc.SCREEN_HEIGHT-2*gc.WALL_WIDTH-gc.GOAL_SIZE)/2
            bottom_wall=gc.SCREEN_HEIGHT-gc.WALL_WIDTH-(gc.SCREEN_HEIGHT-2*gc.WALL_WIDTH-gc.GOAL_SIZE)/2
            if top_wall-self.rect.top > 2*gc.PLAYER_MOVESTEP and self.rect.left<gc.WALL_WIDTH:
                self.rect.left=gc.WALL_WIDTH
            elif top_wall-self.rect.top > 2*gc.PLAYER_MOVESTEP and self.rect.right>gc.SCREEN_WIDTH-gc.WALL_WIDTH:
                self.rect.right=gc.SCREEN_WIDTH-gc.WALL_WIDTH
            elif self.rect.bottom-bottom_wall > 2*gc.PLAYER_MOVESTEP and self.rect.left<gc.WALL_WIDTH:
                self.rect.left=gc.WALL_WIDTH
            elif self.rect.bottom-bottom_wall > 2*gc.PLAYER_MOVESTEP and self.rect.right>gc.SCREEN_WIDTH-gc.WALL_WIDTH:
                self.rect.right=gc.SCREEN_WIDTH-gc.WALL_WIDTH
            elif self.rect.top < top_wall:
                self.rect.top=top_wall
            elif self.rect.bottom > bottom_wall:
                self.rect.bottom=bottom_wall

    def compute_y_direction(self):
        if self.type=='split':
            if self.target_position>gc.SCREEN_HEIGHT/2:
                return self.target_position-self.rect.bottom+gc.PLAYER_HEIGHT/2
            else:
                return self.target_position-self.rect.top-gc.PLAYER_HEIGHT/2
        else:
            return self.target_position-self.rect.centery

    def compute_anglechange(self,ballpos_y):
        location_on_paddle=ballpos_y-self.rect.centery
        if self.type=='curved':
            if location_on_paddle>gc.PLAYER_RADIUS:
                location_on_paddle=gc.PLAYER_RADIUS
            elif location_on_paddle<-gc.PLAYER_RADIUS:
                location_on_paddle=-gc.PLAYER_RADIUS
            nominal_change=2*math.asin(location_on_paddle/gc.PLAYER_RADIUS)
            return nominal_change
        else:
            nominal_change=location_on_paddle/gc.PLAYER_HEIGHT*math.pi
            adjusted_change=nominal_change*gc.PLAYER_CONTROL_FACTOR
            return adjusted_change

    def compute_original_angle(self,ballpos_y,speed_x):
        location_on_paddle=self.compute_paddle_location(ballpos_y)
        if speed_x>0:
          original_angle=-math.pi/16*location_on_paddle-math.pi
        else:
          original_angle=math.pi/16*location_on_paddle
        return original_angle

    def compute_paddle_location(self,ballpos_y):
        if self.type=='split':
            if ballpos_y > gc.SCREEN_HEIGHT/2:
                location_on_paddle=math.floor((ballpos_y-(self.rect.bottom-gc.PLAYER_HEIGHT/2))/gc.PLAYER_HEIGHT*8)
            else:
                location_on_paddle=math.floor((ballpos_y-(self.rect.top+gc.PLAYER_HEIGHT/2))/gc.PLAYER_HEIGHT*8)
        else:
            location_on_paddle=math.floor((ballpos_y-self.rect.centery)/gc.PLAYER_HEIGHT*8)
        return location_on_paddle

    def compute_error_distance(self):
        error_distance= gc.PLAYER_HEIGHT*gc.AI_ERROR_DISTANCE*(1+gc.AI_YSPEED_ERROR_FACTOR*abs(self.target.speedy)/gc.BALL_MAX_SPEED)
        return error_distance

    def curved_draw(self,color):
        pygame.draw.circle(self.surf,color,(0,self.surf.get_height()/2),gc.PLAYER_RADIUS)
        pygame.draw.rect(self.surf,gc.SCREEN_COLOR,(0,0,self.surf.get_width()-2*gc.PLAYER_WIDTH,self.surf.get_height()))
        if self.rect.centerx>gc.SCREEN_WIDTH/2:
            self.surf=pygame.transform.flip(self.surf,True,False)
        self.mask=pygame.mask.from_surface(self.surf)

    def split_draw(self,color):
        self.surf.fill(color)
        pygame.draw.rect(self.surf,gc.SCREEN_COLOR,(0,gc.PLAYER_HEIGHT,gc.PLAYER_WIDTH,self.surf.get_height()-2*gc.PLAYER_HEIGHT))
        self.mask=pygame.mask.from_surface(self.surf)

    def compute_target_position(self,random_x=False):
        if random_x:
            margin_x=gc.SCREEN_WIDTH/8
            if self.target.speedx>0:
                move_x=self.target.rect.centerx+margin_x+random.random()*(gc.SCREEN_WIDTH-self.target.rect.centerx-margin_x)
            else:
                move_x=self.target.rect.centerx-margin_x-random.random()*(self.target.rect.centerx-margin_x)
        else:
            move_x=self.rect.centerx
        intercept=genutils.find_intercept(self.target.speedx,self.target.speedy,self.target.rect.centerx,self.target.rect.centery,move_x)
        if (intercept < gc.WALL_WIDTH or intercept > gc.SCREEN_HEIGHT-gc.WALL_WIDTH) and gc.AI_PREDICT_BOUNCE:
            intercept_x_0=genutils.find_intercept(self.target.speedy,self.target.speedx,self.target.rect.centery,self.target.rect.centerx,gc.WALL_WIDTH)
            intercept_x_1=genutils.find_intercept(self.target.speedy,self.target.speedx,self.target.rect.centery,self.target.rect.centerx,gc.SCREEN_HEIGHT-gc.WALL_WIDTH)
            if self.target.speedx>0:
                if intercept_x_1 > intercept_x_0:
                    intercept=genutils.find_intercept(self.target.speedx,-self.target.speedy,intercept_x_1,gc.SCREEN_HEIGHT-gc.WALL_WIDTH,move_x)
                else:
                    intercept=genutils.find_intercept(self.target.speedx,-self.target.speedy,intercept_x_0,gc.WALL_WIDTH,move_x)
            else:
                if intercept_x_1 < intercept_x_0:
                    intercept=genutils.find_intercept(self.target.speedx,-self.target.speedy,intercept_x_1,gc.SCREEN_HEIGHT-gc.WALL_WIDTH,move_x)
                else:
                    intercept=genutils.find_intercept(self.target.speedx,-self.target.speedy,intercept_x_0,gc.WALL_WIDTH,move_x)
            if intercept < 0 or intercept > gc.SCREEN_HEIGHT:
                intercept=-1
        return intercept,move_x

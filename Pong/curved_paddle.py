#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import pygame
import random
import math
import physics
import gameconstants as gc


class CurvedPaddle(pygame.sprite.Sprite):
    def __init__(self,x_position,color,player_id,control):
        super(CurvedPaddle,self).__init__()
        self.real_height=min(gc.PLAYER_HEIGHT,math.sqrt(gc.PLAYER_RADIUS**2-(gc.PLAYER_RADIUS-2*gc.PLAYER_WIDTH)**2)*2)
        self.surf=pygame.Surface((gc.PLAYER_RADIUS,self.real_height))
        self.target=None
        self.target_position=None
        self.surf.set_colorkey(gc.SCREEN_COLOR)
        self.control=control
        self.player_id=player_id
        self.rect = self.surf.get_rect(
            center=(
                x_position,
                0.5*gc.SCREEN_HEIGHT,
            )
        )
        self.draw(color)

    def update(self, pressed_keys, balls):
        if self.control == 'arrows':
            if pressed_keys[gc.K_UP]:
                self.rect.move_ip(0,-gc.PLAYER_MOVESTEP)
            if pressed_keys[gc.K_DOWN]:
                self.rect.move_ip(0,gc.PLAYER_MOVESTEP)
            if gc.PADDLE_ALLOW_LEFTRIGHT:
                if pressed_keys[gc.K_LEFT]:
                    self.rect.move_ip(-gc.PLAYER_MOVESTEP,0)
                if pressed_keys[gc.K_RIGHT]:
                    self.rect.move_ip(gc.PLAYER_MOVESTEP,0)
        elif self.control == 'wasd':
            if pressed_keys[gc.K_w]:
                self.rect.move_ip(0,-gc.PLAYER_MOVESTEP)
            if pressed_keys[gc.K_s]:
                self.rect.move_ip(0,gc.PLAYER_MOVESTEP)
            if gc.PADDLE_ALLOW_LEFTRIGHT:
                if pressed_keys[gc.K_a]:
                    self.rect.move_ip(-gc.PLAYER_MOVESTEP,0)
                if pressed_keys[gc.K_d]:
                    self.rect.move_ip(gc.PLAYER_MOVESTEP,0)
        elif self.control == 'computer':
            recompute=False
            if not self.target:
                for ball in balls:
                    self.target=ball
                self.target_position_true=self.compute_target_position()
                recompute=True
                if not self.target:
                    return
            error_distance=self.compute_error_distance()
            if recompute or random.random()<gc.AI_RANDOM_ADJUST:
                self.target_position=self.target_position_true+2*(random.random()-0.5)*error_distance
            if self.target_position>-error_distance and self.target_position<gc.SCREEN_HEIGHT+error_distance:
                direction=self.target_position-self.rect.centery
                if abs(direction) > gc.PLAYER_MOVESTEP:
                    self.rect.move_ip(0,direction/abs(direction)*gc.PLAYER_MOVESTEP)

        if self.rect.top <= gc.WALL_WIDTH:
            self.rect.top=gc.WALL_WIDTH
        if self.rect.left <= gc.WALL_WIDTH:
            self.rect.left=gc.WALL_WIDTH
        if self.rect.bottom > gc.SCREEN_HEIGHT-gc.WALL_WIDTH:
            self.rect.bottom=gc.SCREEN_HEIGHT-gc.WALL_WIDTH
        if self.rect.right > gc.SCREEN_WIDTH-gc.WALL_WIDTH:
            self.rect.right=gc.SCREEN_WIDTH-gc.WALL_WIDTH

    def compute_anglechange(self,ballpos_y):
        location_on_paddle=ballpos_y-self.rect.centery
        if location_on_paddle>gc.PLAYER_RADIUS:
            location_on_paddle=gc.PLAYER_RADIUS
        elif location_on_paddle<-gc.PLAYER_RADIUS:
            location_on_paddle=-gc.PLAYER_RADIUS
        nominal_change=2*math.asin(location_on_paddle/gc.PLAYER_RADIUS)
        return nominal_change
    
    def draw(self,color):
        pygame.draw.circle(self.surf,color,(0,self.surf.get_height()/2),gc.PLAYER_RADIUS)
        pygame.draw.rect(self.surf,gc.SCREEN_COLOR,(0,0,self.surf.get_width()-2*gc.PLAYER_WIDTH,self.surf.get_height()))
        if self.rect.centerx>gc.SCREEN_WIDTH/2:
            self.surf=pygame.transform.flip(self.surf,True,False)
        self.mask=pygame.mask.from_surface(self.surf)

    def compute_error_distance(self):
        error_distance= gc.PLAYER_HEIGHT*gc.AI_ERROR_DISTANCE*(1+gc.AI_YSPEED_ERROR_FACTOR*abs(self.target.speedy)/gc.BALL_MAX_SPEED)
        return error_distance

    def compute_target_position(self):
        intercept=physics.find_intercept(self.target.speedx,self.target.speedy,self.target.rect.centerx,self.target.rect.centery,self.rect.centerx)
        if (intercept < gc.WALL_WIDTH or intercept > gc.SCREEN_HEIGHT-gc.WALL_WIDTH) and gc.AI_PREDICT_BOUNCE:
            intercept_x_0=physics.find_intercept(self.target.speedy,self.target.speedx,self.target.rect.centery,self.target.rect.centerx,gc.WALL_WIDTH)
            intercept_x_1=physics.find_intercept(self.target.speedy,self.target.speedx,self.target.rect.centery,self.target.rect.centerx,gc.SCREEN_HEIGHT-gc.WALL_WIDTH)
            if self.target.speedx>0:
                if intercept_x_1 > intercept_x_0:
                    intercept=physics.find_intercept(self.target.speedx,-self.target.speedy,intercept_x_1,gc.SCREEN_HEIGHT-gc.WALL_WIDTH,self.rect.centerx)
                else:
                    intercept=physics.find_intercept(self.target.speedx,-self.target.speedy,intercept_x_0,gc.WALL_WIDTH,self.rect.centerx)
            else:
                if intercept_x_1 < intercept_x_0:
                    intercept=physics.find_intercept(self.target.speedx,-self.target.speedy,intercept_x_1,gc.SCREEN_HEIGHT-gc.WALL_WIDTH,self.rect.centerx)
                else:
                    intercept=physics.find_intercept(self.target.speedx,-self.target.speedy,intercept_x_0,gc.WALL_WIDTH,self.rect.centerx)
            if intercept < 0 or intercept > gc.SCREEN_HEIGHT:
                intercept=-1
        return intercept

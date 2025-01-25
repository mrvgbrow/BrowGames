#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import pygame
import os
import random
from . import spacerace_gameconstants as gc
import settings
import gameobject as go
import spritefunctions as sf
import controls as ctrl

def decide_move(sprite_move,sprites_avoid,movestep,nsteps=1):
    prect=[sprite_move.rect.left,sprite_move.rect.right,sprite_move.rect.top+movestep,sprite_move.rect.bottom+movestep]
    for sprite_avoid in sprites_avoid:
        for step in range(nsteps):
            erect=sprite_avoid.rect
            if erect.left+step*sprite_avoid.velocity.x<=prect[1] and erect.right+step*sprite_avoid.velocity.x>=prect[0] and erect.top<=prect[3]+step*movestep and erect.bottom>=prect[2]+step*movestep:
                return False
    return True

class PlayerShip(go.GameObject):
    def __init__(self,sprite_name,position,move_speed=0,control='Computer',player_side=1,color=None,scale=None,pace=None,boundary=None,image_path='',collidecount=None):
        self.init_position=position
        super(PlayerShip,self).__init__(sprite_name,position,color=color,scale=scale,pace=pace,boundary=boundary,image_path=image_path,collidecount=collidecount)
        self.add_sequences()
        self.power_counter=0
        self.animate=gc.gc['PLAYER_ANIMATE']
        self.control=control
        self.player_side=player_side
        self.move_speed=move_speed
        self.powerup=False

    def update(self,pressed_keys,asteroids,gravity):
        super(PlayerShip,self).update_tickers()
        if not super(PlayerShip,self).check_collide_counter(): return
        self.invisible=False
        if not self.sequence.update():
            if self.dead:
                pygame.sprite.Sprite.kill(self)
            if self.sequence.next_sequence:
                self.sequence.reset()
                self.set_sequence(self.sequence.next_sequence)
            else:
                self.set_sequence(self.default_sequence)
        self.surf=self.sequence.get_surface(flip_x=self.flip[0],flip_y=self.flip[1])
        self.mask=self.sequence.get_mask(flip_x=self.flip[0],flip_y=self.flip[1])
        if (self.control == 'Computer'):
            if self.player_side==1:
                nsteps=gc.gc['PLAYER1_STEPS_ANTICIPATE']
            else:
                nsteps=gc.gc['PLAYER2_STEPS_ANTICIPATE']
            if self.powerup or decide_move(self,asteroids,-self.move_speed,nsteps=nsteps):
                if self.animate:
                    if self.sequence.name=='Default':
                        self.set_sequence('Takeoff')
                    if self.sequence.name=='DefaultPower':
                        self.set_sequence('TakeoffPower')
                if gravity==0:
                    self.position.y-=self.move_speed
                else:
                    self.velocity.y-=gc.gc['PLAYER_ACCELERATION']
            if self.sequence.name=='Burn':
                self.set_sequence('Deburn')
            if self.sequence.name=='BurnPower':
                self.set_sequence('DeburnPower')
        elif pressed_keys[ctrl.keycons[self.control]['up']]:
            if self.animate:
                if self.sequence.name=='Default':
                    self.set_sequence('Takeoff')
                if self.sequence.name=='DefaultPower':
                    self.set_sequence('TakeoffPower')
            if gravity==0:
                self.position.y-=self.move_speed
            else:
                self.velocity.y-=gc.gc['PLAYER_ACCELERATION']
        elif pressed_keys[ctrl.keycons[self.control]['down']]:
            if gravity==0:
                self.position.y+=self.move_speed
        else:
            if self.animate:
                if self.sequence.name=='Burn':
                    self.set_sequence('Deburn')
                if self.sequence.name=='BurnPower':
                    self.set_sequence('DeburnPower')
        if self.power_counter>0:
            self.power_counter-=1
            if self.power_counter==0:
                self.set_powerup(power=False)
        if gravity>0:
            self.update_motion((0,gravity))
            self.update_position(self.velocity)
        super(PlayerShip,self).perform_movement()
        if self.rect.centery > gc.gc['PLAYER_Y_START'] and gravity>0:
            self.reset()
            super(PlayerShip,self).perform_movement()
        self.check_boundary()

    def reset(self,wrap=False):
        self.position.y=self.init_position[1]
        if wrap: self.position.y+=self.rect.bottom-self.rect.top
        self.position.x=self.init_position[0]
        self.velocity.y=0
        self.velocity.x=0
        self.set_powerup(power=False)
        super(PlayerShip,self).reset_collide()
        self.invisible=True

    def set_powerup(self,power=True):
        if power and self.powerup:
            return
        if power:
            self.power_counter=gc.gc['POWERUP_TIME']
            sequence_name=self.sequence.name+'Power'
        else:
            self.power_counter=0
            sequence_name=self.default_sequence
        self.set_sequence(sequence_name)
        self.powerup=power

    def add_sequences(self):
        self.add_sequence('Takeoff',next_sequence='Burn',loop=0)
        self.add_sequence('Burn')
        self.add_sequence('Deburn',loop=0,next_sequence='Default')
        self.add_sequence('DefaultPower')
        self.add_sequence('BurnPower')
        self.add_sequence('TakeoffPower',next_sequence='BurnPower',loop=0)
        self.add_sequence('DeburnPower',next_sequence='DefaultPower',loop=0)

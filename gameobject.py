#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import pygame
import random
import ticker
import math
import genutils as genu
import controls as ctrl
from collections import deque
import gameconstants as gc
import spritefunctions as sf


class GameObject(pygame.sprite.Sprite):
    def __init__(self,sprite_name,position,scale=4,color=None,pace=4,flip=[0,0],
                 loop=-1,velocity=[0,0],default_sequence=None,path=None,
                 speed=None,boundary=None,angle=0,sprite_id=None,key_mode=None,
                 tie=None,collidecount=None,birthcount=None,image_path='',
                 move_mode=None,controller=None,angle0=0):
        super(GameObject,self).__init__()
        self.image_path=image_path
        self.build_sprite(sprite_name,color,scale,pace,loop,angle0)
        if not default_sequence:
            default_index=random.randint(1,self.default_count)
            default_sequence='Default'
            if default_index>1:
                default_sequence+=str(default_index)
        self.controller=controller
        self.default_sequence=default_sequence
        self.tie=tie
        self.key_mode=key_mode
        self.ticker_dict=None
        self.sprite_name=sprite_name
        if sprite_id:
            self.sprite_id=sprite_id
        self.default_color=color
        self.default_scale=scale
        self.default_pace=pace
        if collidecount:
            self.add_ticker('Collide',collidecount)
        if birthcount:
            self.add_ticker('Birth',birthcount)
        self.set_sequence(self.default_sequence)
        self.surf=self.sequence.get_surface(flip_x=flip[0],flip_y=flip[1])
        self.mask=self.sequence.get_mask(flip_x=flip[0],flip_y=flip[1])
        self.angle=angle
        self.boundary=boundary
        self.dead=False
        self.path=path
        if path:
            self.move_mode='Path'
            self.path_index=0
        else:
            if not move_mode:
                self.move_mode='External'
            else:
                self.move_mode=move_mode
            self.path_index=None
        self.flip=flip
        self.velocity=pygame.math.Vector2(velocity[0],velocity[1])
        self.position=pygame.math.Vector2(position[0],position[1])
        self.posqueue=deque([self.position.copy()]*2)
        if not speed:
            self.speed=self.velocity.magnitude()
        else:
            self.speed=speed
        if color:
            sf.fill(self.surf,color)
        self.rect=self.surf.get_rect(
            center=(
                self.position.x,
                self.position.y,
            )
        )

    def update_sequence(self):
        if not self.sequence.update():
            if self.dead:
                pygame.sprite.Sprite.kill(self)
            if self.sequence.next_sequence:
                self.sequence.reset()
                self.set_sequence(self.sequence.next_sequence)
            else:
                self.set_sequence(self.default_sequence)

    def update_tickers(self):
        if self.ticker_dict:
            for ticker_i in self.ticker_dict:
                self.ticker_dict[ticker_i].update()

    def update(self,impulse=None,step=None):
        self.update_tickers()
        self.update_sequence()
        self.surf=self.sequence.get_surface(flip_x=self.flip[0],
                                            flip_y=self.flip[1])
        self.mask=self.sequence.get_mask(flip_x=self.flip[0],
                                         flip_y=self.flip[1])
        if self.move_mode=='External' or self.move_mode == 'Random':
            if impulse:
                self.update_motion(impulse)
            if step:
                self.update_position(step)
            self.position.x+=self.velocity[0]
            self.position.y+=self.velocity[1]
        elif self.move_mode=='Path':
            if self.path_index<len(self.path.path):
                target=self.path.path[self.path_index]
                self.position=self.position.move_towards(target,self.speed)
                if self.position==target:
                    self.path_index+=1
        elif self.move_mode=='Tied':
            self.update_tie_position()
        self.perform_movement()
        self.check_boundary()

    def check_boundary(self):
        if self.boundary:
            if True in self.boundary.stop:
                if self.rect.centerx>self.boundary.right-self.rect.width/2 and self.boundary.stop[2]:
                    self.position.x=self.boundary.right-self.rect.width/2
                elif self.rect.centerx<self.boundary.left+self.rect.width/2 and self.boundary.stop[0]:
                    self.position.x=self.boundary.left+self.rect.width/2
                elif self.rect.centery<self.boundary.top+self.rect.height/2 and self.boundary.stop[1]:
                    self.position.y=self.boundary.top+self.rect.height/2
                elif self.rect.centery>self.boundary.bottom-self.rect.height/2 and self.boundary.stop[3]:
                    self.position.y=self.boundary.bottom-self.rect.height/2
            elif True in self.boundary.wrap:
                if self.rect.left>self.boundary.right and self.boundary.wrap[2]:
                    self.position.x=self.boundary.left-self.rect.width/2
                elif self.rect.right<self.boundary.left and self.boundary.wrap[0]:
                    self.position.x=self.boundary.right+self.rect.width/2
                elif self.rect.bottom<self.boundary.top and self.boundary.wrap[1]:
                    self.position.y=self.boundary.bottom+self.rect.height/2
                elif self.rect.top>self.boundary.bottom and self.boundary.wrap[3]:
                    self.position.y=self.boundary.top-self.rect.height/2
            elif True in self.boundary.bounce:
                if self.rect.right>self.boundary.right and self.boundary.bounce[2]:
                    self.velocity.x*=-1
                elif self.rect.left<self.boundary.left and self.boundary.bounce[0]:
                    self.velocity.x*=-1
                elif self.rect.top<self.boundary.top and self.boundary.bounce[1]:
                    self.velocity.y*=-1
                elif self.rect.bottom>self.boundary.bottom and self.boundary.bounce[3]:
                    self.velocity.y*=-1
            else:
                if self.rect.left>self.boundary.right or self.rect.right<self.boundary.left or self.rect.top>self.boundary.bottom or self.rect.bottom<self.boundary.top:
                    self.kill()

    def revert_position(self,n_back):
        self.position=self.posqueue[n_back-1].copy()
        self.perform_movement()

    def update_history(self):
        self.posqueue.pop()
        self.posqueue.appendleft(self.position.copy())

    def update_motion(self,impulse,thrust=None):
        if not thrust:
            self.velocity.x+=impulse[0]
            self.velocity.y+=impulse[1]
        else:
            self.velocity.y-=thrust*math.cos(self.angle)
            self.velocity.x-=thrust*math.sin(self.angle)

    def kill(self):
        self.dead=True
        self.set_sequence('Die')

    def update_position(self,step):
        self.position.x+=step[0]
        self.position.y+=step[1]

    def update_tie_position(self):
        self.angle=self.tie.angle
        self.position.x=self.tie.position.x-self.tie_offset.x*math.cos(self.angle)+self.tie_offset.y*math.sin(self.angle)
        self.position.y=self.tie.position.y+self.tie_offset.x*math.sin(self.angle)+self.tie_offset.y*math.cos(self.angle)

    def perform_movement(self):
        self.rect.move_ip(round(self.position.x-self.rect.centerx),
                          round(self.position.y-self.rect.centery))
        self.update_history()

    def set_sequence(self,sequence_name):
        self.sequence=self.sequence_dict[sequence_name]

    def build_sprite(self,sprite_name,color,scale,pace,loop,angle0):
        self.sequence_dict = {
                'Default' : sf.Sequence(sprite_name=sprite_name,name='Default',
                                        image_path=self.image_path,
                                        frozen=False,scale=scale,color=color,
                                        pace=pace,loop=loop,angle0=angle0),
                'Die' : sf.Sequence(sprite_name=sprite_name,name='Die',
                                    image_path=self.image_path,
                                    frozen=False,scale=scale,color=color,
                                    pace=pace,loop=0,angle0=angle0)
        }
        default_found=True
        index=1
        while default_found:
            index+=1
            default_string='Default'+str(index)
            seq=sf.Sequence(sprite_name=sprite_name,name=default_string,
                            frozen=False,scale=scale,color=color,pace=pace,
                            image_path=self.image_path,loop=loop)
            if seq.empty or index==9:
                default_found=False
            else:
                self.sequence_dict[default_string]=seq
        self.default_count=index-1

    def add_tie(self,tie,offset):
        self.tie=tie
        self.tie_offset=pygame.math.Vector2(offset)

    def add_sequence(self,name,frozen=False,color=None,pace=None,loop=-1,scale=None,next_sequence=None):
        if not color:
            color=self.default_color
        if not pace:
            pace=self.default_pace
        if not scale:
            scale=self.default_scale
        self.sequence_dict[name]=sf.Sequence(sprite_name=self.sprite_name,
                                             name=name,frozen=frozen,
                                             scale=scale,loop=loop,color=color,
                                             image_path=self.image_path,pace=pace,
                                             next_sequence=next_sequence)

    def add_ticker(self,name,count,loop=0):
        if not self.ticker_dict:
            self.ticker_dict={}
        self.ticker_dict[name]=ticker.Ticker(name,count,loop=loop)

    def reset_collide(self):
        if self.ticker_dict and 'Collide' in self.ticker_dict:
            self.ticker_dict['Collide'].reset()

    def check_collide_counter(self):
        if self.ticker_dict:
            if 'Collide' in self.ticker_dict:
                if not self.ticker_dict['Collide'].is_finished():
                    return False
            if 'Birth' in self.ticker_dict:
                if not self.ticker_dict['Birth'].is_finished():
                    return False
        return True


class Burst(GameObject):
    def __init__(self,sprite_name,position,scale=4,color=None,pace=4,flip=[0,0],loop=0,image_path=''):
        super(Burst,self).__init__(sprite_name,position,scale=scale,color=color,
                                   pace=pace,flip=flip,loop=loop,image_path=image_path)

    def update(self):
        if not self.sequence.update():
            if self.dead:
                pygame.sprite.Sprite.kill(self)
            else:
                self.kill()
            self.set_sequence(self.default_sequence)
        self.surf=self.sequence.get_surface(flip_x=self.flip[0],
                                            flip_y=self.flip[1])
        self.mask=self.sequence.get_mask(flip_x=self.flip[0],
                                         flip_y=self.flip[1])

class PlayerFixed(GameObject):
    def __init__(self,sprite_name,position,scale=4,color=None,pace=4,flip=[0,0],
                 loop=0,move_mode='External',control_step=[0,0,0,0],
                 boundary=None,player_side=None,velocity=[0,0],
                 birthcount=180,key_mode=None,angle=0,image_path=''):
        super(PlayerFixed,self).__init__(sprite_name,position,scale=scale,
                                         color=color,pace=pace,flip=flip,
                                         loop=loop,move_mode=move_mode,
                                         boundary=boundary, velocity=velocity,
                                         birthcount=birthcount,image_path=image_path,
                                         key_mode=key_mode,angle=angle)
        self.control_step=control_step
        if player_side:
            self.player_side=player_side

    def update_controls_computer(self,pressed_keys):
        direction=[0,0]
        if pressed_keys[self.key_mode]['up']:
            self.position.y-=self.control_step[1]
            direction[1]=-1
        if pressed_keys[self.key_mode]['down']:
            self.position.y+=self.control_step[3]
            direction[1]=1
        if pressed_keys[self.key_mode]['left']:
            self.position.x-=self.control_step[0]
            direction[0]=-1
        if pressed_keys[self.key_mode]['right']:
            self.position.x+=self.control_step[2]
            direction[0]=1
        return direction

    def update_controls(self,pressed_keys):
        direction=[0,0]
        if pressed_keys[ctrl.keycons[self.key_mode]['up']]:
            self.position.y-=self.control_step[1]
            direction[1]=-1
        if pressed_keys[ctrl.keycons[self.key_mode]['down']]:
            self.position.y+=self.control_step[3]
            direction[1]=1
        if pressed_keys[ctrl.keycons[self.key_mode]['left']]:
            self.position.x-=self.control_step[0]
            direction[0]=-1
        if pressed_keys[ctrl.keycons[self.key_mode]['right']]:
            self.position.x+=self.control_step[2]
            direction[0]=1
        return direction

    def update_all(self,pressed_keys,computer_keys=None):
        if computer_keys and self.move_mode=='computer':
            direction=self.update_controls_computer(computer_keys)
        else:
            direction=self.update_controls(pressed_keys)
        self.update()
        return direction
    
class GameObjectSimple(pygame.sprite.Sprite):
    def __init__(self,position,sprite_name=None,scale=4,color=None,angle0=0,
                 default_sequence=None,sprite_id=None,surface=None,mask=None,
                 image_path=''):
        super(GameObjectSimple,self).__init__(image_path=image_path)
        if sprite_name:
            self.build_sprite(sprite_name,color,scale)
            if not default_sequence:
                default_sequence='Default'
            self.default_sequence=default_sequence
            self.set_sequence(self.default_sequence)
        self.sprite_name=sprite_name
        self.angle0=angle0
        if sprite_id:
            self.sprite_id=sprite_id
        if not surface:
            self.surf=self.sequence.get_surface()
        else:
            self.surf=surface
        if not mask:
            self.mask=self.sequence.get_mask()
        else:
            self.mask=mask
        self.position=pygame.math.Vector2(position[0],position[1])
        if color:
            sf.fill(self.surf,color)
        self.rect=self.surf.get_rect(
            center=(
                self.position.x,
                self.position.y,
            )
        )

    def update(self,impulse=None,step=None):
        if not self.sequence.update():
            self.set_sequence(self.default_sequence)
        self.surf=self.sequence.get_surface()
        self.mask=self.sequence.get_mask()

    def set_sequence(self,sequence_name):
        self.sequence=self.sequence_dict[sequence_name]

    def build_sprite(self,sprite_name,color,scale):
        self.sequence_dict = {
                'Default' : sf.Sequence(sprite_name=sprite_name,name='Default',
                                        frozen=True,scale=scale,color=color,
                                        loop=-1),
        }
        index=1

class Rocket(GameObject):
    def __init__(self,sprite_name,position,scale=4,color=None,pace=4,flip=[0,0],
                 loop=0,move_mode='External',boundary=None,player_side=None,
                 velocity=[0,0],rot_step=[0,0],speed_step=0,angle=0,angle0=0,
                 sprite_id=None,tie=None,birthcount=180,key_mode=None,image_path=''):
        super(Rocket,self).__init__(sprite_name,position,scale=scale,
                                    color=color,pace=pace,flip=flip,loop=loop,
                                    move_mode=move_mode,boundary=boundary,
                                    velocity=velocity,angle=angle,image_path=image_path,
                                    sprite_id=sprite_id,tie=tie,angle0=angle0,
                                    birthcount=birthcount,key_mode=key_mode)
        self.rot_step=rot_step
        self.unrotated_surf=self.sequence.get_surface()
        self.speed_step=speed_step
        if player_side:
            self.player_side=player_side

    def update_controls(self,pressed_keys):
        direction=[0,0]
        if pressed_keys[ctrl.keycons[self.key_mode]['left']]:
            self.angle+=self.rot_step
        if pressed_keys[ctrl.keycons[self.key_mode]['right']]:
            self.angle-=self.rot_step
        if pressed_keys[ctrl.keycons[self.key_mode]['up']]:
            self.update_motion(0,thrust=self.speed_step)
        return direction

    def update(self,pressed_keys):
        self.update_tickers()
        self.update_sequence()
        if not self.move_mode=='Tied':
            self.update_controls(pressed_keys)
        self.unrotated_surf=self.sequence.get_surface(flip_x=self.flip[0],
                                                      flip_y=self.flip[1])
        self.surf,self.rect=sf.rot_center(self.unrotated_surf,
                                          self.angle*180/math.pi,
                                          self.rect.centerx,self.rect.centery)
        self.mask=self.sequence.get_mask(flip_x=self.flip[0],
                                         flip_y=self.flip[1])
        if self.move_mode=='Tied':
            self.update_tie_position()
        else:
            self.update_position([self.velocity.x,self.velocity.y])
        self.perform_movement()
        self.check_boundary()

    def get_bullet_location(self):
        pos_x=self.position.x-self.rect.width/2*math.sin(self.angle)
        pos_y=self.position.y-self.rect.height/2*math.cos(self.angle)
        return [pos_x,pos_y]

class GameObjectRot(GameObject):
    def __init__(self,sprite_name,position,scale=4,color=None,pace=4,flip=[0,0],
                 loop=-1,move_mode='External',boundary=None,angle0=0,image_path='',
                 velocity=[0,0],angle=0,sprite_id=None,tie=None):
        super(GameObjectRot,self).__init__(sprite_name,position,scale=scale,
                                           color=color,pace=pace,flip=flip,
                                           loop=loop,move_mode=move_mode,
                                           boundary=boundary,angle0=angle0,
                                           velocity=velocity,angle=angle,
                                           image_path=image_path,
                                           sprite_id=sprite_id,tie=tie)
        self.unrotated_surf=self.sequence.get_surface()

    def update(self):
        self.update_tickers()
        self.update_sequence()
        self.unrotated_surf=self.sequence.get_surface(flip_x=self.flip[0],
                                                      flip_y=self.flip[1])
        self.surf,self.rect=sf.rot_center(self.unrotated_surf,
                                          self.angle*180/math.pi,
                                          self.rect.centerx,self.rect.centery)
        self.mask=self.sequence.get_mask(flip_x=self.flip[0],flip_y=self.flip[1])
        if self.move_mode=='Tied':
            self.update_tie_position()
        else:
            self.update_position([self.velocity.x,self.velocity.y])
        self.perform_movement()
        self.check_boundary()


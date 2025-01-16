#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import pygame
import random
import spacerace_gameconstants as gc
import spacerace_spritefunctions as sf


class GameObject(pygame.sprite.Sprite):
    def __init__(self,sprite_name,position,scale=4,color=None,pace=4,flip=[0,0],loop=-1,velocity=[0,0],default_sequence=None,path=None,speed=None,boundary=None,angle=0):
        super(GameObject,self).__init__()
        self.build_sprite(sprite_name,color,scale,pace,loop)
        if not default_sequence:
            default_index=random.randint(1,self.default_count)
            default_sequence='Default'
            if default_index>1:
                default_sequence+=str(default_index)
        self.default_sequence=default_sequence
        self.sprite_name=sprite_name
        self.default_color=color
        self.default_scale=scale
        self.default_pace=pace
        self.set_sequence(self.default_sequence)
        self.surf=self.sequence.get_surface(flip_x=flip[0],flip_y=flip[1])
        self.mask=self.sequence.get_mask(flip_x=flip[0],flip_y=flip[1])
        self.angle=angle
        self.boundary=boundary
        self.dead=False
        self.path=path
        if path:
            self.mode='Path'
            self.path_index=0
        else:
            self.mode='External'
            self.path_index=None
        self.flip=flip
        self.velocity=pygame.math.Vector2(velocity[0],velocity[1])
        self.position=pygame.math.Vector2(position[0],position[1])
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

    def update(self,impulse=None,step=None):
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
        if self.mode=='External':
            if impulse:
                self.update_motion(impulse)
            if step:
                self.update_position(step)
            self.position.x+=self.velocity[0]
            self.position.y+=self.velocity[1]
        elif self.mode=='Path':
            if self.path_index<len(self.path.path):
                target=self.path.path[self.path_index]
                self.position=self.position.move_towards(target,self.speed)
                if self.position==target:
                    self.path_index+=1
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

    def set_control(self,control_mode):
        self.mode=control_mode

    def update_motion(self,impulse,thrust=None):
        self.velocity.x+=impulse[0]
        self.velocity.y+=impulse[1]
        self.speed=self.velocity.magnitude()

    def kill(self):
        self.dead=True
        self.set_sequence('Die')

    def update_position(self,step):
        self.position.x+=step[0]
        self.position.y+=step[1]

    def perform_movement(self):
        self.rect.move_ip(round(self.position.x-self.rect.centerx),round(self.position.y-self.rect.centery))

    def set_sequence(self,sequence_name):
        self.sequence=self.sequence_dict[sequence_name]

    def build_sprite(self,sprite_name,color,scale,pace,loop):
        self.sequence_dict = {
                'Default' : sf.Sequence(sprite_name=sprite_name,name='Default',frozen=False,scale=scale,color=color,pace=pace,loop=loop),
                'Die' : sf.Sequence(sprite_name=sprite_name,name='Die',frozen=False,scale=scale,color=color,pace=pace,loop=0)
        }
        default_found=True
        index=1
        while default_found:
            index+=1
            default_string='Default'+str(index)
            seq=sf.Sequence(sprite_name=sprite_name,name=default_string,frozen=False,scale=scale,color=color,pace=pace,loop=loop)
            if seq.empty or index==9:
                default_found=False
            else:
                self.sequence_dict[default_string]=seq
        self.default_count=index-1

    def add_sequence(self,name,frozen=False,color=None,pace=None,loop=-1,scale=None,next_sequence=None):
        if not color:
            color=self.default_color
        if not pace:
            pace=self.default_pace
        if not scale:
            scale=self.default_scale
        self.sequence_dict[name]=sf.Sequence(sprite_name=self.sprite_name,name=name,frozen=frozen,scale=scale,loop=loop,color=color,pace=pace,next_sequence=next_sequence)

class Burst(GameObject):
    def __init__(self,sprite_name,position,scale=4,color=None,pace=4,flip=[0,0],loop=0):
        super(Burst,self).__init__(sprite_name,position,scale=scale,color=color,pace=pace,flip=flip,loop=loop)

    def update(self):
        if not self.sequence.update():
            if self.dead:
                pygame.sprite.Sprite.kill(self)
            else:
                self.kill()
            self.set_sequence(self.default_sequence)
        self.surf=self.sequence.get_surface(flip_x=self.flip[0],flip_y=self.flip[1])
        self.mask=self.sequence.get_mask(flip_x=self.flip[0],flip_y=self.flip[1])


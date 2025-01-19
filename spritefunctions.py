#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import os
import math
import pygame
import genutils as genu

def fill(surface,color):
    w, h = surface.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pygame.Color(r, g, b, a))

def rot_center(image, angle, x, y):

    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

    return rotated_image, new_rect

class Sequence():
    def __init__(self,sprite_name=None,name=None,opacity=[],images=[],rotation=[],trans_x=[],trans_y=[],delay=[],frozen=False,loop=0,color=None,flip_x=[],flip_y=[],scale=None,pace=None,next_sequence=None,angle0=0,nrotations=1,image_path=''):
        self.sprite_name=sprite_name
        self.name=name
        self.image_path=image_path
        self.next_sequence=next_sequence
        self.path=os.path.join(image_path,'sprites',self.sprite_name)
        self.empty=False
        if sprite_name and name:
            if not self.read_sequence():
                self.empty=True
                return None
        if not self.images:
            self.images=images
        if not rotation:
            rotations=[0]*len(self.images)
        self.rotation=rotation
        self.nrotations=nrotations
        self.angle0=angle0
        if not trans_x:
            trans_x=[0]*len(self.images)
        self.trans_x=trans_x
        if not trans_y:
            trans_y=[0]*len(self.images)
        self.trans_y=trans_y
        if not delay:
            delay=[1]*len(self.images)
        self.delay=delay
        if not opacity:
            opacity=[1]*len(self.images)
        self.opacity=opacity
        if not flip_x:
            flip_x=[False]*len(self.images)
        self.flip_x=flip_x
        if not flip_y:
            flip_y=[False]*len(self.images)
        self.flip_y=flip_y
        self.frozen=frozen
        self.now=0
        self.index=0
        self.scale=scale
        self.loop=loop
        self.finished=False
        self.loop_index=0
        self.build_surfaces(color,scale)
        if pace:
            self.apply_pace(pace)

    def apply_pace(self,pace):
        self.pace=pace
        for i in range(len(self.delay)):
            self.delay[i]*=pace

    # Current image
    def get_image(self):
        return self.images[self.index]

    # Current rotation
    def get_rotation(self):
        return self.rotation[self.index]

    # Current X translation
    def get_trans_x(self):
        return self.trans_x[self.index]*self.scale

    # Current X flip
    def get_flip_x(self):
        return self.flip_x[self.index]

    # Current Y flip
    def get_flip_y(self):
        return self.flip_y[self.index]

    # Current Y translation
    def get_trans_y(self):
        return self.trans_y[self.index]*self.scale

    # Current delay
    def get_delay(self):
        return self.delay[self.index]

    def set_delay(self,delay):
        self.delay[self.index]=delay

    def set_opacity(self,opacity):
        self.opacity[self.index]=opacity

    def set_flip_x(self,flip_x):
        self.flip_x[self.index]=flip_x

    def set_flip_y(self,flip_y):
        self.flip_y[self.index]=flip_y

    def set_rotation(self,rotation):
        self.rotation[self.index]=rotation

    def set_trans_x(self,trans_x):
        self.trans_x[self.index]=trans_x

    def set_trans_y(self,trans_y):
        self.trans_y[self.index]=trans_y

    # Current opacity
    def get_opacity(self):
        return self.opacity[self.index]

    # Current surface
    def get_surface(self,flip_x=0,flip_y=0):
        flip_index=2*flip_y+flip_x
        return self.surfaces[self.index][flip_index]

    # Current mask
    def get_mask(self,flip_x=0,flip_y=0):
        flip_index=2*flip_y+flip_x
        return self.masks[self.index][flip_index]

    # Based on the current value of the time counter, determine which
    # image is active 
    def update(self):
        if self.empty:
            return False
        if self.finished:
            return False
        if self.frozen:
            return True
        self.now+=1
        delay_index=-1
        total=0
        while total<self.now:
            delay_index+=1
            if delay_index<len(self.delay):
                total+=self.delay[delay_index]
            else:
                total+=1

        # If reached the end of the sequence, mark as finished or loop again.
        if delay_index==len(self.images):
            if self.loop_index==self.loop:
                self.finished=True
                return False
            else:
                self.now=0
                delay_index=0
                self.loop_index+=1

        self.index=delay_index
        return True

    def reset(self):
        self.now=0
        self.index=0
        self.finished=False
        self.loop_index=0

    def freeze(self):
        self.frozen=True

    def unfreeze(self):
        self.frozen=False

    def build_surfaces(self,color,scale_factor):
        self.surfaces=[]
        self.masks=[]
        rotations=[]
        if self.nrotations>1:
            rotation_interval=90.0/self.nrotations
            for k in range(self.nrotations):
                rotations.append(rotation_interval*k)
        for i in range(len(self.images)):
            surf=pygame.image.load(os.path.join(self.path,self.images[i])).convert_alpha()
            rect0=surf.get_rect(top=0,left=0)
            if color:
                fill(surf,color)
            if scale_factor:
                surf=pygame.transform.scale_by(surf,scale_factor)
            if self.angle0!=0:
                surf,rect=rot_center(surf,self.angle0,rect0.centerx,rect0.centery)
            self.masks.append([])
            self.surfaces.append([])
            for j in range(4):
                flip_x=(self.flip_x[i]+abs(((j+1)%2)-1))%2
                flip_y=(self.flip_y[i]+int(float(j)/2))%2
                surf_flip=pygame.transform.flip(surf,flip_x,flip_y)
                self.surfaces[i].append(surf_flip)
                self.masks[i].append(pygame.mask.from_surface(surf_flip))

    def read_sequence(self):
        if not self.sprite_name or not self.name:
            return False
        sequence_file=os.path.join(self.image_path,'sprites',self.sprite_name,'sequence.txt')
        if os.path.isfile(sequence_file)==0:
            print("Sequence file ",sequence_file," not found")
            print(self.image_path)
            return False
        f=open(sequence_file,'r')
        found=False
        for line in f:
            tag=line.split(":")
            if found and tag[0].strip()=='':
                break
            if tag[0].strip()=='':
                continue
            if tag[0]=='Name':
                namehere=tag[1].strip()
                if namehere==self.name:
                    found=True
                    continue
            tag[1]=genu.index_expand(tag[1])
            if tag[0]=='Sequence' and found:
                sequence=tag[1].split(',')
                self.images=[]
                for im in sequence:
                    self.images.append(im.strip()+'.png')
            if tag[0]=='Rotation' and found:
                sequence=tag[1].split(',')
                self.rotation=[]
                for rot in sequence:
                    self.rotation.append(float(rot))
            if tag[0]=='Offset_x' and found:
                sequence=tag[1].split(',')
                self.trans_x=[]
                for offset in sequence:
                    self.trans_x.append(float(offset))
            if tag[0]=='Offset_y' and found:
                sequence=tag[1].split(',')
                self.trans_y=[]
                for offset in sequence:
                    self.trans_y.append(float(offset))
            if tag[0]=='Flip_x' and found:
                sequence=tag[1].split(',')
                self.flip_x=[]
                for flip in sequence:
                    self.flip_x.append(int(flip))
            if tag[0]=='Flip_y' and found:
                sequence=tag[1].split(',')
                self.flip_y=[]
                for flip in sequence:
                    self.flip_y.append(int(flip))
        if not found:
            return False
        else:
            return True

def hold_boundary(sprite,boundaries):
    if sprite.rect.right>boundaries[2]:
        sprite.x=boundaries[2]-sprite.rect.width/2
    if sprite.rect.left<boundaries[0]:
        sprite.x=boundaries[0]+sprite.rect.width/2
    if sprite.rect.top<boundaries[1]:
        sprite.y=boundaries[1]+sprite.rect.height/2
    if sprite.rect.bottom>boundaries[3]:
        sprite.y=boundaries[3]-sprite.rect.height/2

def check_boundary(sprite,boundaries):
    if sprite.bounce[2]:
        if sprite.rect.right>boundaries[2]:
            sprite.speedx*=-1
            return True
    else:
        if sprite.rect.left>boundaries[2]:
            sprite.kill()
    if sprite.bounce[3]:
        if sprite.rect.bottom>boundaries[3]:
            sprite.speedy*=-1
            return True
    else:
        if sprite.rect.top>boundaries[3]:
            sprite.kill()
    if sprite.bounce[1]:
        if sprite.rect.top<boundaries[1]:
            sprite.speedy*=-1
            return True
    else:
        if sprite.rect.bottom<boundaries[1]:
            sprite.kill()
    if sprite.bounce[0]:
        if sprite.rect.left<boundaries[0]:
            sprite.speedx*=-1
            return True
    else:
        if sprite.rect.right<boundaries[0]:
            sprite.kill()
    return False

def bounce_sprite(sprite,collide_point):
    collide_angle=math.atan2(sprite.rect.height/2-collide_point[1],sprite.rect.width/2-collide_point[0])
    v=pygame.Vector2(sprite.speedx,sprite.speedy)
    v.rotate_rad_ip(-collide_angle)
    v.x*=-1
    v.rotate_rad_ip(collide_angle)
    sprite.speedx=v.x
    sprite.speedy=v.y

def bounce_gameobject(sprite,angle):
    v=sprite.velocity
    v.rotate_rad_ip(angle)
    v.x*=-1
    v.rotate_rad_ip(-angle)
    sprite.velocity=v


def average_collision_point(left,right):
    offset=(right.rect[0]-left.rect[0],right.rect[1]-left.rect[1])
    overlap=left.mask.overlap(right.mask,offset)
    if overlap:
        mask_overlap=left.mask.overlap_mask(right.mask,offset)
        return mask_overlap.centroid()
    return None

def decide_move(sprite_move,sprites_avoid,movestep):
    prect=[sprite_move.rect.left+movestep[0],sprite_move.rect.right+movestep[0],sprite_move.rect.top+movestep[1],sprite_move.rect.bottom+movestep[1]]
    for sprite_avoid in sprites_avoid:
        erect=sprite_avoid.rect
        if erect.left<=prect[1] and erect.right>=prect[0] and erect.top<=prect[3] and erect.bottom>=prect[2]:
            return False
    return True

def collide_mask_check(sprite1,sprite2):
    if pygame.sprite.collide_rect(sprite1,sprite2):
        collided=pygame.sprite.collide_mask(sprite1,sprite2)
        return collided or []
    return []

def collide_check_all(sprite1,sprites):
    collided=[]
    do_reset=False
    if sprite1.check_collide_counter():
        for sprite2 in sprites:
            if sprite2.check_collide_counter() and collide_mask_check(sprite1,sprite2):
                collided+=[sprite2]
                sprite2.reset_collide()
                sprite1.reset_collide()
    return collided

def collide_avpts_all(sprite1,sprites):
    collided=[]
    avpts=[]
    if sprite1.check_collide_counter():
        for sprite2 in sprites:
            if sprite2.check_collide_counter():
                avpt=average_collision_point(sprite1,sprite2)
                if avpt:
                    collided+=[sprite2]
                    avpts+=[avpt]
    return collided,avpts


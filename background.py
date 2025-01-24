#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import pygame
import gameconstants as gc
import random
import physics
import math
import spritefunctions as sf

class Boundary(pygame.Rect):
    def __init__(self,rect,bounce=[False,False,False,False],wrap=[False,False,False,False],stop=[False,False,False,False]):
        super(Boundary,self).__init__(rect)
        self.bounce=bounce
        self.stop=stop
        self.wrap=wrap

class Border(pygame.sprite.Sprite):
    def __init__(self,thick=2,color=(255,255,255),back_color=(0,0,0)):
        super(Border,self).__init__()
        left=thick/2
        top=thick/2
        right=gc.gc['SCREEN_WIDTH']-thick/2
        bottom=gc.gc['SCREEN_HEIGHT']-thick/2
        self.surf=pygame.Surface((gc.gc['SCREEN_WIDTH'],gc.gc['SCREEN_HEIGHT']))
        self.surf.fill(back_color)
        self.surf.set_colorkey(back_color)
        pygame.draw.line(self.surf,color,(left,1),(left,gc.gc['SCREEN_HEIGHT']-1),width=thick)
        pygame.draw.line(self.surf,color,(1,top),(gc.gc['SCREEN_WIDTH']-1,top),width=thick)
        pygame.draw.line(self.surf,color,(right,1),(right,gc.gc['SCREEN_HEIGHT']-1),width=thick)
        pygame.draw.line(self.surf,color,(gc.gc['SCREEN_WIDTH']-1,bottom),(1,bottom),width=thick)
        self.rect = self.surf.get_rect(left=gc.gc['LEFT'],top=gc.gc['TOP'])

class DashedBoundary(pygame.sprite.Sprite):
    def __init__(self,x_position,thick=2,n_dashes=30):
        super(DashedBoundary,self).__init__()
        self.surf=pygame.Surface((thick,gc.gc['SCREEN_HEIGHT']))
        self.surf.set_colorkey(gc.gc['SCREEN_COLOR'])
        y_interval=round(gc.gc['SCREEN_HEIGHT']/n_dashes)
        for y in range(gc.gc['TOP'],gc.gc['FULL_HEIGHT'],y_interval):
            pygame.draw.line(self.surf,(255,255,255),(thick/2,y),(thick/2,y+y_interval/2),width=thick)
        self.rect = self.surf.get_rect(
            center=(
                x_position,
                gc.gc['FULL_HEIGHT']-gc.gc['SCREEN_HEIGHT']/2,
            )
        )


class Marker(pygame.sprite.Sprite):
    def __init__(self,position,length,thick=4,color=(255,255,255),direction='vertical'):
        super(Marker,self).__init__()
        if direction=='vertical':
            self.dimen=(thick,length)
            self.wrap_points=(-self.dimen[1],gc.gc['FULL_HEIGHT']+self.dimen[1])
        else:
            self.dimen=(length,thick)
            self.wrap_points=(-self.dimen[0],gc.gc['FULL_WIDTH']+self.dimen[0])
        self.surf=pygame.Surface(self.dimen)
        self.surf.set_colorkey(gc.gc['SCREEN_COLOR'])
        self.direction=direction
        self.surf.fill(color)
        self.x=position[0]
        self.y=position[1]
        self.rect = self.surf.get_rect(
            center=(
                position[0],
                position[1],
            )
        )

    def update(self,speed):
        if self.direction=='vertical':
            self.y+=speed
        else:
            self.x+=speed
        self.rect.move_ip(self.x-self.rect.centerx,self.y-self.rect.centery)
        # Do a vertical screen wrap
        if self.direction=='vertical':
            if self.rect.centery>=self.wrap_points[1]:
                self.y=self.wrap_points[0]+(self.rect.centery-self.wrap_points[1])
            if self.rect.centery<=self.wrap_points[0]:
                self.y=self.wrap_points[1]+(self.rect.centery-self.wrap_points[0])
        else:
            if self.rect.centerx>=self.wrap_points[1]:
                self.x=self.wrap_points[0]+(self.rect.centerx-self.wrap_points[1])
            if self.rect.centerx<=self.wrap_points[0]:
                self.x=self.wrap_points[1]+(self.rect.centerx-self.wrap_points[0])

class SolidBackground(pygame.sprite.Sprite):
    def __init__(self,position,dimen,color):
        super(SolidBackground,self).__init__()
        self.surf=pygame.Surface(dimen)
        self.surf.fill(color)
        self.rect=self.surf.get_rect(
            center=(
                position[0],
                position[1],
            )
        )

class ObjectFill(pygame.sprite.Sprite):
    def __init__(self,position,dimen,color):
        super(ObjectFill,self).__init__()
        self.surf=pygame.Surface(dimen)
        self.mask=pygame.mask.from_surface(self.surf)
        self.x=position[0]
        self.y=position[1]
        self.surf.fill(color)
        self.rect=self.surf.get_rect(
            center=(
                self.x,
                self.y,
            )
        )

class MarkerLine():
    def __init__(self,position,length,width,number,color,direction='vertical'):
        marker_separation=length/number+1
        marker_length=marker_separation/2
        self.markers=pygame.sprite.Group()
        for i in range(number+1):
            position_along=i*marker_separation
            if direction=='vertical':
                marker_i=Marker((position,position_along),marker_length,direction='vertical',color=color)
            else:
                marker_i=Marker((position_along,position),marker_length,direction='horizontal',color=color)
            self.markers.add(marker_i)

    def update(self,speed):
        for marker_i in self.markers:
            marker_i.update(speed)

    def blit(self,screen):
        for marker_i in self.markers:
            screen.blit(marker_i.surf,marker_i.rect)

class Starfield(pygame.Surface):
    def __init__(self,dimen,nstars=50,period=100,color=(255,255,255)):
        super(Starfield,self).__init__(dimen)
        self.dimen=dimen
        self.nstars=nstars
        self.period=period
        self.color=color
        self.init_starfield()
        self.counter=0

    def update(self):
        field=pygame.surfarray.pixels2d(self)
        for i in range(len(self.x)):
            bright=round((math.sin(2*math.pi*self.counter/self.period+self.phase[i])**2*0.25+0.75)*self.bright[i])
            field[self.y[i],self.x[i]]=self.map_rgb(bright,bright,bright)
        self.counter+=1

    def init_starfield(self):
        x=[]
        y=[]
        bright=[]
        phase=[]
        for i in range(self.nstars):
            x.append(random.randrange(0,self.dimen[1]))
            y.append(random.randrange(0,self.dimen[0]))
            bright.append(random.randrange(0,256))
            phase.append(random.random()*2*math.pi)
        self.x=x
        self.y=y
        self.bright=bright
        self.phase=phase

class ParticleExplosion(pygame.Surface):
    def __init__(self,dimen=(500,500),nparticles=300,init_speed=1,decel=0.1,color=(255,255,255),lifetime=300):
        super(ParticleExplosion,self).__init__(dimen)
        self.center=(round(dimen[0]/2),round(dimen[1]/2))
        self.nparticles=nparticles
        self.init_speed=init_speed
        self.decel=decel
        self.lifetime=lifetime
        self.count=0
        self.init_particles()
        self.color=color
        self.finished=False
    
    def init_particles(self):
        self.particles=[]
        for i in range(self.nparticles):
            angle=random.random()*2*math.pi
            speed=self.init_speed*random.random()
            self.particles.append(physics.Particle(self.center,angle=angle,speed=speed))

    def update(self):
        if self.count<=self.lifetime:
            field=pygame.surfarray.pixels2d(self)
            field[:,:]=self.map_rgb(0,0,0,0)
            if self.count<self.lifetime:
                fade_factor=1-self.count/self.lifetime
                for particle in self.particles:
                    bright=[round(self.color[0]*fade_factor),
                            round(self.color[1]*fade_factor),
                            round(self.color[2]*fade_factor)]
                    particle.update()
                    x=round(particle.position.y)
                    y=round(particle.position.x)
                    if x<self.center[0]*2 and y<self.center[1]*2 and x>=0 and y>=0:
                        field[y,x]=self.map_rgb(bright[0],bright[1],bright[2],255)
        else:
            self.finished=True
        self.count+=1

class Tracer(pygame.Surface):
    def __init__(self,surface,sprites=[],color=(255,0,0,255),width=1):
        dimen=surface.get_size()
        self.dimen=dimen
        super(Tracer,self).__init__(dimen)
        self.fill((0,0,0))
        self.set_colorkey((0,0,0))
        self.sprites=sprites
        self.width=width
        self.color=color

    def add(self,sprites):
        self.sprites.append(sprites)

    def draw(self):
        surfarr=pygame.surfarray.pixels2d(self)
        for sprite in self.sprites:
            position=sprite.rect.center
            if position[0]>=self.width and position[1]>self.width and \
                    position[0]<self.dimen[0]-self.width and \
                    position[1]<self.dimen[1]-self.width:
                surfarr[position[0]-self.width:position[0]+self.width,
                        position[1]-self.width:position[1]+self.width]=self.map_rgb(self.color)

class Life_Counter():
    def __init__(self,position,init_lives,direction,life_size,separation=None,max_lives=None,color=(255,255,255),file=None):
        self.current_count=init_lives
        self.direction=direction
        self.separation=separation if separation else life_size[0]*1.5
        self.position=position
        self.max_lives=max_lives
        self.color=color
        self.life_size=life_size
        self.life_markers=[]
        for i in range(init_lives):
            life_marker=self.get_marker(i)
            self.life_markers.append(life_marker)

    def get_marker(self,count):
        if self.direction=='right':
            x_pos=self.position[0]+self.life_size[0]/2+self.separation*count
            y_pos=self.position[1]+self.life_size[1]/2
        elif self.direction=='left':
            x_pos=self.position[0]-self.life_size[0]/2-self.separation*count
            y_pos=self.position[1]+self.life_size[1]/2
        elif self.direction=='down':
            x_pos=self.position[0]+self.life_size[0]/2
            y_pos=self.position[1]+self.life_size[1]/2+self.separation*count
        else:
            x_pos=self.position[0]+self.life_size[0]/2
            y_pos=self.position[1]-self.life_size[1]/2-self.separation*count
        return ObjectFill((x_pos,y_pos),self.life_size,color=self.color)

    def increment_counter(self):
        if not self.max_lives or self.current_count<self.max_lives:
            new_marker=self.get_marker(self.current_count)
            self.life_markers.append(new_marker)
            self.current_count+=1

    def decrement_counter(self):
        if self.current_count>0:
            self.current_count-=1
            removed_life=self.life_markers.pop()
            
    def blit(self,screen):
        for marker_i in self.life_markers:
            screen.blit(marker_i.surf,marker_i.rect)

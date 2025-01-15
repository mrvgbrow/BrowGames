#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import pygame
import gameconstants as gc
import spritefunctions as sf

class Boundary(pygame.Rect):
    def __init__(self,rect,bounce=[False,False,False,False],wrap=[False,False,False,False],stop=[False,False,False,False]):
        super(Boundary,self).__init__(rect)
        self.bounce=bounce
        self.stop=stop
        self.wrap=wrap

class Border(pygame.sprite.Sprite):
    def __init__(self,thick=2):
        super(Border,self).__init__()
        self.surf=pygame.Surface((gc.gc['SCREEN_WIDTH'],gc.gc['SCREEN_HEIGHT']))
        self.surf.set_colorkey(gc.gc['SCREEN_COLOR'])
        pygame.draw.line(self.surf,(255,255,255),(0,0),(0,gc.gc['SCREEN_HEIGHT']-thick),width=thick)
        pygame.draw.line(self.surf,(255,255,255),(0,0),(gc.gc['SCREEN_WIDTH']-thick,0),width=thick)
        pygame.draw.line(self.surf,(255,255,255),(gc.gc['SCREEN_WIDTH']-thick,0),(gc.gc['SCREEN_WIDTH']-thick,gc.gc['SCREEN_HEIGHT']-thick),width=thick)
        pygame.draw.line(self.surf,(255,255,255),(gc.gc['SCREEN_WIDTH']-thick,gc.gc['SCREEN_HEIGHT']-thick),(0,gc.gc['SCREEN_HEIGHT']-thick),width=thick)
        self.rect = self.surf.get_rect(
            center=(
                gc.gc['LEFT']+gc.gc['SCREEN_WIDTH']/2,
                gc.gc['TOP']+gc.gc['SCREEN_HEIGHT']/2,
            )
        )

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

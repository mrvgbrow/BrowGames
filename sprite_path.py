import pygame
import random
import numpy as np
import math

class sprite_path:
    def __init__(self,path,sizes=[],angle1=[],angle2=[],angle3=[],flipx=[],flipy=[],opacity=[],filename='None',animframe=[],ties=[],bezier=[],shake=[]):
        self.path=path
        if filename != 'None':
            self.path,self.animframe=self.read_path(filename)
        self.init_blank_pathvals(len(self.path))
        if len(sizes)==len(self.path):
            self.sizes=sizes
        if len(angle1)==len(self.path):
            self.angle1=angle1
        if len(angle2)==len(self.path):
            self.angle2=angle2
        if len(angle3)==len(self.path):
            self.angle3=angle3
        if len(flipx)==len(self.path):
            self.flipx=flipx
        if len(flipy)==len(self.path):
            self.flipy=flipy
        if len(opacity)==len(self.path):
            self.opacity=opacity
        if len(ties)==len(self.path):
            self.ties=ties
        if len(bezier)==len(self.path):
            self.bezier=bezier
        if len(shake)==len(self.path):
            self.shake=shake
        if len(animframe)==len(self.path):
            self.animframe=animframe

    def init_blank_pathvals(self,length):
        self.sizes=[(-999,-999)]*length
        self.angle1=[-999]*length
        self.angle2=[-999]*length
        self.angle3=[-999]*length
        self.flipx=[-999]*length
        self.flipy=[-999]*length
        self.opacity=[-999]*length
        self.animframe=[-999]*length
        self.ties=[-999]*length
        self.bezier=[-999]*length
        self.shake=[-999]*length

    def fill_nones(self):
        for i in range(len(self.path)):
            if self.path[i][0]==None:
                self.sizes[i]=(None,None)
                self.angle1[i]=None
                self.angle2[i]=None
                self.angle3[i]=None
                self.flipx[i]=None
                self.flipy[i]=None
                self.opacity[i]=None
                self.animframe[i]=None
                self.accel[i]=None
                self.drops[i]=None
                self.ties[i]=None
                self.bezier[i]=None
                self.shake[i]=None

    def discrete_rots(self,nrots):
        for i in range(len(self.path)):
            angle=self.angle1[i]
            if angle!=-999:
                self.angle1[i]=round(angle*nrots/360)*360/nrots

    def add_shake(self):
        for i in range(len(self.shake)):
            if self.shake[i]!= None and self.shake[i]>0:
                amplitude=self.shake[i]
                offset=random.randint(0,amplitude*2)-amplitude
                offset2=random.randint(0,amplitude*2)-amplitude
                self.path[i]=(self.path[i][0]+offset,self.path[i][1]+offset2)

    def fill_bezier(self):
        bez=np.array(self.bezier)
        indices=np.nonzero(bez==3)
        for i in range(0,len(indices[0]),3):
            point1=self.path[indices[0][i]]
            point2=self.path[indices[0][i+1]]
            point3=self.path[indices[0][i+2]]
            nodes1=np.asfortranarray([[point1[0],point2[0],point3[0]],[point1[1],point2[1],point3[1]]])
            curve=bezier.Curve(nodes1,degree=2)
            s0=curve.locate(np.array([[point1[0]],[point1[1]]]))
            s1=curve.locate(np.array([[point3[0]],[point3[1]]]))
            length=indices[0][i+2]-indices[0][i]
            for j in range(indices[0][i],indices[0][i+2]+1):
                point=curve.evaluate(s0+(j-indices[0][i])/length*(s1-s0))
                self.path[j]=(point[0][0],point[1][0])

    def reverse(self,dims='both'):
        if dims=='both':
            for i in range(len(self.path)):
                if self.path[i][0]!=None:
                    self.path[i]=(2*self.path[0][0]-self.path[i][0],2*self.path[0][1]-self.path[i][1])
                    self.flipx[i]=(self.flipx[i]+1)%2
                    self.flipy[i]=(self.flipy[i]+1)%2
        if dims=='x':
            for i in range(len(self.path)):
                if self.path[i][0]!=None:
                    self.path[i]=(2*self.path[0][0]-self.path[i][0],self.path[i][1])
                    self.flipx[i]=(self.flipx[i]+1)%2
        if dims=='y':
            for i in range(len(self.path)):
                if self.path[i][0]!=None:
                    self.path[i]=(self.path[i][0],2*self.path[0][1]-self.path[i][1])
                    self.flipy[i]=(self.flipy[i]+1)%2

    def find_minmax(self):
        minx=min(self.path,key=lambda t:t[0])[0]
        maxx=max(self.path,key=lambda t:t[0])[0]
        miny=min(self.path,key=lambda t:t[1])[1]
        maxy=max(self.path,key=lambda t:t[1])[1]
        return minx,maxx,miny,maxy

    def copy_path_element(self,i,j):
        self.path[i]=self.path[j]
        self.angle1[i]=self.angle1[j]
        self.angle2[i]=self.angle2[j]
        self.angle3[i]=self.angle3[j]
        self.flipx[i]=self.flipx[j]
        self.flipy[i]=self.flipy[j]
        self.sizes[i]=self.sizes[j]
        self.opacity[i]=self.opacity[j]
        self.animframe[i]=self.animframe[j]
        self.accel[i]=self.accel[j]
        self.drops[i]=self.drops[j]
        self.ties[i]=self.ties[j]
        self.bezier[i]=self.bezier[j]

    def remove_path_element(self,i):
        self.path.pop(i)
        self.angle1.pop(i)
        self.angle2.pop(i)
        self.angle3.pop(i)
        self.flipx.pop(i)
        self.flipy.pop(i)
        self.opacity.pop(i)
        self.sizes.pop(i)
        self.animframe.pop(i)
        self.accel.pop(i)
        self.drops.pop(i)
        self.ties.pop(i)
        self.bezier.pop(i)
        self.shake.pop(i)

    def append_path_element(self,j):
        self.path.append(self.path[j])
        self.angle1.append(self.angle1[j])
        self.angle2.append(self.angle2[j])
        self.angle3.append(self.angle3[j])
        self.flipx.append(self.flipx[j])
        self.flipy.append(self.flipy[j])
        self.sizes.append(self.sizes[j])
        self.opacity.append(self.opacity[j])
        self.animframe.append(self.animframe[j])
        self.accel.append(self.accel[j])
        self.drops.append(self.drops[j])
        self.ties.append(self.ties[j])
        self.bezier.append(self.bezier[j])
        self.shake.append(self.shake[j])

    def set_element_none(self,j):
        self.path[j]=(None,None)
        self.angle1[j]=None
        self.angle2[j]=None
        self.angle3[j]=None
        self.flipx[j]=None
        self.flipy[j]=None
        self.sizes[j]=(None,None)
        self.opacity[j]=None
        self.animframe[j]=None
        self.accel[j]=None
        self.drops[j]=None
        self.ties[j]=None
        self.bezier[j]=None
        self.shake[j]=None

    def extend_path(self,length):
        j=len(self.path)-1
        for i in range(j+1,length):
            self.append_path_element(j)
        self.compute_center()

    def flip(self,flag_x,flag_y):
        if flag_x==1:
            for i in range(len(self.path)):
                if self.path[i][0]!=None:
                    self.path[i]=(2*self.center[0]-self.path[i][0],self.path[i][1])
        if flag_y==1:
            for i in range(len(self.path)):
                if self.path[i][0]!=None:
                    self.path[i]=(self.path[i][0],2*self.center[1]-self.path[i][1])

    def compute_center(self):
        meanx=0
        meany=0
        countx=0
        county=0
        for i in range(len(self.path)):
            if self.path[i][0]!=-999 and self.path[i][0]!=None:
                meanx+=self.path[i][0]
                meany+=self.path[i][1]
                countx+=1
                county+=1
        if countx>0 and county>0:
            self.center=(meanx/countx,meany/county)
        else:
            self.center=(None,None)

    def scale_to_box(self,box):
        minx,maxx,miny,maxy=self.find_minmax()
        dx=maxx-minx
        dy=maxy-miny
        if maxx-minx>0:
            xscale=(box[1]-box[0])/(maxx-minx)
        else:
            xscale=1.0
        if maxy-miny>0:
            yscale=(box[3]-box[2])/(maxy-miny)
        else:
            yscale=1.0
        for i in range(len(self.path)):
            self.path[i]=(box[0]+(self.path[i][0]-minx)*xscale,box[2]+(self.path[i][1]-miny)*yscale)
        self.compute_center()

    def scale_and_loop(self,box,images,resampling=1,loop=1):
        self.scale_to_box(box)
        init_length=len(self.path)
        if resampling!=1:
            self.resample_path(resampling)
        self.extend_path(len(images))
        if loop==1:
            self.loop_path(int((init_length-1)*resampling))
        else:
            for i in range(init_length,len(self.path)):
                self.set_element_none(i)
        self.compute_center()

    def shift_path(self,nframes):
        pathlen=len(self.path)
        for i in range(pathlen):
            j=(i+pathlen-nframes)%pathlen
            self.append_path_element(j)
        for i in range(pathlen):
            self.remove_path_element(0)

    def determine_angles(self,ref_angle=0,scale=1):
        if self.path[1][0]!=None and self.path[0][0]!=None:
            self.angle1[0]=math.atan2((self.path[1][0]-self.path[0][0]),(self.path[1][1]-self.path[0][1]))*180/math.pi+ref_angle
        else:
            self.angle1[0]=None
        for i in range(1,len(self.path)):
            imin=max(0,i-scale)
            imax=min(len(self.path)-1,i+scale)
            if self.path[imax][0]!=None and self.path[imin][0]!=None:
                self.angle1[i]=math.atan2((self.path[imax][0]-self.path[imin][0]),(self.path[imax][1]-self.path[imin][1]))*180/math.pi+ref_angle
            else:
                self.angle1[i]=None
    
    def adjust_path(self,direction,amount):
        if direction=='-y':
            for i in range(len(self.path)):
                self.path[i]=(self.path[i][0],self.path[i][1]-amount)
        if direction=='+y':
            for i in range(len(self.path)):
                self.path[i]=(self.path[i][0],self.path[i][1]+amount)
        if direction=='+x':
            for i in range(len(self.path)):
                self.path[i]=(self.path[i][0]+amount,self.path[i][1])
        if direction=='-x':
            for i in range(len(self.path)):
                self.path[i]=(self.path[i][0]-amount,self.path[i][1])
        self.compute_center()
    
    def path_length(self,ind1,ind2):
        if self.path[ind1][0]!=None and self.path[ind2][0]!=None:
            length=(math.sqrt((self.path[ind1][0]-self.path[ind2][0])**2+(self.path[ind1][1]-self.path[ind2][1])**2))
        else:
            length=0
        return length

    def scale(self,factor,center=None):
        if center==None:
            try: self.center
            except: center=(0,0)
        for i in range(len(self.path)):
            if self.path[i][0]!=None and self.path[i][0]!=-999:
                self.path[i]=((self.path[i][0]-center[0])*factor+center[0],(self.path[i][1]-center[1])*factor+center[1])

    def fade_on_path(self,fade_frames,fade_amount=0.8):
        fade_interval=fade_amount/fade_frames
        for i in range(len(self.path)):
            self.opacity[i]=1-i*fade_interval
            if self.opacity[i]<1-fade_amount:
                self.opacity[i]=1-fade_amount

    def invert_path(self):
        pathlen=len(self.path)
        for i in range(pathlen):
            self.append_path_element(pathlen-i-1)
        for i in range(pathlen):
            self.remove_path_element(0)

    def resample_path(self,factor):
        if factor>1:
            self.extend_path(int(factor*len(self.path)))
            for i in range(len(self.path)-1,0,-1):
                j=int(i/factor)
                self.copy_path_element(i,j)
        else:
            factor2=round(1/factor)
            i=0
            while i<len(self.path):
                self.remove_path_element(i)
                i+=1


    def loop_path(self,index):
        for i in range(index,len(self.path)):
            j=i%index
            self.copy_path_element(i,j)


    def write_path(self,outfile):
        f=open(outfile,'w')
        for i in range(len(self.path)):
            f.write(str(self.path[i][0])+","+str(self.path[i][1])+","+str(self.animframe[i])+"\n")
        f.close()

    def fill_random(self,box_points):
        rx=random.randint(box_points[0],box_points[1])
        ry=random.randint(box_points[2],box_points[3])
        for i in range(len(self.path)):
            self.path[i][1]=ry
            self.path[i][0]=rx
        self.compute_center()

    def read_path(self,filename):
        f=open(filename,'r')
        f1=f.readlines()
        f1=[line.strip() for line in f1]
        f1=[line.strip('\x00') for line in f1]
        i=0
        path=[]
        animframes=[]
        for line in f1:
            (x,y,animframe)=line.split(',')
            path.append((float(x),float(y)))
            animframes.append(int(animframe))
            i+=1
        f.close()
        self.compute_center()
        return path,animframes

#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

from sys import getsizeof, stderr
from itertools import chain
from collections import deque
import glob
import os
import sys
import re
import math
import random
import numpy as np
try:
    from reprlib import repr
except ImportError:
    pass

def position_in_circle(radius,angle,center):
    circlepos=(math.cos(angle)*radius,math.sin(angle)*radius)
    abspos=(circlepos[0]+center[0],circlepos[1]+center[1])
    return abspos

def gaussian_function(norm_distance):
    return 1.0/math.sqrt(2*math.pi)*math.exp(-1.0/2.0*norm_distance**2)

def cart_to_polar(xv,yv,maxrad=1,minrad=0,axis=0,phase=0):
    theta_v=math.pi*2*xv/np.max(xv)
    r_v=yv/np.max(yv)*maxrad+minrad
    xnew_v=r_v*np.cos(theta_v+phase)
    ynew_v=r_v*np.sin(theta_v+phase)
    return((xnew_v,ynew_v))

def sample_line(pos1,pos2,nsample):
    inc_x=(pos2[0]-pos1[0])/(nsample-1)
    inc_y=(pos2[1]-pos1[1])/(nsample-1)
    pos_all=[pos1]
    for i in range(nsample-2):
        pos_all.append((int(pos1[0]+(i+1)*inc_x),int(pos1[1]+(i+1)*inc_y)))
    pos_all.append(pos2)
    return pos_all

def sample_quadratic(pos1,pos2,nsample,sign=1):
    samples=np.linspace(0,1,num=nsample)
    if sign==1:
        x=np.multiply(samples,samples*((pos2[0]-pos1[0])))+pos1[0]
        y=np.multiply(samples,samples*((pos2[1]-pos1[1])))+pos1[1]
    else:
        x=pos2[0]-np.multiply(samples,samples*((pos2[0]-pos1[0])))
        y=pos2[1]-np.multiply(samples,samples*((pos2[1]-pos1[1])))
        x=np.flip(x)
        y=np.flip(y)
    return x,y

def rotate_points(origin,points,angle):

    ox,oy=origin
    points_new=[]
    for i in range(len(points)):
        qx=int(ox+math.cos(angle)*(points[i][0]-ox)-math.sin(angle)*(points[i][1]-oy))
        qy=int(oy+math.sin(angle)*(points[i][0]-ox)+math.cos(angle)*(points[i][1]-oy))
        points_new.append((qx,qy))
    return points_new

def make_reverse_dict(d):
    inv_dict={v: k for k, v in d.items()}
    return inv_dict

def make_rotation_matrix(a1,a2,a3):
    a1*=math.pi/180
    a2*=math.pi/180
    a3*=math.pi/180
    rot=np.matrix([[math.cos(a1)*math.cos(a2), \
            math.cos(a1)*math.sin(a2)*math.sin(a3)-math.sin(a1)*math.cos(a3), \
            math.cos(a1)*math.sin(a2)*math.cos(a3)+math.sin(a1)*math.sin(a3)], \
            [math.sin(a1)*math.cos(a2), \
            math.sin(a1)*math.sin(a2)*math.sin(a3)+math.cos(a1)*math.cos(a3), \
            math.sin(a1)*math.sin(a2)*math.cos(a3)-math.cos(a1)*math.sin(a3)], \
            [-math.sin(a2),math.cos(a2)*math.sin(a3),math.cos(a2)*math.cos(a3)]])
    return rot

def match_in_list(list0,regex_string):
    r=re.compile(regex_string)
    matchlist=list(filter(r.match,list0))
    if len(matchlist)==0:
        return ''
    else:
        return matchlist[0]

def get_format_val(list0,regex_string,vtype='int'):
    form_args=[]
    r=re.compile(regex_string)
    matchlist=list(filter(r.match,list0))
    if len(matchlist)==0:
        return '',form_args
    else:
        form_args=matchlist[0].split('#')
    if vtype=='int':
        val=int((form_args[0])[1:])
    if vtype=='float':
        val=float((form_args[0])[1:])
    if vtype=='str':
        val=(form_args[0])[1:]
    return val,form_args

def get_camera_matrix(fx,fy,cx,cy):
    camera_matrix=np.matrix([[fx,0,cx],[0,fy,cy],[0,0,1]])
    return camera_matrix

def total_size(o, handlers={}, verbose=False):
    """ Returns the approximate memory footprint an object and all of its contents.

    Automatically finds the contents of the following builtin containers and
    their subclasses:  tuple, list, deque, dict, set and frozenset.
    To search other containers, add handlers to iterate over their contents:

        handlers = {SomeContainerClass: iter,
                    OtherContainerClass: OtherContainerClass.get_elements}

    """
    dict_handler = lambda d: chain.from_iterable(d.items())
    all_handlers = {tuple: iter,
                    list: iter,
                    deque: iter,
                    dict: dict_handler,
                    set: iter,
                    frozenset: iter,
                   }
    all_handlers.update(handlers)     # user handlers take precedence
    seen = set()                      # track which object id's have already been seen
    default_size = getsizeof(0)       # estimate sizeof object without __sizeof__

    def sizeof(o):
        if id(o) in seen:       # do not double count the same object
            return 0
        seen.add(id(o))
        s = getsizeof(o, default_size)

        if verbose:
            print(s, type(o), repr(o), file=stderr)

        for typ, handler in all_handlers.items():
            if isinstance(o, typ):
                s += sum(map(sizeof, handler(o)))
                break
        return s

    return sizeof(o)

def index_expand(index_string):
    underscore_splits=index_string.split('_')
    if len(underscore_splits)>1:
        for i in range(0,len(underscore_splits)-1):
            num1=int((re.findall(r"\d+$",underscore_splits[i]))[0])
            num2=int((re.findall(r"^\d+",underscore_splits[i+1]))[0])
            inc_splits=underscore_splits[i+1].split('i')
            if len(inc_splits)>1:
                step=int((re.findall(r"^\d+",inc_splits[1]))[0])
                num2=int(inc_splits[0])
                stepstr='i'+str(step)
            else:
                step=1
                stepstr=''
            if num1>num2:
                new_string=str(num1)
                r1=num1-1
                r2=num2-1
                step=-step
            else:
                new_string=str(num1)
                r1=num1+1
                r2=num2+1
            for j in range(r1,r2,step):
                new_string+=','+str(j)
            index_string=index_string.replace(str(num1)+'_'+str(num2)+stepstr,new_string,1)
    x_splits=index_string.split('x')
    if len(x_splits)>1:
        for i in range(0,len(x_splits)-1):
            check_paren=re.search('\(',x_splits[i])
            if check_paren is not None:
                num1=extract_inside(x_splits[i])
                num1_original='('+num1+')'
            else:
                num1=int((re.findall(r"\d+$",x_splits[i]))[0])
                num1_original=num1
            num2=int((re.findall(r"^\d+",x_splits[i+1]))[0])
            new_string=str(num1)
            for j in range(num2-1):
                new_string+=','+str(num1)
            index_string=index_string.replace(str(num1_original)+'x'+str(num2),new_string,1)
    return index_string

def bounce_boundary(pos,bounds,v_in):
    newpos=np.array(pos)
    v=np.array(v_in)
    if pos[0]>bounds[1]:
        newpos[0]=2*bounds[1]-pos[0]
        v[0]=-v_in[0]
    if pos[1]>bounds[3]:
        newpos[1]=2*bounds[3]-pos[1]
        v[1]=-v_in[1]
    if pos[0]<bounds[0]:
        newpos[0]=2*bounds[0]-pos[0]
        v[0]=-v_in[0]
    if pos[1]<bounds[2]:
        newpos[1]=2*bounds[2]-pos[1]
        v[1]=-v_in[1]
    return newpos,v

def wrap_boundary(pos,bounds,sprite_size=(0,0)):
    newpos=np.array(pos)
    if pos[0]>bounds[1]+sprite_size[0]/3:
        newpos[0]=bounds[0]+pos[0]-bounds[1]-sprite_size[0]/2
    if pos[1]>bounds[3]+sprite_size[1]/3:
        newpos[1]=bounds[2]+pos[1]-bounds[3]-sprite_size[1]/2
    if pos[0]<bounds[0]-sprite_size[0]/3:
        newpos[0]=bounds[1]-(bounds[0]-pos[0])+sprite_size[0]/2
    if pos[1]<bounds[2]-sprite_size[1]/3:
        newpos[1]=bounds[3]-(bounds[2]-pos[1])+sprite_size[1]/2
    return newpos

def move_variate(v,dx,f=1):
    val=random.randint(0,int(dx/v/f))
    return val==0

def check_arg(args,element,default,valtype='None'):
    if len(args)>element:
        val=args[element]
    else:
        val=default
    if valtype=='int':
        val=int(val)
    if valtype=='float':
        val=float(val)
    return val

def tuple_distance(pos1,pos2):
    return (math.sqrt((pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2))

def extract_inside(string,char='paren'):
    if char=='paren':
        matches=re.search('\(([^)]+)\)',string)
    if matches is not None:
        return matches.group(1)

def expand_formatted_input(string,objects_path,append=""):
    objects=string.split()
    objects_expand=[]
    i=0
    for object in objects:
        object_str=object.split('!')
        object2=object_str[0]
        if object2=='blank':
            objects_expand.append(object+"!"+append)
        object_counts=object.split('&')
        tail='!'.join(tuple(object_str[1:]))
        if len(object_counts)>1:
            count=int((object_counts[1].split('!'))[0])
            for j in range(count-1):
                objects_expand.append(object_counts[0]+'!'+tail+"!"+append)
            object2=object_counts[0]
        objarr=glob.glob(objects_path+object2)
        for obj in objarr:
            objstr=os.path.basename(obj)+'!'+tail+"!"+append
            objects_expand.append(objstr)
        i+=1
    return objects_expand

def bezier_from_points(points,t_arr):
    degree=len(points)
    j=0
    B=[]
    for t in t_arr:
        Bsum=[0,0]
        i=0
        for p in points:
            coeff=binom(degree,i)*t**i*(1-t)**(n-i)
            Bsum[0]+=coeff*p[0]
            Bsum[1]+=coeff*p[1]
            i+=1
        B.append(tuple(Bsum))
        j+=1
    return B

def binom(n,k):
    return math.factorial(n) // math.factorial(k) // math.factorial(n-k)

def randsign():
    return int(np.sign(random.random()-0.5))

def parse_box(box_string):
    coords=box_string.split(',')
    xlims=coords[0].split(':')
    ylims=coords[1].split(':')
    return [[int(xlims[0]),int(ylims[0])],[int(xlims[1]),int(ylims[1])]]

def replace_var_line(line,varnum,val):
    return line.replace('$'+str(varnum),str(val))

def parse_range(word):
    if (word[0]=='l'):
        word='np.linspace('+word[1:]+')'
    if (word[0]=='r'):
        word='range('+word[1:]+')'
    if (word[0]=='R'):
        word='genu.getrandoms('+word[1:]+')'
    if (word[0]=='i'):
        word='genu.getrandints('+word[1:]+')'
    return word

def getrandoms(N,norm=1):
    randoms=[]
    for i in range(N):
        randoms.append(random.random())
    return randoms

def getrandints(N,end):
    randints=[]
    for i in range(N):
        randints.append(random.randint(1,end))
    return randints

def angle_to_coords(angle,amplitude):
    return amplitude*math.cos(angle),amplitude*math.sin(angle)

def coords_to_angle(coordx,coordy):
    return math.atan2(coordy,coordx),(coordx*coordx+coordy*coordy)**0.5

def find_intercept(speedx,speedy,x,y,x0):
    return y+(x0-x)*speedy/speedx

def sign(value):
    if value<0:
        return -1
    else:
        return 1

def randsign():
    return 1 if random.random() <0.5 else -1

def check_array_coords(array,coords):
    for idx,dim in enumerate(array.shape):
        if coords[idx]<0 or coords[idx]>=dim:
            return False
    return True

def angle_to_atan2_range(angle):
    return math.atan2(math.sin(angle),math.cos(angle))


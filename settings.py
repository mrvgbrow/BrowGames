#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import glob
import os
__location__=os.path.realpath(os.path.join(os.getcwd(),os.path.dirname(__file__)))

MOUSE_SENSITIVITY=2.0
FULLSCREEN_MODE=False
SOUND_VOLUME=1.0

def load_settings():
    global __location__
    settings_file=glob.glob(os.path.join(__location__,'settings_default.dat'))
    settings_dict=read_settings_file(settings_file[0])
    return settings_dict

def read_settings_file(settings_file):
    settings_lines=open(settings_file,"r")
    settings_dict={}
    for settings_line in settings_lines:
        settings_line=settings_line.replace('\n','').replace('\r','')
        if '=' in settings_line:
            parts=settings_line.split('=',1)
            parameter_name=parts[0]
            parameter_value=parts[1]
            if parameter_value == 'True' or parameter_value == 'False':
                parameter_value=True if parameter_value=='True' else False
            elif "\'" in parameter_value:
                parts_string=parameter_value.split("\'",2)
                parameter_value=parts_string[1]
            elif '.' in parameter_value:
                parameter_value=float(parameter_value)
            elif "(" in parameter_value:
                new_list=[]
                paren_parts=parameter_value.split('(',1)
                comma_parts=paren_parts[1].split(',')
                for comma_part in comma_parts:
                    if ')' in comma_part:
                        paren_parts2=comma_part.split(')')
                        new_list.append(int(paren_parts2[0]))
                    else:
                        new_list.append(int(comma_part))
                parameter_value=tuple(new_list)
            else:
                parameter_value=int(parameter_value)
            settings_dict[parameter_name]=parameter_value
    return settings_dict

def set_settings(settings_dict):
    for parameter in settings_dict:
        globals()[parameter]=settings_dict[parameter]


#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import glob
import os

ignore_pars=['QUIT','KEYDOWN','KEYUP','RLEACCEL']
__location__=os.path.realpath(os.path.join(os.getcwd(),os.path.dirname(__file__)))

def load_presets(game):
    global __location__
    preset_files=glob.glob(os.path.join(__location__,game+'/presets/gc_*'))
    all_presets={}
    for preset_file in preset_files:
        preset_dict=read_preset_file(preset_file)
        preset_name=os.path.basename(preset_file)[3:-4].replace("_"," ").title()
        all_presets[preset_name]=preset_dict
#        print(preset_file,preset_dict)
    return all_presets

def read_preset_file(preset_file):
    preset_lines=open(preset_file,"r")
    preset_dict={}
    for preset_line in preset_lines:
        preset_line=preset_line.replace('\n','').replace('\r','')
        if 'pygame.locals' in preset_line:
            break
        if '=' in preset_line and '{' not in preset_line:
            parts=preset_line.split('=',1)
            parameter_name=parts[0]
            parameter_value=parts[1]
            if '[' in parameter_name:
                parparts=parameter_name.split("\'",2)
                parameter_name=parparts[1]
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
            preset_dict[parameter_name]=parameter_value
    return preset_dict


def get_parameter_values(pardict,par):
    parlist=[]
    for preset,preset_dict in pardict.items():
        parlist.append(preset_dict[par])
    return list(set(parlist))


def save_preset(name):
    global ignore_pars,__location__

    name='presets/gc_'+name+'.dat'
    new_preset=open(os.join.path(__location__,name),"w")
    parameters=gc.__dir__()
    for par in parameters:
        if par.upper() == par and par[:2] != 'K_' and par[:1] != '_' and not par in ignore_pars:
           value=getattr(gc,par)
           if type(value) is str:
               value="\'"+value+"\'"
           new_preset.write(par+'='+str(value))
           new_preset.write("\n")
    new_preset.close()

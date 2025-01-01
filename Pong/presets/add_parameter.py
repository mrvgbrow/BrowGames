#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import glob
import sys
import os

preset_files=glob.glob('gc_*.dat')
parameter_name=sys.argv[1]
parameter_value=sys.argv[2]
for preset_file in preset_files:
    preset_lines=open(preset_file,"r")
    new_preset_file=open(preset_file+'.new',"w")
    linenum=0
    for preset_line in preset_lines:
        if linenum==5:
            new_preset_file.write(parameter_name+'='+parameter_value+"\n")
        linenum+=1
        new_preset_file.write(preset_line)
    new_preset_file.close()
    preset_lines.close()
    os.replace(preset_file+'.new',preset_file)

#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import glob
import sys
import os

preset_files=glob.glob('gc_*.dat')
parameter_name=sys.argv[1]
for preset_file in preset_files:
    preset_lines=open(preset_file,"r")
    new_preset_file=open(preset_file+'.new',"w")
    linenum=0
    for preset_line in preset_lines:
        if parameter_name+"=" not in preset_line:
            new_preset_file.write(preset_line)
        linenum+=1
    new_preset_file.close()
    preset_lines.close()
    os.replace(preset_file+'.new',preset_file)

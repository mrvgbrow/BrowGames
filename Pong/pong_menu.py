#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import pygame_menu
import pong_gameconstants as gc
import pong_presets as presets

def run_menu(title,screen,settings_dict,presets_dict,preset_default,fourplayers):
  global menu_run,original_pars
  font_size=24
  menu_run=False
  menu=pygame_menu.Menu(title,800,600,theme=pygame_menu.themes.THEME_DEFAULT,onclose=pygame_menu.events.CLOSE)
  get_parameters()
  n_parameters=len(original_pars.keys())
  n_rows=int(n_parameters/2)+2
  amenu=pygame_menu.Menu('About',800,600,theme=pygame_menu.themes.THEME_DEFAULT)
  smenu=pygame_menu.Menu('Settings',800,600,theme=pygame_menu.themes.THEME_DEFAULT)
  parmenu=pygame_menu.Menu('Game Parameters',800,600,theme=pygame_menu.themes.THEME_DEFAULT,columns=2,rows=n_rows)
  pmenu=pygame_menu.Menu('Presets',800,600,theme=pygame_menu.themes.THEME_DEFAULT,onclose=pygame_menu.events.CLOSE)
  spmenu=pygame_menu.Menu('Save Preset',800,600,theme=pygame_menu.themes.THEME_DEFAULT)
  menu.add.button('Play with Current Settings',pygame_menu.events.CLOSE,font_size=font_size)
  menu.add.button('Presets',pmenu,font_size=font_size)
  menu.add.button('Settings',smenu,font_size=font_size)
  menu.add.button('Game Parameters',parmenu,font_size=font_size)
  menu.add.button('About',amenu,font_size=font_size)
#  menu.add.button('Save Preset',spmenu)
  menu.add.button('Quit',pygame_menu.events.EXIT,font_size=font_size)
  menu.add.label('',font_size=font_size)
  menu.add.label('',font_size=font_size)
  add_control_menu(menu,fourplayers)
  menu.add.label('',font_size=font_size)
  preset_input=menu.add.label('Loaded preset: '+preset_default,font_size=font_size)
  make_amenu(amenu)
  make_parmenu(parmenu,presets_dict)
  make_smenu(smenu)
  make_pmenu(pmenu,presets_dict,preset_input)
  make_spmenu(spmenu)
  menu.mainloop(screen)
  return menu_run,preset_input.get_title()[15:]

def add_control_menu(menu,fourplayers):
  global original_pars

  control_values=['Arrows','WASD','IJKL','Computer','Mouse','None']
  font_size=24
  input_select_list=[]
  for input_val in control_values:
      input_select_list.append((input_val,input_val))
  widget=menu.add.dropselect(title='P1: ',items=input_select_list,onchange=set_input_drop,args=['PLAYER1_CONTROL'],default=control_values.index(original_pars['PLAYER1_CONTROL']),font_size=font_size-2,align=pygame_menu.locals.ALIGN_LEFT,float=True)
  widget.translate(gc.SCREEN_WIDTH/8,0)
  widget=menu.add.dropselect(title='P2: ',items=input_select_list,onchange=set_input_drop,args=['PLAYER2_CONTROL'],default=control_values.index(original_pars['PLAYER2_CONTROL']),font_size=font_size-2,align=pygame_menu.locals.ALIGN_RIGHT,float=True)
  widget.translate(-gc.SCREEN_WIDTH/8,0)
  menu.add.label('',font_size=font_size)
  if fourplayers:
    widget=menu.add.dropselect(title='P3: ',items=input_select_list,onchange=set_input_drop,args=['PLAYER3_CONTROL'],default=control_values.index(original_pars['PLAYER3_CONTROL']),font_size=font_size-2,align=pygame_menu.locals.ALIGN_LEFT,float=True)
    widget.translate(gc.SCREEN_WIDTH/8,0)
    widget=menu.add.dropselect(title='P4: ',items=input_select_list,onchange=set_input_drop,args=['PLAYER4_CONTROL'],default=control_values.index(original_pars['PLAYER4_CONTROL']),font_size=font_size-2,align=pygame_menu.locals.ALIGN_RIGHT,float=True)
    widget.translate(-gc.SCREEN_WIDTH/8,0)

def make_spmenu(spmenu):
  label=spmenu.add.label('')
  widget=spmenu.add.text_input('Preset Name: ',default='')
  def save_preset_inmenu():
      presets.save_preset(widget.get_value())
      label.set_title('Saved!')
  spmenu.add.button('Save',save_preset_inmenu)
  spmenu.add.button('Back',pygame_menu.events.BACK,background_color=(75,75,75),font_color=(255,255,255))

def make_pmenu(pmenu,presets_dict,preset_input):
  font_size=24
  def select_preset(widget=None):
      global menu_run
      preset_input.set_title('Loaded Preset: '+widget.get_title())
      presets.set_preset(presets_dict[widget.get_title()])
      menu_run=True
      pmenu.close()
  for preset_key in sorted(list(presets_dict.keys())):
      preset_name=preset_key
      button=pmenu.add.button(preset_name,select_preset,font_size=font_size)
      button.add_self_to_kwargs()
  pmenu.add.label('')
  pmenu.add.button('Back',pygame_menu.events.BACK,font_size=font_size,background_color=(75,75,75),font_color=(255,255,255))
  return True

def make_amenu(amenu):
  font_size=24
  readme_file="text/instructions.md"
  readme_file_lines=open(readme_file,"r")
  first_line=readme_file_lines.readline()
  title_array1=first_line.split(">")
  title_array2=title_array1[1].split(" ")
  version_file="text/version.md"
  version_file_lines=open(version_file,"r")
  first_line=version_file_lines.readline()
  version_array1=first_line.split("<")
  version_array2=version_array1[1].split(" ")
  amenu.add.label(title_array2[0])
  amenu.add.label('Version '+version_array2[1])
  amenu.add.label('Written by Nicholas A. Bond, 2024-2025')
  amenu.add.label('')
  amenu.add.button('Back',pygame_menu.events.BACK,font_size=font_size,background_color=(75,75,75),font_color=(255,255,255))
  return True

def make_smenu(smenu):
  global original_pars
  font_size=24
  first_widget=[]
  widget=smenu.add.text_input('Screen Width: ',default=getattr(gc,'SCREEN_WIDTH'),onchange=set_input,args=['SCREEN_WIDTH'],input_type=pygame_menu.locals.INPUT_INT,font_size=font_size)
  widget=smenu.add.text_input('Screen Height: ',default=getattr(gc,'SCREEN_HEIGHT'),onchange=set_input,args=['SCREEN_HEIGHT'],input_type=pygame_menu.locals.INPUT_INT,font_size=font_size)
  widget=smenu.add.toggle_switch('Fullscreen Mode',getattr(gc,'FULLSCREEN_MODE'),onchange=set_input,args=['FULLSCREEN_MODE'],font_size=font_size)
  widget=smenu.add.range_slider('Volume: ',default=getattr(gc,'SOUND_VOLUME'),onchange=set_input,args=['SOUND_VOLUME'],increment=0.05,range_values=(0,1),font_size=font_size)
  widget=smenu.add.range_slider('Mouse Sensitivity: ',default=getattr(gc,'MOUSE_SENSITIVITY'),onchange=set_input,args=['MOUSE_SENSITIVITY'],increment=0.1,range_values=(0,5),font_size=font_size)
  smenu.add.label('')
  widget=smenu.add.button('OK',pygame_menu.events.BACK,background_color=(75,75,75),font_color=(255,255,255))

def make_parmenu(parmenu,presets_dict):
  global original_pars
  font_size=17
  first_widget=[]
  for par in sorted(original_pars):
      value=getattr(gc,par)
      if type(value) is bool:
          widget=parmenu.add.toggle_switch(par,value,onchange=set_input,args=[par],font_size=font_size,align=pygame_menu.locals.ALIGN_LEFT)
      elif type(value) is int:
          widget=parmenu.add.text_input(par+': ',default=value,onchange=set_input,args=[par],input_type=pygame_menu.locals.INPUT_INT,font_size=font_size,align=pygame_menu.locals.ALIGN_LEFT)
      elif type(value) is float:
          widget=parmenu.add.text_input(par+': ',default=value,onchange=set_input,args=[par],input_type=pygame_menu.locals.INPUT_FLOAT,font_size=font_size,align=pygame_menu.locals.ALIGN_LEFT)
      elif type(value) is str and '_CONTROL' not in par:
          parvals=presets.get_parameter_values(presets_dict,par)
          input_select_list=[]
          for input_val in parvals:
              input_select_list.append((input_val,input_val))
          widget=parmenu.add.dropselect(title=par+': ',items=input_select_list,onchange=set_input_drop,args=[par],default=parvals.index(value),font_size=font_size,align=pygame_menu.locals.ALIGN_LEFT)
      elif type(value) is tuple:
          tmenu=pygame_menu.Menu(par,600,400,theme=pygame_menu.themes.THEME_DEFAULT)
          widget=parmenu.add.button(par,tmenu,font_size=font_size,align=pygame_menu.locals.ALIGN_LEFT)
          index=0
          for subvalue in value:
              tmenu.add.text_input(par+': ',default=subvalue,onchange=set_input_subvalue,args=[par,index],input_type=pygame_menu.locals.INPUT_INT)
              index+=1
          tmenu.add.button('OK',pygame_menu.events.BACK)
      if not first_widget:
          first_widget=widget
  parmenu.add.label('')
  widget=parmenu.add.button('OK',pygame_menu.events.BACK,background_color=(75,75,75),font_color=(255,255,255))
  parmenu.scroll_to_widget(first_widget)

def get_parameters():
  global original_pars
  parameters=gc.__dir__()
  ignore_pars=['QUIT','KEYDOWN','KEYUP','RLEACCEL','SOUND_VOLUME','MOUSE_SENSITIVITY','SCREEN_HEIGHT','SCREEN_WIDTH']
  original_pars={}
  for par in parameters:
      if par.upper() == par and par[:2] != 'K_' and par[:1] != '_' and not par in ignore_pars:
          original_pars[par]=getattr(gc,par)

def set_input(input_value,args):
  setattr(gc,args[0],input_value)

def set_input_drop(input_dict,input_value,args):
  setattr(gc,args[0],input_value)

def set_input_subvalue(input_value,args):
  tup=getattr(gc,args[0])
  tup_vals=[tup[0],tup[1],tup[2]]
  tup_vals[args[1]]=input_value
  new_tup=(tup_vals[0],tup_vals[1],tup_vals[2])
  setattr(gc,args[0],new_tup)

def load_original_parameters():
  global original_pars
  for par in original_pars:
      setattr(gc,par,original_pars[par])


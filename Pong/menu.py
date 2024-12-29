#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import pygame_menu
import gameconstants as gc
import presets

def run_menu(title,screen,presets_dict,preset_default):
  global menu_run
  menu_run=False
  menu=pygame_menu.Menu(title,800,600,theme=pygame_menu.themes.THEME_BLUE,onclose=pygame_menu.events.CLOSE)
  smenu=pygame_menu.Menu('Settings',800,600,theme=pygame_menu.themes.THEME_BLUE)
  pmenu=pygame_menu.Menu('Presets',800,600,theme=pygame_menu.themes.THEME_BLUE,onclose=pygame_menu.events.CLOSE)
  spmenu=pygame_menu.Menu('Save Preset',800,600,theme=pygame_menu.themes.THEME_BLUE)
  menu.add.button('Play with Current Settings',pygame_menu.events.CLOSE)
  def one_player_run():
      presets.set_preset(presets_dict['One Player Standard'])
      menu.close()
  menu.add.button('One-Player Standard',one_player_run)
  def two_player_run():
      presets.set_preset(presets_dict['Two Player Standard'])
      menu.close()
  menu.add.button('Two-Player Standard',two_player_run)
  def zero_player_run():
      presets.set_preset(presets_dict['Zero Player Standard'])
      menu.close()
  menu.add.button('Computer Only',zero_player_run)
  menu.add.button('Presets',pmenu)
  menu.add.button('Settings',smenu)
#  menu.add.button('Save Preset',spmenu)
  menu.add.button('Quit',pygame_menu.events.EXIT)
  menu.add.label('')
  preset_input=menu.add.label('Loaded preset: '+preset_default)
  make_smenu(smenu)
  make_pmenu(pmenu,presets_dict,preset_input)
  make_spmenu(spmenu)
  menu.mainloop(screen)
  return menu_run,preset_input.get_title()[15:]

def make_spmenu(spmenu):
  label=spmenu.add.label('')
  widget=spmenu.add.text_input('Preset Name: ',default='')
  def save_preset_inmenu():
      presets.save_preset(widget.get_value())
      label.set_title('Saved!')
  spmenu.add.button('Save',save_preset_inmenu)
  spmenu.add.button('Back',pygame_menu.events.BACK)

def make_pmenu(pmenu,presets_dict,preset_input):
  def select_preset(widget=None):
      global menu_run
      preset_input.set_title('Loaded Preset: '+widget.get_title())
      presets.set_preset(presets_dict[widget.get_title()])
      menu_run=True
      pmenu.close()
  for preset_key in presets_dict.keys():
      preset_name=preset_key
      button=pmenu.add.button(preset_name,select_preset)
      button.add_self_to_kwargs()
  pmenu.add.label('')
  pmenu.add.button('Back',pygame_menu.events.BACK)
  return True

def make_smenu(smenu):
  global original_pars
  parameters=gc.__dir__()
  ignore_pars=['QUIT','KEYDOWN','KEYUP','RLEACCEL']
  input_values=['arrows','wasd','computer']
  input_select_list=[]
  for input_val in input_values:
      input_select_list.append((input_val.capitalize(),input_val))
  original_pars={}
  first_widget=[]
  for par in parameters:
      if par.upper() == par and par[:2] != 'K_' and par[:1] != '_' and not par in ignore_pars:
          original_pars[par]=getattr(gc,par)
          value=getattr(gc,par)
          if type(value) is bool:
              widget=smenu.add.toggle_switch(par,value,onchange=set_input,args=[par],font_size=24)
          elif type(value) is int:
              widget=smenu.add.text_input(par+': ',default=value,onchange=set_input,args=[par],input_type=pygame_menu.locals.INPUT_INT,font_size=24)
          elif type(value) is float:
              widget=smenu.add.text_input(par+': ',default=value,onchange=set_input,args=[par],input_type=pygame_menu.locals.INPUT_FLOAT,font_size=24)
          elif value in input_values:
              widget=smenu.add.dropselect(title=par+': ',items=input_select_list,onchange=set_input_drop,args=[par],default=input_values.index(value),font_size=24)
          elif type(value) is tuple:
              tmenu=pygame_menu.Menu(par,600,400,theme=pygame_menu.themes.THEME_BLUE)
              widget=smenu.add.button(par,tmenu,font_size=24)
              index=0
              for subvalue in value:
                  tmenu.add.text_input(par+': ',default=subvalue,onchange=set_input_subvalue,args=[par,index],input_type=pygame_menu.locals.INPUT_INT)
                  index+=1
              tmenu.add.button('OK',pygame_menu.events.BACK)
          if not first_widget:
              first_widget=widget
  smenu.add.label('')
  smenu.add.button('OK',pygame_menu.events.BACK)
  smenu.scroll_to_widget(first_widget)

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

#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import pygame_menu

def run_menu(title,screen,settings_dict):
  global menu_run,game_select
  game_select='None'
  font_size=36
  menu_run=False
  menu=pygame_menu.Menu(title,800,600,theme=pygame_menu.themes.THEME_DEFAULT,onclose=pygame_menu.events.CLOSE)
  gmenu=pygame_menu.Menu('Game List',800,600,theme=pygame_menu.themes.THEME_DEFAULT,onclose=pygame_menu.events.CLOSE)
  amenu=pygame_menu.Menu('About',800,600,theme=pygame_menu.themes.THEME_DEFAULT)
#  smenu=pygame_menu.Menu('Settings',800,600,theme=pygame_menu.themes.THEME_DEFAULT)
  menu.add.button('Select Game',gmenu,font_size=font_size)
#  menu.add.button('Settings',smenu,font_size=font_size)
  menu.add.button('About',amenu,font_size=font_size)
#  menu.add.button('Save Preset',spmenu)
  menu.add.button('Quit',pygame_menu.events.EXIT,font_size=font_size)
  make_amenu(amenu)
#  make_smenu(smenu)
  make_gmenu(gmenu)
  menu.mainloop(screen)
  return menu_run,game_select

def make_amenu(amenu):
  font_size=36
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

def make_gmenu(gmenu):
  global game_select
  font_size=36
  game_list=read_game_list()
  def set_game_select(widget=None):
      global game_select
      if widget != None:
          game_select=widget.get_title()
          gmenu.close()
  for game in game_list:
      button=gmenu.add.button(game.capitalize(),set_game_select,font_size=font_size)
      button.add_self_to_kwargs()
  gmenu.add.label('')
  widget=gmenu.add.button('Back',pygame_menu.events.BACK,background_color=(75,75,75),font_color=(255,255,255))

def make_smenu(smenu):
  font_size=36
  first_widget=[]
  widget=smenu.add.text_input('Screen Width: ',default=getattr(gc,'SCREEN_WIDTH'),onchange=set_input,args=['SCREEN_WIDTH'],input_type=pygame_menu.locals.INPUT_INT,font_size=font_size)
  widget=smenu.add.text_input('Screen Height: ',default=getattr(gc,'SCREEN_HEIGHT'),onchange=set_input,args=['SCREEN_HEIGHT'],input_type=pygame_menu.locals.INPUT_INT,font_size=font_size)
  widget=smenu.add.toggle_switch('Fullscreen Mode',getattr(gc,'FULLSCREEN_MODE'),onchange=set_input,args=['FULLSCREEN_MODE'],font_size=font_size)
  widget=smenu.add.range_slider('Volume: ',default=getattr(gc,'SOUND_VOLUME'),onchange=set_input,args=['SOUND_VOLUME'],increment=0.05,range_values=(0,1),font_size=font_size)
  widget=smenu.add.range_slider('Mouse Sensitivity: ',default=getattr(gc,'MOUSE_SENSITIVITY'),onchange=set_input,args=['MOUSE_SENSITIVITY'],increment=0.1,range_values=(0,5),font_size=font_size)
  smenu.add.label('')
  widget=smenu.add.button('OK',pygame_menu.events.BACK,background_color=(75,75,75),font_color=(255,255,255))

def set_input(input_value,args):
  setattr(gc,args[0],input_value)

def set_input_drop(input_dict,input_value,args):
  setattr(gc,args[0],input_value)

def read_game_list():
  game_list=[]
  game_file='game_list.dat'
  gamelist_lines=open(game_file,'r')
  for gamelist_line in gamelist_lines:
      game_list.append(gamelist_line.rstrip())
  return game_list

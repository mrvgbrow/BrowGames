#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import pygame_menu
import settings
button_color=(255,229,180)
button_text=(25,25,25)

def run_menu(title,screen,settings_dict):
  global menu_run,game_select,current_sets
  game_select='None'
  font_size=36
  menu_run=False
  all_quit=False
  browtheme=pygame_menu.Theme(background_color=(255,255,255,255), title_font_shadow=True,title_background_color=(50,0,100,255),selection_color=(25,25,180,255),widget_font_color=(25,25,25,255))
  menu=pygame_menu.Menu(title,800,600,theme=browtheme,onclose=pygame_menu.events.CLOSE)
  current_sets=settings_dict
  gmenu=pygame_menu.Menu('Game List',800,600,theme=browtheme,onclose=pygame_menu.events.CLOSE)
  amenu=pygame_menu.Menu('About',800,600,theme=browtheme)
  smenu=pygame_menu.Menu('Settings',800,600,theme=browtheme)
  menu.add.image('mrbrow.jpg')
  menu.add.button('Select Game',gmenu,font_size=font_size)
  menu.add.button('Settings',smenu,font_size=font_size)
  menu.add.button('About',amenu,font_size=font_size)
#  menu.add.button('Save Preset',spmenu)
  menu.add.button('Quit',pygame_menu.events.EXIT,font_size=font_size)
  make_amenu(amenu)
  make_smenu(smenu)
  make_gmenu(gmenu)
  menu.mainloop(screen)
  return menu_run,game_select,all_quit,current_sets

def make_amenu(amenu):
  global button_color,button_text
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
  amenu.add.button('Back',pygame_menu.events.BACK,font_size=font_size,background_color=button_color,font_color=button_text,border_width=2)
  return True

def make_gmenu(gmenu):
  global button_color,button_text
  global game_select
  font_size=36
  game_list=read_game_list()
  def set_game_select(widget=None):
      global game_select
      if widget != None:
          game_select=widget.get_title()
          gmenu.close()
  for game in game_list:
      button=gmenu.add.button(game.title(),set_game_select,font_size=font_size)
      button.add_self_to_kwargs()
  gmenu.add.label('')
  widget=gmenu.add.button('Back',pygame_menu.events.BACK,background_color=button_color,font_color=button_text,border_width=2)

def make_smenu(smenu):
  global button_color,button_text,current_sets
  font_size=36
  first_widget=[]
  widget=smenu.add.toggle_switch('Fullscreen Mode',current_sets['FULLSCREEN_MODE'],onchange=set_input,args=['FULLSCREEN_MODE'],font_size=font_size)
  widget=smenu.add.range_slider('Volume: ',default=current_sets['SOUND_VOLUME'],onchange=set_input,args=['SOUND_VOLUME'],increment=0.05,range_values=(0,1),font_size=font_size)
  widget=smenu.add.range_slider('Mouse Sensitivity: ',default=current_sets['MOUSE_SENSITIVITY'],onchange=set_input,args=['MOUSE_SENSITIVITY'],increment=0.1,range_values=(0,5),font_size=font_size)
  smenu.add.label('')
  widget=smenu.add.button('OK',pygame_menu.events.BACK,background_color=button_color,font_color=button_text,border_width=2)

def set_input(input_value,args):
  global current_sets
  current_sets[args[0]]=input_value

def set_input_drop(input_dict,input_value,args):
  global current_sets
  current_sets[args[0]]=input_value

def read_game_list():
  game_list=[]
  game_file='game_list.dat'
  gamelist_lines=open(game_file,'r')
  for gamelist_line in gamelist_lines:
      game_list.append(gamelist_line.rstrip())
  return game_list

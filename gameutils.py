
import pygame
import os
import settings
import datetime
import sys
import gameconstants as gc
import presets

def browgame_init(font=False,mouse=False,clock=False):
    pygame.init()
    if font: pygame.font.init()
    if clock: return pygame.time.Clock()


def set_screen(gc_dict):
    if settings.sets['FULLSCREEN_MODE']:
        screen = pygame.display.set_mode((gc_dict['SCREEN_WIDTH'],gc_dict['SCREEN_HEIGHT']),pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((gc_dict['SCREEN_WIDTH'],gc_dict['SCREEN_HEIGHT']))
    return screen

def mouse_init():
    pygame.event.set_grab(True)
    pygame.mouse.set_visible(False)

def append_scores(game,control_list,scores,game_time):
    # Print the game time and score to a table to keep track of high scores
    original_stdout = sys.stdout
    with open('scores.dat','a') as f:
        sys.stdout = f
        print('%s, %s, Player1 (%s): %d,  Player2 (%s): %d,  Game Time: %.2f seconds' % (datetime.datetime.now(),game,control_list[0],scores[0],control_list[1],scores[1],game_time))
        sys.stdout=original_stdout
    
def show_debug(message,font,screen,position):
    if message != '':
        debug_text=font.render(message,True,(255,255,255))
        screen.blit(debug_text, (position[0],position[1]))

def show_time(game_time,font,screen,position):
    rounded_time=float(int(game_time*100))/100.0
    time_text=font.render(f'Time: {rounded_time}',True,(255,255,255))
    screen.blit(time_text, (position[0],position[1]))

def render(screen,all_sprites,screen_color):
    screen.fill(screen_color)
    for entity in all_sprites:
        if not hasattr(entity,'invisible') or not entity.invisible:
            screen.blit(entity.surf,entity.rect)

def advance_clock(clock,framerate,game_time):
    clock.tick(framerate)
    return game_time+1.0/framerate

def process_standard_events(running,pause,step=False,reset=False,endgame=None):
    for event in pygame.event.get():
        # Did the user click the window close button?
        if event.type == pygame.QUIT or event.type == endgame:
            running = False
        elif event.type == gc.KEYDOWN:
            if event.key == gc.K_ESCAPE:   # Esc quits
                running = False
            if event.key == gc.K_p:     # p pauses/unpauses
                if pause:
                    pause=False
                else:
                    pause=True
            if event.key == gc.K_RIGHTBRACKET:     # ] steps one frame at a time
                step=True
            if event.key == gc.K_r:                # r resets the score
                reset=True
    return running,pause,step,reset

def init_sound(path,sound_files):
    for sound_file in sound_files:
        pygame.mixer.music.load(os.path.join(path,sound_file))
    pygame.mixer.music.set_volume(settings.sets['SOUND_VOLUME'])   # Set the volume.

def draw_trail(screen,position_array):
    for position in position_array:
        if position[0]>0 and position[1]>0:
            pygame.draw.circle(screen, (255,255,255),position,1)

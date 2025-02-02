#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'  # Used to hide the pygame info message 
import pygame
import sys
import presets
import gameutils
import settings
import menu
import scoretable
from . import reverse_string
import datetime
import random
import touchkey
from . import reverse_gameconstants as gc

def run(current_pars,settings_dict,quickstart=False,default='Reverse'):
    # Initialize the game, music, timer, and screen
    __location__=os.path.realpath(os.path.join(os.getcwd(),os.path.dirname(__file__)))
    clock=gameutils.browgame_init(font=True,clock=True)
    presets_dict=presets.load_presets('Reverse')
    if not current_pars:
        preset_set=default
        gc.set_preset(presets_dict[preset_set])
        gc.scale_parameters()
    else:
        gc.set_preset(current_pars)
        preset_set=None

    # Load the menu. Continue reloading the menu until an option is selected that requests
    # the game to load.
    if not quickstart:
        back_to_main,menu_run,preset_out,current_pars=menu.run_menu('Reverse',settings_dict,presets_dict,preset_set,1,False,init_pars=current_pars)
        if back_to_main:
            return settings_dict,True,current_pars
        gc.set_preset(current_pars)
        gc.scale_parameters()

    settings.set_settings(settings_dict)
    current_parameters=gc.get_parameters(gc.__dir__())
    screen = pygame.display.set_mode([gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT])
    score_table=scoretable.ScoreTable('scores.dat')
    
    ENDGAME = pygame.USEREVENT + 1
    BUTTON_PRESS=pygame.USEREVENT+2
    font=pygame.font.Font(None,gc.FONT_SIZE)
    font_prompt=pygame.font.Font(None,50)
    
    rstring=reverse_string.ReverseString(gc.NUMBER_DIGITS,gc.NUMBER_REVERSES)
    
    skipkey=touchkey.TouchKey((gc.SCREEN_WIDTH*0.83,gc.SCREEN_HEIGHT*0.9),'SKIP',size=40)
    quitkey=touchkey.TouchKey((gc.SCREEN_WIDTH*0.17,gc.SCREEN_HEIGHT*0.9),'QUIT',size=40)
    
    width_interval=0.1*gc.SCREEN_WIDTH
    key_height=0.35*gc.SCREEN_HEIGHT
    first_key=0.55*gc.SCREEN_WIDTH-width_interval*float(gc.NUMBER_DIGITS)/2
    touchkeys=pygame.sprite.Group()
    digit_touchkeys=pygame.sprite.Group()
    all_sprites=pygame.sprite.Group()
    for i in range(gc.NUMBER_DIGITS):
        touchkey_i=touchkey.TouchKey((first_key+width_interval*i,key_height),str(rstring.value[i]),place=i+1)
        touchkeys.add(touchkey_i)
        digit_touchkeys.add(touchkey_i)
        all_sprites.add(touchkey_i)
    all_sprites.add(skipkey,quitkey)
    
    running = True
    total_time=0
    score=0
    game_state=0
    game_count=0
    while running:
    
        # Start a new game
        if game_state==0:
            n_guess=0
            user_text=''
            reverse_message=''
            score_bonus=gc.SCORE_MAX
            game_state=1
            rstring.reset_string()
            rstring.do_reverses(gc.NUMBER_REVERSES)
            for touchkey_i in digit_touchkeys:
                touchkey_i.change_key(str(rstring.value[touchkey_i.place-1]))
    
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == ENDGAME:
                game_state=0
            elif event.type == BUTTON_PRESS:
                button_press.render_key()
                if button_press in digit_touchkeys:
                    n_guess+=1
                    for touchkey_i in digit_touchkeys:
                        touchkey_i.change_key(str(rstring.value[touchkey_i.place-1]))
                    if rstring.check_solved():
                        game_state=2
                        reverse_message='YOU GOT IT!'
                        score+=score_bonus
                        game_count+=1
                    else:
                        if n_guess>=gc.NUMBER_REVERSES:
                            score_bonus=int(score_bonus/2)
                button_press=None
            elif event.type == gc.KEYDOWN:
                if event.key == gc.K_ESCAPE:
                    running = False
    
    
        # Fill the background
        screen.fill(gc.SCREEN_COLOR)
    
        pressed_buttons=pygame.mouse.get_pressed()
        mouse_pos=pygame.mouse.get_pos()
    
        for touchkey_i in touchkeys:
            pressed=touchkey_i.update(pressed_buttons,mouse_pos)
            if pressed:
                rstring.reverse_digits(touchkey_i.place)
                pygame.time.set_timer(BUTTON_PRESS, 100,loops=1)
                button_press=touchkey_i
    
        pressed_quit=quitkey.update(pressed_buttons,mouse_pos)
        if pressed_quit:
            running=False
    
        pressed_skip=skipkey.update(pressed_buttons,mouse_pos)
        if pressed_skip:
            game_state=2
            score=0
            score_bonus=gc.SCORE_MAX
            pygame.time.set_timer(BUTTON_PRESS, 100,loops=1)
            button_press=skipkey
            reverse_message='Skipping this problem'
    
    #    screen.blit(bg,(0,0))
        for entity in all_sprites:
            screen.blit(entity.surf,entity.rect)
    
        # Display the score in the corner
        score_text=font.render(f'Score: {score:d}   Guess Bonus: {score_bonus:d}',True,(255,255,255))
        screen.blit(score_text, (gc.SCORE_XPOS,gc.SCORE_YPOS))
    
        # Update the message to the user
        reverse_text=font_prompt.render(reverse_message,True,(255,255,255))
        screen.blit(reverse_text, (gc.SCREEN_WIDTH/2-reverse_text.get_width()/2,gc.SCREEN_HEIGHT*0.6-reverse_text.get_height()/2))
    
        # Flip the display
        pygame.display.flip()
    
        # Only run the timer if the game is still going
        if game_state==1:
            clock.tick(gc.TICK_FRAMERATE)
            total_time=total_time+1/gc.TICK_FRAMERATE
            
        # Puzzle solved, display win message
        if game_state==2:
            pygame.time.set_timer(ENDGAME, 2000,loops=1)
            game_state=3
    
    if len(sys.argv)>1:
        player_name=sys.argv[1]
    else:
        player_name='Unknown'
    
    print('')
    print('Your Score: %d' % (score))
    print('')
    print('High Scores:')
    print('')
    
    # Print the game time and score to a data file
    data_list=[player_name,datetime.datetime.now(),score,game_count]
    if score>0:
        score_table.add_row(data_list)
    score_table.print_all_best(player_name)
    

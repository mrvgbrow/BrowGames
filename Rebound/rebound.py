#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide' 
os.environ['SDL_VIDEO_WINDOW_POS']="%d,%d" % (0,0)
import pygame
import sys
import gameutils
import menu
import presets
import settings
from . import rebound_player as player
import background
import datetime
from . import rebound_ball as ball
from . import rebound_gameconstants as gc

def run(current_pars,settings_dict,quickstart=False,default='Original'):
    # Initialize the game, music, timer, and screen
    __location__=os.path.realpath(os.path.join(os.getcwd(),os.path.dirname(__file__)))
    clock=gameutils.browgame_init(font=True,clock=True)
    presets_dict=presets.load_presets('Rebound')
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
        back_to_main,menu_run,preset_out,current_pars=menu.run_menu('Rebound',settings_dict,presets_dict,preset_set,2,True,init_pars=current_pars)
        if back_to_main:
            return settings_dict,True,current_pars
        gc.set_preset(current_pars)
        gc.scale_parameters()

    settings.set_settings(settings_dict)
    current_parameters=gc.get_parameters(gc.__dir__())
    font=pygame.font.Font("pong-score-extended.ttf",gc.FONT_SIZE) # A pong-like font. Used in displayed text.
    gameutils.init_sound('Sounds',["ding.mp3"])

    if settings.sets['FULLSCREEN_MODE']:
        screen = pygame.display.set_mode([gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT],pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode([gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT])
    
    all_sprites = pygame.sprite.Group()
    font_end=pygame.font.Font(None,72)
    
    # Create the player and ball sprites, add them to sprite groups for 
    # ease of processing.
    player1=player.Player(gc.PLAYER_Y_POSITION,gc.PLAYER1_COLOR,1,gc.PLAYER1_CONTROL,gc.PADDLE_TYPE)
    player2=player.Player(gc.PLAYER_Y_POSITION,gc.PLAYER2_COLOR,2,gc.PLAYER2_CONTROL,gc.PADDLE_TYPE)
    all_sprites.add(player1,player2)
    balls=pygame.sprite.Group()
    for i in range(gc.BALL_NUMBER):
        ball_i=ball.Ball()
        balls.add(ball_i)
        all_sprites.add(ball_i)
    
    # Create the net
    net=background.ObjectFill((0.5*gc.SCREEN_WIDTH,gc.SCREEN_HEIGHT-gc.NET_HEIGHT/2),(gc.NET_WIDTH,gc.NET_HEIGHT),gc.NET_COLOR)
    all_sprites.add(net)
    
    # Initialize variables
    running = True    # Flag indicating when to stop the game
    total_time=0      
    game_state=3
    ball_position_array=[]
    scores=[0,0]
    reference_time=0
    pause=False
    step=False
    game_message=''
    while running:
    
        running,pause,step,reset=gameutils.process_standard_events(running,pause)
        # If paused, continuously skip over the game loop (except event processing).
        # If taking one step through the loop, don't pause but unset the step
        # immediately after.
        if pause and not step:
            pygame.time.delay(16)
            continue
        if step:
            step=False
    
        pressed_keys = pygame.key.get_pressed()
        mouse_relative = pygame.mouse.get_rel()
    
        if game_state==1:
            # For each ball, determine the position where the it will intersect with
            # the court line. This is used by the AI to decide where to move.
            for ball_i in balls:
                ball_i.update()
                intercept=ball_i.compute_intercept(gc.PLAYER_Y_POSITION,gc.GRAVITY)
                ball_position_array.append((ball_i.x,ball_i.y))
    
            # Only update the AI position when the intercept falls on its side
            if intercept > 0.5*gc.SCREEN_WIDTH:
                player1.update(pressed_keys,-1,mouse_relative)
                player2.update(pressed_keys,intercept,mouse_relative)
            else:
                player1.update(pressed_keys,intercept,mouse_relative)
                player2.update(pressed_keys,-1,mouse_relative)
    
    
        gameutils.render(screen,all_sprites,gc.SCREEN_COLOR)
    
        # Render the score in the upper left corner 
        if not gc.SCORE_HIDE:
            score_text1=font.render(f'{scores[0]}',True,(255,255,255))
            score_text2=font.render(f'{scores[1]}',True,(255,255,255))
    #        screen.blit(score_text, (gc.SCORE_XPOS,gc.SCORE_YPOS))
            screen.blit(score_text1, (0.23*gc.SCREEN_WIDTH,gc.SCORE_YPOS))
            screen.blit(score_text2, (0.73*gc.SCREEN_WIDTH,gc.SCORE_YPOS))
    
        # Update the message to the user
        game_text=font_end.render(game_message,True,(255,255,255))
        screen.blit(game_text, (gc.SCREEN_WIDTH/2-game_text.get_width()/2,gc.SCREEN_HEIGHT*0.53-game_text.get_height()/2))
    
    
        # Check whether any balls are colliding with the player 1. If so, compute
        # the bounce angle 
        balls_hit=pygame.sprite.spritecollide(player1, balls,False,collided=pygame.sprite.collide_mask)
        if balls_hit:
            for ball_hit in balls_hit:
                ball_hit.bounce_wall('up')
                anglechange=player1.compute_anglechange(ball_hit.rect.centerx)
                ball_hit.anglechange(anglechange)
    
        # Check whether any balls are colliding with the player 2. If so, compute
        # the bounce angle 
        balls_hit=pygame.sprite.spritecollide(player2, balls,False,collided=pygame.sprite.collide_mask)
        if balls_hit:
            for ball_hit in balls_hit:
                ball_hit.bounce_wall('up')
                anglechange=-player2.compute_anglechange(ball_hit.rect.centerx)
                ball_hit.anglechange(anglechange)
    
        # Check whether any balls are colliding with the net. If so, 
        # bounce in the opposite direction
        balls_hit=pygame.sprite.spritecollide(net, balls,False)
        if balls_hit:
            for ball_hit in balls_hit:
                if ball_hit.speedx>0:
                    ball_hit.bounce_wall('left')
                else:
                    ball_hit.bounce_wall('right')
    
        # If no balls remain on the field, increment the score for the player
        # whose side it *didn't* fall on
        if not balls:
            game_state=3
            ball_position_array=[]
            reference_time=total_time
            ball_0=ball.Ball()
            balls.add(ball_0)
            all_sprites.add(ball_0)
            if intercept<0.5*gc.SCREEN_WIDTH:
                scores[0]+=1
            else:
                scores[1]+=1
    
        if game_state==3:
            countdown=int(4+reference_time-total_time)
            game_message=str(countdown)
            if countdown==0:
                game_state=1
                game_message=''
    
        if gc.SHOW_BALL_TRAIL:
            gameutils.draw_trail(screen,ball_position_array)
    
        # Update the display
        pygame.display.flip()
    
        total_time=gameutils.advance_clock(clock,gc.TICK_FRAMERATE,total_time)
    
    # Print the game time and score to a table to keep track of high scores
    gameutils.append_scores('Rebound',[gc.PLAYER1_CONTROL,gc.PLAYER2_CONTROL],scores,total_time)
    
    # Stop the sound effects
    pygame.mixer.music.stop()
    
    return settings_dict,False,current_pars

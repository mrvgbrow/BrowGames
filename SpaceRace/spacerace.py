#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import os
import sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide' 
#os.environ['SDL_VIDEO_WINDOW_POS']="%d,%d" % (0,0)
import pygame
from . import spacerace_gameconstants as gc
import presets
import settings
import menu
import datetime
import timer
import time
from . import spacerace_player 
import random
import timeit
from . import spacerace_asteroid as asteroid
import background as bg
import gameobject as go

def run(preset_init,settings_dict,quickstart=False):
    __location__=os.path.realpath(os.path.join(os.getcwd(),os.path.dirname(__file__)))
    gc.gc,sdict=gc.make_shortcuts(gc.gc)
    gc.gc=gc.process_game_arguments(sys.argv,gc.gc,sdict)
    
    pygame.init()
    pygame.font.init()
    presets_dict=presets.load_presets('SpaceRace')
    settings.set_settings(settings_dict)
    preset_set=preset_init
    gc.set_preset(presets_dict[preset_set])
    gc.scale_parameters()
    screen = pygame.display.set_mode((800,600))
    
    # Load the menu. Continue reloading the menu until an option is selected that requests
    # the game to load.
    if not quickstart:
        menu_run=True
        while menu_run:
            back_to_main,menu_run,preset_out,current_pars=menu.run_menu('Space Race',screen,settings_dict,presets_dict,preset_set,False)
            if back_to_main:
                return settings_dict
            if menu_run:
                gc.set_preset(presets_dict[preset_out])
            preset_set=preset_out
     
        # Scale the selected game constants and extract them as a dictionary
        gc.set_preset(current_pars)
        gc.scale_parameters()
    
    if settings.FULLSCREEN_MODE:
        screen = pygame.display.set_mode((gc.gc['SCREEN_WIDTH'],gc.gc['SCREEN_HEIGHT']),pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((gc.gc['SCREEN_WIDTH'],gc.gc['SCREEN_HEIGHT']))
    
    # The asteroid wrap horizontally, but with a delay. Defining a larger rectangle for their motion
    # to account for this.
    full_width=gc.gc['GAME_WIDTH']+gc.gc['ASTEROID_REVIVE_TIME']*gc.gc['ASTEROID_SPEED']
    pad=(full_width-gc.gc['GAME_WIDTH'])/2
    screen_rect=pygame.Rect((gc.gc['LEFT']-pad,gc.gc['TOP']),(gc.gc['GAME_WIDTH']+pad,gc.gc['GAME_HEIGHT']))
    boundary=bg.Boundary(screen_rect)
    boundary2=bg.Boundary(screen_rect,bounce=[True,False,True,False])
    
    ENDGAME = pygame.USEREVENT + 1
    clock=pygame.time.Clock()
    font=pygame.font.Font(None,gc.gc['FONT_SIZE'])
    font_pong=pygame.font.Font("pong-score-extended.ttf",gc.gc['FONT_SIZE']) # A pong-like font. Used in displayed text.
    font_end=pygame.font.SysFont('times',gc.gc['FONT_SIZE']*3)
    score_text_sample=font_pong.render(f'0',True,gc.gc['SCORE_COLOR'])
    
    # Make the player sprites
    asteroids=pygame.sprite.Group()
    bursts=pygame.sprite.Group()
    canisters=pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()

    
    player1=spacerace_player.PlayerShip('Ship',(gc.gc['PLAYER1_X_POSITION'],gc.gc['PLAYER_Y_START']),scale=gc.gc['PLAYER_SCALE'],control=gc.gc['PLAYER1_CONTROL'],move_speed=gc.gc['PLAYER_MOVESTEP'],player_side=1,pace=gc.gc['PLAYER_ANIM_PACE'],boundary=boundary2,image_path=__location__)
    player2=spacerace_player.PlayerShip('Ship',(gc.gc['PLAYER2_X_POSITION'],gc.gc['PLAYER_Y_START']),scale=gc.gc['PLAYER_SCALE'],control=gc.gc['PLAYER2_CONTROL'],move_speed=gc.gc['PLAYER_MOVESTEP'],player_side=2,pace=gc.gc['PLAYER_ANIM_PACE'],boundary=boundary2,image_path=__location__)
    all_sprites.add(player1,player2)

    timer_bar=timer.Timer(gc.gc['TIMER_POSITION'],(gc.gc['TIMER_DIMENSIONS'][0],gc.gc['TIMER_DIMENSIONS'][1]),gc.gc['TIMER_DURATION'],color=gc.gc['TIMER_COLOR'],orientation='down')

    asteroid_start=gc.gc['SCORE_YPOS']-score_text_sample.get_height()/2
    asteroid_stop=gc.gc['ASTEROID_MAX_HEIGHT']
    direction=1
    asteroid_type='Asteroid_old' if gc.gc['ASTEROID_OLD_TYPE'] else 'Asteroid'
    for height in range(int(asteroid_start),int(asteroid_stop),-int(gc.gc['ASTEROID_SEPARATION'])):
        asteroid_speed=(random.random()-0.5)*gc.gc['ASTEROID_SPEED_SPREAD']+gc.gc['ASTEROID_SPEED']
        off_distance=gc.gc['ASTEROID_REVIVE_TIME']/gc.gc['TICK_FRAMERATE']*asteroid_speed
        x_position=random.random()*full_width-(full_width-gc.gc['GAME_WIDTH'])/2
        if random.random()>gc.gc['CANISTER_FRACTION'] or height<gc.gc['TOP']+0.2*gc.gc['GAME_HEIGHT']:
            asteroid_i=asteroid.Asteroid(asteroid_type,(x_position,height),scale=gc.gc['ASTEROID_SCALE'],color=gc.gc['ASTEROID_COLOR'],velocity=[direction*asteroid_speed,0],boundary=boundary,image_path=__location__)
            all_sprites.add(asteroid_i)
            asteroids.add(asteroid_i)
        else:
            canister_i=asteroid.Asteroid('Canister',(x_position,height),scale=gc.gc['CANISTER_SCALE'],color=gc.gc['CANISTER_COLOR'],velocity=[direction*gc.gc['CANISTER_SPEED'],0],boundary=boundary,image_path=__location__)
            all_sprites.add(canister_i)
            canisters.add(canister_i)
        direction*=-1
    
    running = True
    pause=False
    total_time=0
    score_player=[0,0]
    step=False
    game_state=3
    game_message=''
    timer_bar.start()
    while running:
    
    
        # Did the user click the window close button?
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == ENDGAME:
                running = False
            elif event.type == gc.KEYDOWN:
                if event.key == gc.K_ESCAPE:
                    running = False
                if event.key == gc.K_p:
                    if pause:
                        pause=False
                    else:
                        pause=True
                if event.key == gc.K_RIGHTBRACKET:
                    step=True
    
        # If paused, continuously skip over the game loop (except event processing).
        # If taking one step through the loop, don't pause but unset the step
        # immediately after.
        if pause and not step:
            pygame.time.delay(16)
            continue
        if step:
            step=False
    
        if game_state==3:
            time_left=int(gc.gc['START_COUNTDOWN']+1-total_time)
            countdown=str(time_left)
            if time_left==0:
                game_state=1
                countdown=''
    
        pressed_keys = pygame.key.get_pressed()
    
        # Update the bullet positions
        for asteroid_i in asteroids:
            if game_state==1:
                asteroid_i.update()
    
        # Update the bullet positions
        for canister_i in canisters:
            if game_state==1:
                canister_i.update()
    
        for burst_i in bursts:
            burst_i.update()
    
        # Update the player position 
        for player in [player1,player2]:
            if game_state==1:
                player.update(pressed_keys,asteroids,gc.gc['GRAVITY'])
                if player.rect.bottom<0:
                    score_player[player.player_side-1]+=1
                    player.reset(wrap=True)
    
        asteroids_hit=pygame.sprite.spritecollide(player1,asteroids,False,collided=pygame.sprite.collide_mask)
        if asteroids_hit:
            if gc.gc['PLAYER_COLLISION_RESET']:
                player1.reset()
            else:
                for asteroid_i in asteroids_hit:
                    burst_i=go.Burst('Burst',(asteroid_i.position.x,asteroid_i.position.y),pace=1,scale=6,image_path=__location__)
                    bursts.add(burst_i)
                    all_sprites.add(burst_i)
                    asteroid_i.kill()
                    if not player1.powerup:
                        player1.update_motion(impulse=[gc.gc['ASTEROID_IMPULSE']*asteroid_i.velocity.x/abs(asteroid_i.velocity.x),-2*player1.velocity.y])
    
        asteroids_hit=pygame.sprite.spritecollide(player2,asteroids,False,collided=pygame.sprite.collide_mask)
        if asteroids_hit:
            if gc.gc['PLAYER_COLLISION_RESET']:
                player2.reset()
            else:
                for asteroid_i in asteroids_hit:
                    burst_i=go.Burst('Burst',(asteroid_i.position.x,asteroid_i.position.y),pace=1,scale=6,image_path=__location__)
                    bursts.add(burst_i)
                    all_sprites.add(burst_i)
                    asteroid_i.kill()
                    if not player2.powerup:
                        player2.update_motion(impulse=[gc.gc['ASTEROID_IMPULSE']*asteroid_i.velocity.x/abs(asteroid_i.velocity.x),-2*player2.velocity.y])
    
        canisters_hit=pygame.sprite.spritecollide(player1,canisters,False,collided=pygame.sprite.collide_mask)
        if canisters_hit:
            for canister_i in canisters_hit:
                canister_i.kill(fullkill=True)
                player1.set_powerup()
    
        canisters_hit=pygame.sprite.spritecollide(player2,canisters,False,collided=pygame.sprite.collide_mask)
        if canisters_hit:
            for canister_i in canisters_hit:
                canister_i.kill(fullkill=True)
                player2.set_powerup()
    
        if game_state==1:
            timer_bar.update()
    
        if timer_bar.time_left==0 and game_state==1:
            game_state=2
    
        # Fill the background
        screen.fill(gc.gc['SCREEN_COLOR'])
    
        # Update all sprites
        for entity in all_sprites:
            screen.blit(entity.surf,entity.rect)
    
        if game_state==1:
            screen.blit(timer_bar.surf,timer_bar.rect)
    
        # Display the score in the corner
        score_text_1=font_pong.render(f'{score_player[0]}',True,gc.gc['SCORE_COLOR'])
        score_text_2=font_pong.render(f'{score_player[1]}',True,gc.gc['SCORE_COLOR'])
        screen.blit(score_text_1, (gc.gc['SCORE_P1_XPOS']-score_text_1.get_width(),gc.gc['SCORE_YPOS']-score_text_1.get_height()/2))
        screen.blit(score_text_2, (gc.gc['SCORE_P2_XPOS']-score_text_2.get_width(),gc.gc['SCORE_YPOS']-score_text_2.get_height()/2))
    
        # Update the message to the user
        game_text=font_end.render(game_message,True,(255,255,255))
        screen.blit(game_text, (gc.gc['GAME_WIDTH']/2-game_text.get_width()/2,gc.gc['SCREEN_HEIGHT']*0.53-game_text.get_height()/2))
    
        # Countdown text
        countdown_text=font_pong.render(countdown,True,(255,255,255))
        screen.blit(countdown_text, (gc.gc['GAME_WIDTH']/2-game_text.get_width()/2,gc.gc['SCREEN_HEIGHT']*0.53-game_text.get_height()/2))
    
        # Flip the display
        pygame.display.flip()
    
        # Only run the timer if the game is still going
        if game_state==1 or game_state==3:
            clock.tick(gc.gc['TICK_FRAMERATE'])
            total_time=total_time+1/gc.gc['TICK_FRAMERATE']
    
        # Game finished
        if game_state==2:
            if score_player[0]>score_player[1]:
                game_message='Player 1 wins!'
            elif score_player[1]>score_player[0]:
                game_message='Player 2 wins!'
            else:
                game_message='Draw!'
            pygame.time.set_timer(ENDGAME, 2000,loops=1)
            game_state=0
    return settings_dict
    

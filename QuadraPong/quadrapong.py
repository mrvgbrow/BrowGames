#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide' 
os.environ['SDL_VIDEO_WINDOW_POS']="%d,%d" % (0,0)
import pygame
import math
import sys
from . import quadrapong_wall as wallmod
from . import quadrapong_player as player
from . import quadrapong_ball as ball
import paddlefunctions as pf
import presets
import background as bg
import settings
import menu
import gameutils
import datetime
from . import quadrapong_gameconstants as gc

def run(current_pars,settings_dict,quickstart=False,default='Original'):
    # Initialize the game, timer, and fonts
    __location__=os.path.realpath(os.path.join(os.getcwd(),os.path.dirname(__file__)))
    clock=gameutils.browgame_init(font=True,clock=True)
    presets_dict=presets.load_presets('Quadrapong')
    if not current_pars:
        preset_set=default
        gc.set_preset(presets_dict[preset_set])
        gc.scale_parameters()
    else:
        gc.set_preset(current_pars)
        preset_set=None
    settings.set_settings(settings_dict)

    # Load the menu. Continue reloading the menu until an option is selected that requests
    # the game to load.
    if not quickstart:
        back_to_main,menu_run,preset_out,current_pars=menu.run_menu('Quadrapong',settings_dict,presets_dict,preset_set,4,True,init_pars=current_pars)
        if back_to_main:
            return settings_dict,True,current_pars
        gc.set_preset(current_pars)
        gc.scale_parameters()

    current_parameters=gc.get_parameters(gc.__dir__())
    font_message=pygame.font.Font(None,36) 
    gameutils.init_sound('Sounds',["ding.mp3"])

    if settings.sets['FULLSCREEN_MODE']:
        screen = pygame.display.set_mode([gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT],pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode([gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT])
    
    # Create the player and ball sprites, add them to sprite groups for 
    # ease of processing.
    players=[]
    scores=[gc.LIVES_START]*4
    all_sprites = pygame.sprite.Group()
    players = pygame.sprite.Group()
    n_init_players=0
    for player_i in range(4):
        player_control=current_parameters['PLAYER'+str(player_i+1)+'_CONTROL']
        if player_control == "None": 
            scores[player_i]=0 
        else: 
            n_init_players+=1
        player_color=current_parameters['PLAYER'+str(player_i+1)+'_COLOR']
        if player_control=='Mouse':
            gameutils.mouse_init()
        player_obj=player.Player(player_color,player_i+1,player_control,gc.PADDLE_TYPE)
        all_sprites.add(player_obj)
        players.add(player_obj)

    life_counter_offset=gc.SCREEN_PAD+gc.WALL_WIDTH+0.12*gc.SCREEN_HEIGHT
    life_counter_offset_2=gc.SCREEN_PAD-0.012*gc.SCREEN_HEIGHT-gc.WALL_WIDTH/2-gc.SCORE_SIZE/2
    life_counter_bottom=bg.Life_Counter((life_counter_offset,gc.SCREEN_WIDTH-life_counter_offset_2),scores[3],'right',(gc.SCORE_SIZE/2,gc.SCORE_SIZE))
    life_counter_left=bg.Life_Counter((life_counter_offset_2,life_counter_offset),scores[0],'up',(gc.SCORE_SIZE,gc.SCORE_SIZE/2),separation=gc.SCORE_SIZE*3/4)
    life_counter_top=bg.Life_Counter((gc.SCREEN_WIDTH-life_counter_offset,life_counter_offset_2),scores[1],'right',(gc.SCORE_SIZE/2,gc.SCORE_SIZE))
    life_counter_right=bg.Life_Counter((gc.SCREEN_WIDTH-life_counter_offset_2,gc.SCREEN_HEIGHT-life_counter_offset),scores[2],'up',(gc.SCORE_SIZE,gc.SCORE_SIZE/2),separation=gc.SCORE_SIZE*3/4)
    life_counters=[life_counter_left,life_counter_top,life_counter_right,life_counter_bottom]
    
    balls=pygame.sprite.Group()
    balls_to_hit=[]
    
    walls=pygame.sprite.Group()
    center_walls=pygame.sprite.Group()
    for i in range(1,5):
        for j in range(1,3):
            wall=wallmod.Wall(i,j)
            all_sprites.add(wall)
            walls.add(wall)
        wall=wallmod.Wall(i,j,center=True)
        center_walls.add(wall)
    
    # Initialize variables
    running = True    # Flag indicating when to stop the game
    total_time=0      
    alive=[True,True,True,True]
    game_state=0
    ball_position_array=[]
    pause=False
    step=False
    
    while running:
    
        if game_state==0:
            game_state=1
            for i in range(gc.BALL_NUMBER):
                ball_i=ball.Ball(i)
                balls.add(ball_i)
#                if i==0: ball_i.shoot((50,60),10,600,225)
#                if i==1: ball_i.shoot((50,760),10,600,135)
                balls_to_hit.append(ball_i)
                all_sprites.add(ball_i)
    
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
    
        # Update the ball positions
        for ball_i in balls:
            scored=ball_i.update(scores)
            if scored!=None: 
                life_counters[scored].decrement_counter()
            ball_position_array.append((ball_i.x,ball_i.y))

        for iscore, score in enumerate(scores):
            if score<=0 and alive[iscore]:
                for player_i in players:
                    if player_i.player_side==iscore+1: player_i.kill()
                all_sprites.add(center_walls.sprites()[iscore])
                walls.add(center_walls.sprites()[iscore])
                alive[iscore]=False
                # If only one player is left, remove it and leave the ball bouncing
                if alive.count(False)==3 and n_init_players>1:
                    last_player_index=alive.index(True)
                    all_sprites.add(center_walls.sprites()[last_player_index])
                    walls.add(center_walls.sprites()[last_player_index])
                    alive[last_player_index]=False
                    for player_i in players:
                        if player_i.player_side==last_player_index+1: player_i.kill()
    
        # For each player, choose a ball to target, starting with the innermost player
        for player_i in players:
            if not player_i.target_ball:
                ball_targeted=pf.choose_target(player_i,balls_to_hit,gc.SCREEN_HEIGHT,gc.SCREEN_WIDTH,gc.PADDLE_LIMIT,gc.PLAYER_MOVESTEP,gc.PADDLE_LENGTH,ai_try_all=gc.AI_TRY_ALL)
                if ball_targeted:
                   balls_to_hit.remove(ball_targeted)
                   player_i.randomize_target_position()

        # Only update the AI position when the ball is moving towards it
        for player_i in players:
            player_i.update(pressed_keys,mouse_relative)
    
        gameutils.render(screen,all_sprites,gc.SCREEN_COLOR)

        if not gc.SCORE_HIDE:
            for life_counter in life_counters:
                life_counter.blit(screen)

        if gc.SHOW_BALL_TRAIL:
            gameutils.draw_trail(screen,ball_position_array)
    
        # Check whether any balls are colliding with the players.
        # If so, compute the bounce angle and change the active player
        for player_i in players:
            balls_hit=pygame.sprite.spritecollide(player_i, balls,False,collided=pygame.sprite.collide_mask)
            if balls_hit:
                for ball_hit in balls_hit:
                    if player_i.player_side!=ball_hit.player_hit:
                        if gc.ORIGINAL_BOUNCE:
                            if player_i.orientation=='vertical' and abs(ball_hit.speedx)<0.001 or player_i.orientation=='horizontal' and abs(ball_hit.speedy)<0.001:
                                ball_hit.speedx=-ball_hit.speedx
                                ball_hit.speedy=-ball_hit.speedy
                            else:
                                new_angle=pf.compute_original_angle(player_i,ball_hit,gc.PADDLE_LENGTH)
                                ball_hit.set_angle(new_angle,reference_paddle=player_i.orientation)
                        else:
                            ball_hit.bounce_wall(player_i.collision_direction)
                            anglechange=pf.compute_anglechange(player_i,ball_hit,radius=gc.PADDLE_RADIUS,paddle_length=gc.PADDLE_LENGTH,paddle_control_factor=gc.PADDLE_CONTROL_FACTOR)
                            ball_hit.anglechange(anglechange)
                        ball_hit.player_hit=player_i.player_side
                        balls_to_hit.append(ball_hit)
                        for player_j in players:
                            if player_j.target_ball==ball_hit.ball_id:
                                player_j.reset_target()
                pygame.mixer.music.play(loops=1)
    
        # Check whether any balls are colliding with the walls
        for wall_i in walls:
            balls_hit=pygame.sprite.spritecollide(wall_i, balls,False,collided=pygame.sprite.collide_mask)
            if balls_hit:
                for ball_hit in balls_hit:
                    ball_hit.bounce_wall(wall_i.collision_direction)
                    ball_hit.player_hit=-1
                    balls_to_hit.append(ball_hit)
                    for player_j in players:
                        if player_j.target_ball==ball_hit.ball_id:
                            player_j.reset_target()

        # Update the display
        pygame.display.flip()
    
        total_time=gameutils.advance_clock(clock,gc.TICK_FRAMERATE,total_time)
    
        if not balls:
            ball_position_array=[]
            game_state=0
    
    gameutils.append_scores('Quadrapong',[gc.PLAYER1_CONTROL,gc.PLAYER2_CONTROL],scores,total_time)
    
    # Stop the sound effects
    pygame.mixer.music.stop()
    
    return settings_dict,False,current_pars

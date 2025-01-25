#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide' 
os.environ['SDL_VIDEO_WINDOW_POS']="%d,%d" % (0,0)
import pygame
import sys
from . import quadrapong_wall as wallmod
from . import quadrapong_player as player
from . import quadrapong_ball as ball
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
        back_to_main,menu_run,preset_out,current_pars=menu.run_menu('Quadrapong',settings_dict,presets_dict,preset_set,True,True,init_pars=current_pars)
        if back_to_main:
            return settings_dict,True,current_pars
        gc.set_preset(current_pars)
        gc.scale_parameters()

    current_parameters=gc.get_parameters(list(current_pars.keys()))
#    font=pygame.font.Font("pong-score-extended.ttf",gc.FONT_SIZE) # A pong-like font. Used in displayed text.
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
    for player_i in range(4):
        player_control=current_parameters['PLAYER'+str(player_i+1)+'_CONTROL']
        if player_control == "None": scores[player_i]=0
        player_color=current_parameters['PLAYER'+str(player_i+1)+'_COLOR']
        if player_control=='Mouse':
            gameutils.mouse_init()
        player_obj=player.Player(player_color,player_i+1,player_control,gc.PADDLE_TYPE)
        all_sprites.add(player_obj)
        players.add(player_obj)

    life_counter_bottom=bg.Life_Counter((0.8*gc.SCREEN_WIDTH,gc.SCREEN_WIDTH-gc.SCREEN_PAD/2),gc.LIVES_START,'right',(15,15))
    life_counter_left=bg.Life_Counter((gc.SCREEN_PAD/2,0.8*gc.SCREEN_HEIGHT),gc.LIVES_START,'up',(15,15))
    life_counter_top=bg.Life_Counter((0.8*gc.SCREEN_WIDTH,gc.SCREEN_PAD/2),gc.LIVES_START,'right',(15,15))
    life_counter_right=bg.Life_Counter((gc.SCREEN_WIDTH-gc.SCREEN_PAD/2,0.8*gc.SCREEN_HEIGHT),gc.LIVES_START,'up',(15,15))
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

    
        # For each player, choose a ball to target, starting with the innermost player
        for player_i in players:
            if not player_i.target_ball:
                ball_targeted=player_i.choose_target(balls_to_hit)
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
                            new_angle=player_i.compute_original_angle((ball_hit.rect.centerx,ball_hit.rect.centery),(ball_hit.speedx,ball_hit.speedy))
                            ball_hit.set_angle(new_angle)
                        else:
                            ball_hit.bounce_wall(player_i.collision_direction)
                            anglechange=player_i.compute_anglechange([ball_hit.rect.centerx,ball_hit.rect.centery])
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

#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide' 
os.environ['SDL_VIDEO_WINDOW_POS']="%d,%d" % (0,0)
import pygame
import sys
from . import quadrapong_wall as wallmod
from . import quadrapong_player as player
from . import quadrapong_ball as ball
from . import curved_paddle
import presets
import background as bg
import settings
import menu
import gameutils
import datetime
from . import quadrapong_gameconstants as gc

def run(preset_init,settings_dict,quickstart=False):
    # Initialize the game, timer, and fonts
    __location__=os.path.realpath(os.path.join(os.getcwd(),os.path.dirname(__file__)))
    clock=gameutils.browgame_init(font=True,clock=True)
    presets_dict=presets.load_presets('Quadrapong')
    settings.set_settings(settings_dict)
    preset_set=preset_init
    gc.set_preset(presets_dict[preset_set])
    gc.scale_parameters()

    # Load the menu. Continue reloading the menu until an option is selected that requests
    # the game to load.
    if not quickstart:
        back_to_main,menu_run,preset_out,current_pars=menu.run_menu('Quadrapong',settings_dict,presets_dict,preset_set,True,True)
        if back_to_main:
            return settings_dict
        gc.set_preset(current_pars)
        gc.scale_parameters()
    current_parameters=gc.get_parameters(list(presets_dict[preset_set].keys()))

    font=pygame.font.Font("pong-score-extended.ttf",gc.FONT_SIZE) # A pong-like font. Used in displayed text.
    font_message=pygame.font.Font(None,36) 
    gameutils.init_sound(__location__,["ding.mp3"])
    font=pygame.font.Font(None,gc.FONT_SIZE)

    if settings.sets['FULLSCREEN_MODE']:
        screen = pygame.display.set_mode([gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT],pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode([gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT])
    
    # Create the player and ball sprites, add them to sprite groups for 
    # ease of processing.
    players=[]
    all_sprites = pygame.sprite.Group()
    players = pygame.sprite.Group()
    if gc.PADDLE_TYPE=='curved':
        player1=curved_paddle.CurvedPaddle(gc.PLAYER1_X_POSITION,gc.SIDE1_COLOR,1)
        player2=curved_paddle.CurvedPaddle(gc.PLAYER2_X_POSITION,gc.SIDE1_COLOR,2)
        player3=curved_paddle.CurvedPaddle(gc.PLAYER3_X_POSITION,gc.SIDE2_COLOR,3)
        player4=curved_paddle.CurvedPaddle(gc.PLAYER4_X_POSITION,gc.SIDE2_COLOR,4)
    else:
        player1=player.Player(gc.PLAYER1_COLOR,1,gc.PLAYER1_CONTROL)
        player2=player.Player(gc.PLAYER2_COLOR,2,gc.PLAYER2_CONTROL)
        player3=player.Player(gc.PLAYER3_COLOR,3,gc.PLAYER3_CONTROL)
        player4=player.Player(gc.PLAYER4_COLOR,4,gc.PLAYER4_CONTROL)
        all_sprites.add(player1,player2,player3,player4)
        players.add(player1,player2,player3,player4)

    life_counter_bottom=bg.Life_Counter((0.8*gc.SCREEN_WIDTH,gc.SCREEN_WIDTH-gc.SCREEN_PAD/2),3,'right',(15,15))
    life_counter_left=bg.Life_Counter((gc.SCREEN_PAD/2,0.8*gc.SCREEN_HEIGHT),3,'up',(15,15))
    life_counter_top=bg.Life_Counter((0.8*gc.SCREEN_WIDTH,gc.SCREEN_PAD/2),3,'right',(15,15))
    life_counter_right=bg.Life_Counter((gc.SCREEN_WIDTH-gc.SCREEN_PAD/2,0.8*gc.SCREEN_HEIGHT),3,'up',(15,15))
    life_counters=[life_counter_left,life_counter_top,life_counter_right,life_counter_bottom]
    
    balls=pygame.sprite.Group()
    balls_to_hit=[]
    
    walls=pygame.sprite.Group()
    for i in range(1,5):
        for j in range(1,3):
            wall=wallmod.Wall(i,j)
            all_sprites.add(wall)
            walls.add(wall)
    
    # Initialize variables
    running = True    # Flag indicating when to stop the game
    total_time=0      
    scores=[10,10,10,10]
    game_state=0
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
    
        # Update the ball positions
        for ball_i in balls:
            scored=ball_i.update(scores)
            if scored!=None: 
                life_counters[scored].decrement_counter()
    
        # For each player, choose a ball to target, starting with the innermost player
        for player_i in players:
            if not player_i.target_ball:
                ball_targeted=player_i.choose_target(balls_to_hit)
                if ball_targeted:
                   balls_to_hit.remove(ball_targeted)
                   player_i.randomize_target_position()

        # Only update the AI position when the ball is moving towards it
        for player_i in players:
            player_i.update(pressed_keys)
    
        gameutils.render(screen,all_sprites,gc.SCREEN_COLOR)

        for life_counter in life_counters:
            life_counter.blit(screen)
    
        # Render the score
#        if not gc.SCORE_HIDE:
    
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
            game_state=0
    
    gameutils.append_scores('Quadrapong',[gc.PLAYER1_CONTROL,gc.PLAYER2_CONTROL],scores,total_time)
    
    # Stop the sound effects
    pygame.mixer.music.stop()
    
    return settings_dict

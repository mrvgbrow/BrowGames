#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import sys
import gameutils
import os

exec_run=False
if getattr(sys,'frozen', False):
    os.chdir(sys._MEIPASS)
    exec_run=True

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide' 
#os.environ['SDL_VIDEO_WINDOW_POS']="%d,%d" % (0,0)
import pygame
import menu
import presets
import gameutils
import settings
from .import pong_player
import random
import math
from .import pong_ball as ball
from .import pong_wall as wall
from .import pong_gameconstants as gc

def run(preset_init,settings_dict,quickstart=False):
    # Initialize the game, music, timer, and screen
    __location__=os.path.realpath(os.path.join(os.getcwd(),os.path.dirname(__file__)))
    clock=gameutils.browgame_init(font=True,clock=True)
    presets_dict=presets.load_presets('Pong')
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
            back_to_main,menu_run,preset_out,current_pars=menu.run_menu('Pong',screen,settings_dict,presets_dict,preset_set,True,True)
            settings.set_settings(settings_dict)
            if back_to_main:
                return settings_dict
            gc.set_preset(presets_dict[preset_out])
            preset_set=preset_out
     
        # Scale the selected game constants and extract them as a dictionary
        gc.set_preset(current_pars)
        gc.scale_parameters()
    current_parameters=gc.get_parameters(list(presets_dict[preset_set].keys()))
    
    pygame.mixer.music.load(os.path.join(__location__,"ding.mp3"))
    font=pygame.font.Font("pong-score-extended.ttf",gc.FONT_SIZE) # A pong-like font. Used in displayed text.
    font_message=pygame.font.Font(None,36) 
    pygame.mixer.music.set_volume(settings.sets['SOUND_VOLUME'])   # Set the volume.
    
    # Initialize the various sprite groups.
    all_sprites = pygame.sprite.Group()
    players = pygame.sprite.Group()
    balls=pygame.sprite.Group()
    walls=pygame.sprite.Group()
    
    if settings.sets['FULLSCREEN_MODE']:
        screen = pygame.display.set_mode([gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT],pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode([gc.SCREEN_WIDTH, gc.SCREEN_HEIGHT])
    
    # Create the player sprites
    n_players=4
    for player_i in range(n_players):
        player_x_position=current_parameters['PLAYER'+str(player_i+1)+"_X_POSITION"]
        side=1 if player_x_position<gc.SCREEN_WIDTH/2 else 2
        player_color=current_parameters['PLAYER'+str(player_i+1)+"_COLOR"]
        player_control=current_parameters['PLAYER'+str(player_i+1)+"_CONTROL"]
        paddle_type=current_parameters['PLAYER'+str(player_i+1)+"_PADDLE_TYPE"]
    
        # if any players are using the mouse, grab exclusive input from it and make it invisible
        if player_control=='Mouse': 
            gameutils.mouse_init() 

        # Create the player instance and add it to the corresponding sprite group
        if player_control != 'None':
            player_o=pong_player.Player(player_x_position,player_color,player_i+1,player_control,side,paddle_type)
            players.add(player_o)
            all_sprites.add(player_o)
    #    if player_i == 0:
    #        player1=player_o
    
    # Create the ball sprites
    for i in range(gc.BALL_NUMBER):
        ball_i=ball.Ball()
        balls.add(ball_i)
        all_sprites.add(ball_i)
    
    # Create the wall sprites. Left and right walls not needed if a full-height goal is requested.
    top_wall=wall.Wall("top",gc.SCREEN_WIDTH/2,gc.WALL_WIDTH/2,gc.SCREEN_WIDTH,gc.WALL_WIDTH)
    bottom_wall=wall.Wall("bottom",gc.SCREEN_WIDTH/2,gc.SCREEN_HEIGHT-gc.WALL_WIDTH/2,gc.SCREEN_WIDTH,gc.WALL_WIDTH)
    sub_wall_size=(gc.SCREEN_HEIGHT-2*gc.WALL_WIDTH-gc.GOAL_SIZE)/2+gc.WALL_WIDTH
    bottom_left_wall=wall.Wall("bottom left",gc.WALL_WIDTH/2,gc.SCREEN_HEIGHT-sub_wall_size/2,gc.WALL_WIDTH,sub_wall_size)
    top_left_wall=wall.Wall("top left",gc.WALL_WIDTH/2,sub_wall_size/2,gc.WALL_WIDTH,sub_wall_size)
    bottom_right_wall=wall.Wall("bottom right",gc.SCREEN_WIDTH-gc.WALL_WIDTH/2,gc.SCREEN_HEIGHT-sub_wall_size/2,gc.WALL_WIDTH,sub_wall_size)
    top_right_wall=wall.Wall("top right",gc.SCREEN_WIDTH-gc.WALL_WIDTH/2,sub_wall_size/2,gc.WALL_WIDTH,sub_wall_size)
    if gc.GOAL_SIZE<gc.SCREEN_HEIGHT-2*gc.WALL_WIDTH:
        walls=[top_wall,bottom_wall,bottom_left_wall,bottom_right_wall,top_left_wall,top_right_wall]
        all_sprites.add(top_wall,bottom_wall,bottom_left_wall,top_left_wall,bottom_right_wall,top_right_wall)
    else:
        walls.add(top_wall,bottom_wall)
        all_sprites.add(top_wall,bottom_wall)
    
    # Initialize variables
    running = True    # Flag indicating when to stop the game
    total_time=0      
    score=[0,0]
    pause=False
    step=False
    center_line_width=2
    n_dash_center_line=30
    time_ref=0
    time_ref=1
    ball_wait=False
    ball_position_array=[]
    reset=False
    debug_string=''
    game_state=0
    
    while running:
    
        running,pause,step,reset=gameutils.process_standard_events(running,pause)
    
        # If paused, continuously skip over the game loop (except event processing).
        # If taking one step through the loop, don't pause but unset the step
        # immediately after.
        if pause and not step:
            pygame.time.delay(16)
            continue
        if step:  step=False
    
        # For each ball, determine the position where the it will intersect with
        # the horizontal positions of player 1 and player 2. This is used by the
        # AI to decide where to move.
        for ball_i in balls:
            kill_case=ball_i.update()
            if kill_case==-1:
                score[1]+=1
                ball_i.kill()
            elif kill_case==1:
                score[0]+=1
                ball_i.kill()
            elif kill_case==2:
                for player in players:
                    player.target=None
            for side in range(2):
                if score[side]>=gc.SCORE_MAX:
                    win_text=font_message.render('Player '+str(side+1)+' Wins!',True,(255,255,255))
                    game_state=1
                    time_ref_1=total_time
            ball_position_array.append((ball_i.x,ball_i.y))
    
    
        # Always allow player movement when human controlled. Only update the AI position when the ball is moving towards it.
        # Pressed keys are used to control the players.
        pressed_keys = pygame.key.get_pressed()
        mouse_relative = pygame.mouse.get_rel()
        for player in players:
            ball_side=1 if ball_i.speedx<0 else 2
            if not (ball_side!=player.side and player.control == 'Computer'):
                player.update(pressed_keys,mouse_relative,balls)
    
    
        gameutils.render(screen,all_sprites,gc.SCREEN_COLOR)
    
        # Render the score, if requested 
        if not gc.SCORE_HIDE:
    #        score_text=font.render(f'Player1: {score[0]}  Player2: {score[1]}',True,(255,255,255))
            score_text1=font.render(f'{score[0]}',True,(255,255,255))
            score_text2=font.render(f'{score[1]}',True,(255,255,255))
    #        screen.blit(score_text, (gc.SCORE_XPOS,gc.SCORE_YPOS))
            screen.blit(score_text1, (0.23*gc.SCREEN_WIDTH,gc.SCORE_YPOS))
            screen.blit(score_text2, (0.73*gc.SCREEN_WIDTH,gc.SCORE_YPOS))
    
        # Render the clock, if requested
        if not gc.TIME_HIDE:
            gameutils.show_time(total_time,font_message,screen,(gc.TIME_XPOS,gc.TIME_YPOS)) 

        gameutils.show_debug("",font_message,screen,(gc.SCREEN_HEIGHT/2,gc.SCREEN_WIDTH/2))
    
        # Show the trail of the ball, if requested. The trail resets with every point.
        if gc.SHOW_BALL_TRAIL:
            for ball_position in ball_position_array:
                if ball_position[0]>0 and ball_position[1]>0:
                    pygame.draw.circle(screen, (255,255,255),ball_position,1)
    
        # Show the court center line, if requested.
        if not gc.CENTER_LINE_HIDE:
            for center_count in range(n_dash_center_line):
                y_pos=gc.SCREEN_HEIGHT/n_dash_center_line*center_count
                pygame.draw.rect(screen,(255,255,255),(gc.SCREEN_WIDTH/2-center_line_width/2,y_pos,center_line_width,gc.SCREEN_HEIGHT/n_dash_center_line/2))
    
        # Check whether any balls are colliding with a player. If so, compute
        # the bounce angle and change the active player
        for player_object in players:
            balls_hit=pygame.sprite.spritecollide(player_object, balls,False,collided=pygame.sprite.collide_mask)
            if balls_hit:
                for player in players:
                    player.target=None
                for ball_hit in balls_hit:
                    if ball_hit.player_hit!=player_object.player_id:
                        pygame.mixer.music.play(loops=1)
                        direction='right' if ball_hit.speedx<0 else 'left'
                        anglesign=1 if ball_hit.speedx<0 else -1
                        if gc.ORIGINAL_BOUNCE:
                          new_angle=player_object.compute_original_angle(ball_hit.rect.centery,ball_hit.speedx)
                          ball_hit.set_angle(new_angle)
                        else:
                          ball_hit.bounce_wall(direction)
                          anglechange=anglesign*player_object.compute_anglechange(ball_hit.rect.centery)
                          ball_hit.anglechange(anglechange)
                        player_object.target=None
                        ball_hit.player_hit=player_object.player_id
    
        # Check whether any balls are colliding with the walls
        for this_wall in walls:
            balls_hit=pygame.sprite.spritecollide(this_wall, balls,False,collided=pygame.sprite.collide_mask)
            if balls_hit:
                for ball_hit in balls_hit:
                    pygame.mixer.music.play(loops=1)
                    ball_hit.player_hit=0
                    if this_wall.name=="top":
                        ball_hit.bounce_wall("down")
                    elif this_wall.name=="bottom":
                        ball_hit.bounce_wall("up")
                    elif "left" in this_wall.name:
                        ball_hit.bounce_wall("right")
                    elif "right" in this_wall.name:
                        ball_hit.bounce_wall("left")
                for player in players:
                    player.target=None
    
    
        # If no balls remain on the field, increment the score for the player
        # whose turn it *isn't*
        if not balls and game_state==0:
    
            ball_position_array=[]
            # This code is used for testing different ball trajectories
    #        for i in range(1):
    #          ball_0=ball.Ball()
    #          vertical_shift=-gc.PLAYER_HEIGHT/3.35+float(score_side2+score_side1)*gc.PLAYER_HEIGHT/10
    #          ball_0.shoot((gc.SCREEN_WIDTH/2-10,gc.WALL_WIDTH),10,300,250)
    #          balls.add(ball_0)
    #          all_sprites.add(ball_0)
    #        for player in players:
    #            player.target=None
    
            # If there are no balls, set a wait flag and a reference time. 
            if time_ref<total_time and not ball_wait:
                time_ref=total_time
                ball_wait=True
            # If there are no balls and the specified wait time has elapsed, serve the next ball.
            if total_time-time_ref>gc.BALL_WAIT and ball_wait:
                ball_wait=False
                ball_0=ball.Ball()
                balls.add(ball_0)
                all_sprites.add(ball_0)
                for player in players:
                    player.target=None
    
        # If the game has been won by one of the players, display the end game message.. After 3 seconds, the game will close.
        if game_state==1:
            screen.blit(win_text, (gc.SCREEN_WIDTH/2-win_text.get_width()/2,gc.SCREEN_HEIGHT*0.53-win_text.get_height()/2))
            if total_time-time_ref_1>3:
                running=False
    
        # If the user requested a score reset, set both scores to 0.
        if reset:
            score[0]=0
            score[1]=0
            reset=False
    
        # Update the display
        pygame.display.flip()
    
        # Move the clock forward by a tick
        total_time=gameutils.advance_clock(clock,gc.TICK_FRAMERATE,total_time)
    
    gameutils.append_scores('Pong',[gc.PLAYER1_CONTROL,gc.PLAYER2_CONTROL],score,total_time)
    # Stop the sound effects
    pygame.mixer.music.stop()
    return settings_dict
    

#!/c/Users/sp4ce/AppData/Local/Programs/Python/Python310/python

import os
import sys
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide' 
#os.environ['SDL_VIDEO_WINDOW_POS']="%d,%d" % (0,0)
import pygame
import presets
import settings
import copy
import timer
import re
import genutils as genu
import gameutils
from . import gotcha_player as gplayer
import computer_player as cp
import random
from . import gotcha_gameconstants as gc
import background as bg
import mazefunctions as mf
import gameobject as go
import menu

def run(current_pars,settings_dict,quickstart=False,default='Original'):
    __location__=os.path.realpath(os.path.join(os.getcwd(),os.path.dirname(__file__)))
    gc.gc,sdict=gc.make_shortcuts(gc.gc)
    gc.gc=gc.process_game_arguments(sys.argv,gc.gc,sdict)
    
    clock=gameutils.browgame_init(font=True,clock=True)
    presets_dict=presets.load_presets('Gotcha')
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
        back_to_main,menu_run,preset_out,current_pars=menu.run_menu('Gotcha',settings_dict,presets_dict,preset_set,5,False,init_pars=current_pars,n_computer_players=4)
        if back_to_main:
            return settings_dict,True,current_pars
     
        # Scale the selected game constants and extract them as a dictionary
        gc.set_preset(current_pars)
        gc.scale_parameters()

    screen=gameutils.set_screen(gc.gc)
    screen_rect=pygame.Rect((0,0),(gc.gc['SCREEN_WIDTH'],gc.gc['SCREEN_HEIGHT']))
    game_rect=pygame.Rect((gc.gc['LEFT'],gc.gc['TOP']),(gc.gc['GAME_WIDTH'],gc.gc['GAME_HEIGHT']))
    panel=pygame.Surface((gc.gc['GAME_WIDTH'],gc.gc['SCREEN_HEIGHT']-gc.gc['GAME_HEIGHT']))
    panel_rect=panel.get_rect(left=0,top=0)
    border=bg.Border(game_rect,thick=gc.gc['BORDER_THICK'])
    
    maze_sprites=mf.make_full_mazes(gc.gc['GAME_WIDTH'],gc.gc['GAME_HEIGHT'],gc.gc['TOP'],
                                    gc.gc['BORDER_THICK'],gc.gc['SCREEN_COLOR'],gc.gc['MAZE_COLOR'],
                                    gc.gc['NUMBER_TILES_X'],gc.gc['NUMBER_TILES_Y'],image_path=__location__)
    maze_irect=maze_sprites[0].surf.get_rect(left=0,top=0)
    maze_srect=maze_sprites[0].surf.get_rect(left=gc.gc['BORDER_THICK'],top=gc.gc['TOP']+gc.gc['BORDER_THICK'])
    
    boundary=bg.Boundary(maze_srect,stop=[True,True,True,True])
    
    ENDGAME = pygame.USEREVENT + 1
    POINTSCORED=pygame.USEREVENT+2
    font=pygame.font.Font(None,gc.gc['FONT_SIZE'])
    font_pong=pygame.font.Font("pong-score-extended.ttf",gc.gc['FONT_SIZE']) # A pong-like font. Used in displayed text.
    font_end=pygame.font.SysFont('times',gc.gc['FONT_SIZE']*3)
    
    tracer=bg.Tracer(screen)
    
    # Make the player sprites
    players=[]
    all_sprites = pygame.sprite.Group()
    mz_sprites = pygame.sprite.Group()
    
    timer_digits=timer.Timer((gc.gc['TIMER_POSITION_X'],gc.gc['TIMER_POSITION_Y']),(gc.gc['TIMER_WIDTH'],gc.gc['TIMER_LENGTH']),gc.gc['TIMER_DURATION'],color=gc.gc['TIMER_COLOR'],ttype='digits',font=font_pong)
    print(timer_digits.rect.centerx,timer_digits.rect.centery,flush=True)
    
    computer_idx=0
    controllers=[]
    for i in range(gc.gc['PLAYER_NUMBER']):
        player_number=i+1
        if i==0:
            player_name='Player1'
        else:
            player_name='Player2'
        key_mode=gc.gc['PLAYER'+str(i+1)+'_CONTROL']
        if key_mode=='None': continue
        start_position=(334-167*i,894)
        start_position=(gc.gc['PLAYER'+str(i+1)+'_START_X'],gc.gc['PLAYER'+str(i+1)+'_START_Y'])
    #    start_position=(random.random()*gc.gc['GAME_WIDTH'],gc.gc['TOP']+random.random()*gc.gc['GAME_HEIGHT'])
        player_i=go.PlayerFixed(player_name,start_position,
                                scale=gc.gc['PLAYER_SCALE'],key_mode=key_mode,
                                control_step=[gc.gc['PLAYER_MOVESTEP'],gc.gc['PLAYER_MOVESTEP'],
                                              gc.gc['PLAYER_MOVESTEP'],gc.gc['PLAYER_MOVESTEP']],
                                player_side=player_number,boundary=boundary,
                                velocity=[0,0],image_path=__location__)
        if re.match('Computer',key_mode):
            computer_idx+=1
            controller_i=gplayer.GotchaPlayer(gc.gc['PLAYER'+str(i+1)+'_CONTROL'],sprite=player_i,
                                              movestep=gc.gc['PLAYER_MOVESTEP'],
                                              checkstep=gc.gc['PLAYER_MOVESTEP']*3,maxdepth=300)
            controllers.append(controller_i)
            tracer.add(player_i)
            player_i.move_mode='Computer'
            player_i.controller=controller_i
        players.append(player_i)
        all_sprites.add(player_i)
    all_sprites.add(border)
    computer_keys_init=cp.build_keys(controllers)
    
    mazepart_sprites=[]
    running = True
    pause=True
    total_time=0
    score_player=0
    step=False
    show_trace=False
    check_coords=False
    game_state=3   # 0 - game ending, 1 - game playing, 2 - time expired, 3 - initial countdown, 4 - point scored
    maze_line_1=0
    maze_line_2=gc.gc['GAME_HEIGHT']*0.6
    countdown=float(gc.gc['START_COUNTDOWN']+1)
    game_message=''
    timer_digits.start()
    while running:
    
        maze_line_1+=gc.gc['MAZE_CHANGE_SPEED']
        maze_line_2+=gc.gc['MAZE_CHANGE_SPEED']
        if maze_line_1>=maze_srect.height*1.2:
            maze_line_1=0
        if maze_line_2>=maze_srect.height*1.2:
            maze_line_2=0
        mz_sprites.remove(mazepart_sprites)
        mazepart_sprites=mf.make_combined_maze(maze_sprites,maze_srect,maze_line_1,maze_line_2,gc.gc['SCREEN_COLOR'],image_path=__location__)
        mz_sprites.add(mazepart_sprites)
    
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
                if event.key == gc.K_c:
                    if check_coords:
                        check_coords=False
                    else:
                        check_coords=True
                if event.key == gc.K_RIGHTBRACKET:
                    step=True
            elif event.type == POINTSCORED:
                game_state=1
                for player_i in players:
                    new_position=[maze_srect.left+random.random()*maze_srect.width,
                                  maze_srect.top+random.random()*maze_srect.height]
                    player_i.position=pygame.math.Vector2(new_position)
    
        # If paused, continuously skip over the game loop (except event processing).
        # If taking one step through the loop, don't pause but unset the step
        # immediately after.
        if pause and not step:
            pygame.time.delay(16)
            continue
        if step:
            step=False
    
        if check_coords:
            mouse_pos=pygame.mouse.get_pos()
            game_message=str(mouse_pos[0])+','+str(mouse_pos[1])
        else:
            game_message=''
    
    
        if game_state==3:
            time_left=int(gc.gc['START_COUNTDOWN']+1-total_time)
            game_message=str(time_left)
            if time_left==0:
                game_state=1
                game_message=''
    
        pressed_keys = pygame.key.get_pressed()
    
        # Fill the background
        screen.fill(gc.gc['SCREEN_COLOR'])
    
        if show_trace:
            tracer.draw()
    
    
        if game_state!=4:
            for maze_piece in mz_sprites:
                screen.blit(maze_piece.surf,maze_piece.rect)
    
        computer_keys=copy.deepcopy(computer_keys_init)
        for controller_i in controllers:
            controller_i.play(computer_keys,screen,players[0])
    
        # Update the player positions
        for player_i in players:
            if game_state==1:
                direction=player_i.update_all(pressed_keys,computer_keys=computer_keys)
                maze_hit=pygame.sprite.spritecollide(player_i,mazepart_sprites,False,collided=pygame.sprite.collide_mask)
                if maze_hit:
                    if player_i.controller:
                        player_i.controller.force_decide()
                    direction=pygame.math.Vector2(direction[0],direction[1])
                    if direction.magnitude()>0:
                        bump=-direction*gc.gc['PLAYER_MAZE_BUMP']
                        player_i.update_position([bump[0],bump[1]])
                    else:
                        bump=pygame.math.Vector2(0,gc.gc['PLAYER_MAZE_BUMP'])
                        player_i.update_position([bump[0],bump[1]])
    
        # Players have collided, score a point and change game state
        if game_state==1:
            players_hit=pygame.sprite.spritecollide(players[0],players[1:],False,collided=pygame.sprite.collide_mask)
            if players_hit:
                for player_hit in players_hit:
                    game_state=4
                    score_player+=1
                    pygame.time.set_timer(POINTSCORED,gc.gc['WAIT_POINTSCORED']*1000,loops=1)
    
        if game_state==1:
            timer_digits.update(framerate=gc.gc['TICK_FRAMERATE'])
    
        if timer_digits.time_left==0 and game_state==1:
            game_state=2
    
    
        # Fill the panel
        panel.fill(gc.gc['PANEL_COLOR'])
    
        screen.blit(panel,panel_rect)
    
        if show_trace:
            screen.blit(tracer,screen_rect)
    
        # Update all sprites
        if game_state != 4:
            for entity in all_sprites:
                screen.blit(entity.surf,entity.rect)
    
        if game_state==1:
            screen.blit(timer_digits.surf,timer_digits.rect)
    
        # Display the score in the corner
        if game_state != 4:
            score_text=font_pong.render(f'{score_player}',True,gc.gc['SCORE_COLOR'])
            screen.blit(score_text, (gc.gc['GAME_WIDTH']/4-score_text.get_width()/2,(gc.gc['SCREEN_HEIGHT']-gc.gc['GAME_HEIGHT'])/2-score_text.get_height()/2))
    
            # Update the message to the user
            game_text=font_end.render(game_message,True,(0,250,0))
            screen.blit(game_text, (gc.gc['GAME_WIDTH']/2-game_text.get_width()/2,gc.gc['SCREEN_HEIGHT']*0.53-game_text.get_height()/2))
    
        # Flip the display
        pygame.display.flip()
    
        # Only run the timer if the game is still going
        if game_state==1 or game_state>=3:
            clock.tick(gc.gc['TICK_FRAMERATE'])
            total_time=total_time+1/gc.gc['TICK_FRAMERATE']
    
        # Game finished
        if game_state==2:
            game_message='Game Over!'
            pygame.time.set_timer(ENDGAME, 2000,loops=1)
            game_state=0
    
    return settings_dict,False,current_pars

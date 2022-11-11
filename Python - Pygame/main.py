import pygame, sys
from button import Button
from pygame.math import Vector2
pygame.init()

# Screen resolution, title, clock, fps
WIDTH = 1000
HEIGHT = 850
FPS = 25
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodger Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 32)
start_time = pygame.time.get_ticks() 

#Flying Object Events
speedupOBJ = pygame.USEREVENT + 0
speedupOBJ2 = pygame.USEREVENT + 1
speedupOBJ3 = pygame.USEREVENT + 2
speedupOBJ4 = pygame.USEREVENT + 3
pygame.time.set_timer(speedupOBJ, 4000)
pygame.time.set_timer(speedupOBJ2, 6000)
pygame.time.set_timer(speedupOBJ3, 9000)
pygame.time.set_timer(speedupOBJ4, 12000)

# Background variables
MBG = pygame.image.load("images/Menu_background.png").convert()
CBG = pygame.image.load("images/Credits_background.png").convert()
ESBG = pygame.image.load("images/gameover.png").convert()

# Color variables
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 225)


def get_font(size):
    return pygame.font.Font("assets/font.ttf", size)

def play():
    OBJ_SPEED = 15
    HEALTHSCORE = 15

    # defining image used for Playericon
    pl_icon = pygame.image.load("images/pl_circle.png").convert_alpha()
    pl_icon_rect = pl_icon.get_rect(bottomleft=(500, 500))
    #------------------------------------------------

    # defining image used for OBJ icon
    obj_icon = pygame.image.load("images/ob_circle.png").convert_alpha()
    obj_icon_rect = obj_icon.get_rect()
    #defining image used for another OBJ
    obj2_icon = pygame.image.load("images/ob_circle.png").convert_alpha()
    obj2_icon_rect = obj2_icon.get_rect()
    
    #------------------------------------------------

    # defining image used for background
    bg = pygame.image.load("images/background.png")
    gameover = pygame.image.load("images/gameover.png")
    bg_dmg = pygame.image.load("images/dmg_background.png")
    bg_paused = pygame.image.load("images/paused_background.png")
    replay_button = pygame.image.load("images/play-button.png")

    # Music and sound
    music = pygame.mixer.music.load('assets/BGMUSIC.mp3')
    pygame.mixer.music.play(-1,0.0)
    bounceFX = pygame.mixer.Sound('assets/objbounce.mp3')
    bounceFX.set_volume(0.4)
    DamageFX = pygame.mixer.Sound('assets/DamageNoise.wav')
    DamageFX.set_volume(0.3)
    gameoverFX = pygame.mixer.Sound('assets/gameover.wav')
    gameoverFX.set_volume(0.2)

    # Scoreboard
    scorex = 10
    scorey = 10
    HScore = HEALTHSCORE
    font = pygame.font.Font('freesansbold.ttf',32)
    def showscore(x,y):
        score = font.render("LIFE :" + str(HScore),True,(WHITE))
        SCREEN.blit(score, (x, y))

    # Non player Object Bounce Movement:
    def obj_bounce (speed_tuple, obj_position):
        # Did the object hit the left side?
        if obj_position.left <= 0:
            speed_tuple[0] = OBJ_SPEED
            bounceFX.play(0)
        # Did the object hit the right side?
        elif obj_position.right >= WIDTH: #maximum X
            speed_tuple[0] = -OBJ_SPEED
            bounceFX.play(0)
    #             -----------------------
        # Did the object hit the top?
        if obj_position.top <= 0:
            speed_tuple[1] = OBJ_SPEED
            bounceFX.play(0)
        # Did the topic hit the bottom?
        elif obj_position.bottom >= HEIGHT: #maximum Y
            speed_tuple[1] = -OBJ_SPEED
            bounceFX.play(0)


    obj_speed = [OBJ_SPEED, OBJ_SPEED]
    #------------------------------------------------------------

    def obj2_bounce (speed_tuple, obj2_position):
        # Did the object hit the left side?
        if obj2_position.left <= 0:
            speed_tuple[0] = OBJ_SPEED
            bounceFX.play(0)
        # Did the object hit the right side?
        elif obj2_position.right >= WIDTH: #maximum X
            speed_tuple[0] = -OBJ_SPEED
            bounceFX.play(0)
    #-----------------------------------------------------------
        # Did the object hit the top?
        if obj2_position.top <= 0:
            speed_tuple[1] = OBJ_SPEED
            bounceFX.play(0)
        # Did the topic hit the bottom?
        elif obj2_position.bottom >= HEIGHT: #maximum Y
            speed_tuple[1] = -OBJ_SPEED
            bounceFX.play(0)


    obj2_speed = [OBJ_SPEED + 3, OBJ_SPEED + 3 ]

    # Dimensions of the player object
    player_width = pl_icon_rect.width
    player_height = pl_icon_rect.height

    # Speed of the player object
    player_speed = 12

    # All sprites
    all_sprites = pygame.sprite.Group()
    sprites_with_trails = pygame.sprite.Group()

    # OBJTRAIL (trail)
    class OBJ(pygame.sprite.Sprite):

        def __init__(self, pos, *groups):
            super().__init__(*groups)
            self.image = pygame.image.load("images/ob_circle.png").convert_alpha()
            #self.image.fill(pg.Color('sienna1'))
            self.rect = self.image.get_rect(center=pos)
            # A separate image for the trail (just a single-color circle).
            self.trail_image = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(self.trail_image, pygame.Color(WHITE), (20, 20), 20)
            self.trail_rect = self.trail_image.get_rect()

            self.vel = Vector2(0, 0)
            self.pos = Vector2(pos)

        def update(self, new_position=None):
            if new_position:
                self.rect.center = new_position
                self.trail_rect.center = self.rect.center
            # self.pos += self.vel
            # self.rect.center = self.pos
            # # Update the rect of the trail as well, because we'll blit it there.


    # Object with Trail
    alpha_surf = pygame.Surface(SCREEN.get_size(), pygame.SRCALPHA)
    Object = OBJ((200,200), all_sprites, sprites_with_trails)

    # Player object current co-ordinates
    x = pl_icon_rect.x
    y = pl_icon_rect.y

    #Pause mechanic
    def pause():

        paused = True

        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        paused = False

                    elif event.key -- pygame.K_q:
                        pygame.quit()
                        quit()

            pygame.display.update()
            clock.tick(5)


    #original While Loop
    run = True
    while run:
        # Create time delay of 10ms
        pygame.time.delay(10)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == speedupOBJ:
                OBJ_SPEED = 30
                obj_icon = pygame.image.load("images/ob_circle2.png").convert_alpha()
                
                print("object sped up")

            elif event.type == speedupOBJ2:
                OBJ_SPEED = 50
                obj_icon = pygame.image.load("images/ob_circle.png").convert_alpha()
                print("object sped up again")
            
            elif event.type == speedupOBJ3:
                OBJ_SPEED = 15
                obj_icon = pygame.image.load("images/ob_circle.png").convert_alpha()
                print("object slowed down")
            
            elif event.type == speedupOBJ4:
                OBJ_SPEED = 65
                obj_icon = pygame.image.load("images/ob_circle.png").convert_alpha()
                print("object super speed")
            

        # Stores keys pressed
        keys = pygame.key.get_pressed()

            #PLAYERCONTROLS=============================================================================================
        # If left arrow key is pressed
        if keys[pygame.K_LEFT] and x>0:
            x -= player_speed

        # If right arrow key is pressed
        if keys[pygame.K_RIGHT] and x<1000-player_width:
            x += player_speed

        # If up arrow key is pressed
        if keys[pygame.K_UP] and y>0:
            y -= player_speed

        # If down arrow key is pressed
        if keys[pygame.K_DOWN] and y<850-player_height:
            y += player_speed

        if keys[pygame.K_p] :
            SCREEN.blit(bg_paused,(0, 0))
            pause()

        if keys[pygame.K_ESCAPE] :
            pass

        pl_icon_rect.x = x
        pl_icon_rect.y = y

        # Non player objects on the screen, also seen as a rectangle.
        obj_bounce(obj_speed, obj_icon_rect)
        obj_icon_rect = obj_icon_rect.move(obj_speed)

        obj2_bounce(obj2_speed, obj2_icon_rect)
        obj2_icon_rect = obj2_icon_rect.move(obj2_speed)

        #updating OBJ to display with sprite with trail.
        for sprite in sprites_with_trails:
            sprite.update(obj_icon_rect.center)


        # Collision
        if pl_icon_rect.colliderect(obj_icon_rect):
            pygame.draw.rect(SCREEN, RED, pl_icon_rect,4)

        # Damage Indicator
        if pl_icon_rect.colliderect(obj_icon_rect):
            SCREEN.blit(bg_dmg,(0, 0))
            DamageFX.play(0)
            HScore = HScore - 1
        else :SCREEN.blit(bg, (0, 0))

        # If player is dead (0 life), it goes to endscreen
        if HScore <= 0:
            gameoverFX.play(0)
            endscreen()


        showscore(scorex,scorey)
        alpha_surf.fill((255, 255, 255, 244), special_flags=pygame.BLEND_RGBA_MULT)

        all_sprites.update()

        # Blit the trails onto the alpha_surf.
        for sprite in sprites_with_trails:
            alpha_surf.blit(sprite.trail_image, sprite.trail_rect)
        SCREEN.blit(alpha_surf, (0, 0))  # Blit the alpha_surf onto the screen.
        all_sprites.draw(SCREEN)  # Draw the objects onto the alpha_surf.

        #Timer
        if run == True:
            counting_time = pygame.time.get_ticks() - start_time

            # change milliseconds into minutes, seconds, milliseconds
            counting_minutes = str(counting_time/60000).zfill(2)
            counting_seconds = str( (counting_time%60000)/1000 ).zfill(2)
            counting_millisecond = str(counting_time%1000).zfill(3)
            counting_string = "%s:%s:%s" % (counting_minutes, counting_seconds, counting_millisecond)

            counting_text = font.render(str(counting_string), 1, (255,255,255))
            counting_rect = counting_text.get_rect(topright = SCREEN.get_rect().topright)

        SCREEN.blit(counting_text, counting_rect)
        SCREEN.blit(obj_icon, obj_icon_rect,)
        SCREEN.blit(obj2_icon, obj2_icon_rect,)
        SCREEN.blit(pl_icon, pl_icon_rect)

        

        SCREEN.blit(counting_text, counting_rect)



        pygame.display.update()
        clock.tick(FPS)


def credits():
    while True:
        CREDITS_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.blit(CBG, (0, 0))

        CREDITS_BACK = Button(image=None, pos=(500, 700),
                            text_input="BACK", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        CREDITS_BACK.changeColor(CREDITS_MOUSE_POS)
        CREDITS_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if CREDITS_BACK.checkForInput(CREDITS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def main_menu():
    while True:
        SCREEN.blit(MBG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        PLAY_BUTTON = Button(image=pygame.image.load("images/Play Rect.png"), pos=(500, 400),
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        CREDITS_BUTTON = Button(image=pygame.image.load("images/Credits Rect.png"), pos=(500, 550),
                            text_input="CREDITS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("images/Quit Rect.png"), pos=(500, 700),
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        for button in [PLAY_BUTTON, CREDITS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if CREDITS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    credits()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def endscreen():
    while True:
        MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.blit(ESBG, (0, 0))

        REPLAY_BUTTON = Button(image=None, pos=(225, 700),
                    text_input="RETRY", font=get_font(50), base_color="BLACK", hovering_color="#595959")
        MENU_BUTTON = Button(image=None, pos=(500, 700),
                    text_input="MENU", font=get_font(50), base_color="BLACK", hovering_color="#595959")
        QUIT_BUTTON = Button(image=None, pos=(775, 700),
                            text_input="QUIT", font=get_font(50), base_color="BLACK", hovering_color="#595959")

        for button in [REPLAY_BUTTON, MENU_BUTTON, QUIT_BUTTON]:
            button.changeColor(MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if REPLAY_BUTTON.checkForInput(MOUSE_POS):
                    play()
                if MENU_BUTTON.checkForInput(MOUSE_POS):
                    main_menu()
                if QUIT_BUTTON.checkForInput(MOUSE_POS):
                    pygame.quit()
                    sys.exit

        pygame.display.update()

main_menu()

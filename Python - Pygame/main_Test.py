import pygame
import Enemyclasses
#import GameOver
from pygame.sprite import Sprite, Group, collide_rect
pygame.init()


# Screen/display dimensions, and title
SCREEN_W = 1000 #X = Width
SCREEN_H = 850 #Y = Height
OBJ_SPEED = 30
GAME_SPEED = 60
HEALTH = 3

# COLORS IF APPLICABLE:
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN =(0, 255, 0)
BLUE = (0, 0, 225)

SCREEN = pygame.display.set_mode((SCREEN_W, SCREEN_H)) # (X,Y)
pygame.display.set_caption("Top Team Project")
clock = pygame.time.Clock()

# [OBJECTS SECTION]______________________________________________________________________
# defining image used for Playericon
pl_icon = pygame.image.load("images/pl_circle.png").convert_alpha()
pl_icon_rect = pl_icon.get_rect(topleft=(200,200))

#------------------------------------------------
# defining image used for OBJ icon
obj_icon = pygame.image.load("images/ob_circle.png").convert_alpha()
obj_icon_rect = obj_icon.get_rect()
#------------------------------------------------
# defining image used for ENEMY icon
en_icon = pygame.image.load("images/ob_circle.png").convert_alpha()
en_icon_rect = en_icon.get_rect()
#defining image used for background
bg = pygame.image.load("images/background.png")
bg_damage = pygame.image.load("images/dmg_background.png")
gameover = pygame.image.load("images/gameover.png")

#OBJ CLASS SPRITE EXPERIMENT=========================================

#Background Class Experiment:=========================================================
#class

#====================================================================
#Non player Object Bounce Movement:
def obj_bounce (speed_tuple, obj_position):
    # Did the object hit the left side?
    if obj_position.left <= 0:
        speed_tuple[0] = OBJ_SPEED
    # Did the object hit the right side?
    elif obj_position.right >= SCREEN_W: #maximum X
        speed_tuple[0] = -OBJ_SPEED
#-----------------------------------------------------------
    # Did the object hit the top?
    if obj_position.top <= 0:
        speed_tuple[1] = OBJ_SPEED
    # Did the topic hit the bottom?
    elif obj_position.bottom >= SCREEN_H: #maximum Y
        speed_tuple[1] = -OBJ_SPEED

obj_speed = [OBJ_SPEED, OBJ_SPEED]
#=================================================================================================================================================
#======Q======== Game Pause Function:









#================================================================================================================================================
# ----Q------ 
# i made the variables xy and height width equal to the player xy heightwidths cuz we wanna link our player object 
# to the pl_icon_rect data
# --------Q------------
# Player object current co-ordinates
x = pl_icon_rect.x
y = pl_icon_rect.y

# Dimensions of the player object
player_width = pl_icon_rect.width
player_height = pl_icon_rect.height

# Speed of the player object
player_speed = 9

#all_sprites = pygame.sprite.Group()
#player = OBJ_COL
#all_sprites.add(player)

# [GAME SECTION]________________________________________________________________________
# Indicate Pygame is running

RUNNING, PAUSE = 0, 1
state = RUNNING

pygame.font.Font('freesansbold.ttf', 32)
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('The Game is Paused', True, WHITE, BLUE)
textRect = text.get_rect()
textRect.center = (SCREEN_W // 2, SCREEN_H // 2)

# The infinite loop (the game)
while True:
    # Create time delay of 10ms
    #pygame.time.delay(10)
    
    # Repetition of the list of event objects that was returned by pygame.event.get() method.
    for event in pygame.event.get():
        
        # This quits the game and program if the player wishes to quit.
        if event.type == pygame.QUIT: break
        if event.type == pygame.KEYDOWN: #game Pause Experiment
            if event.key == pygame.K_p: state = PAUSE
            if event.key == pygame.K_s: state = RUNNING
    #else:
    SCREEN.fill((0, 0, 0))

    if state == RUNNING:

        # Stores keys pressed
            keys = pygame.key.get_pressed()
            #if left arrow key is pressed
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
        
        
            #===Q: I deleted this one and replace it with a player icon.
            # PLAYER OBJECT on screen, rectangle in this case. You can change the scales above in variables.
            # pygame.draw.rect(SCREEN, (255, 0, 255), (x, y, player_width, player_height)

            #-------Q---------
            # since were in the for loop right now whatever changes here will get updated in the game in real time
            # thats how the movement works theyre just changing the position of the icons on the screen in real time same with the rectangle on top
            # with the code on the bottom here im changing the xy positions of the player icon and those get changed dependent on the movement code 
            pl_icon_rect.x = x
            pl_icon_rect.y = y

            #=============================================================================================================
            # Non player objects on the screen, also seen as a rectangle.
            obj_bounce(obj_speed, obj_icon_rect)
            print(pl_icon_rect)
            obj_icon_rect = obj_icon_rect.move(obj_speed)

            #==Q=== COLLISION
            #Succesful Collision Test :)====================================================================================================
            if pl_icon_rect.colliderect(obj_icon_rect):
                pygame.draw.rect(SCREEN, RED, pl_icon_rect,4)

            #Background and gameover screen
            if pl_icon_rect.colliderect(obj_icon_rect):
                SCREEN.blit(bg_damage,(0, 0))
            else :SCREEN.blit(bg, (0, 0))

    elif state == PAUSE:
        SCREEN.blit(text, textRect)
        
    
    
    
    SCREEN.blit(obj_icon, obj_icon_rect,)
    SCREEN.blit(pl_icon, pl_icon_rect)
    

    #if collide_rect(obj_icon, logo2):
        #logo.reverse()
        #logo2.reverse()

    #new tick loop for the bounce.
    clock.tick(GAME_SPEED)
 
    # Refreshes the window
    pygame.display.update()


# Closes the pygame window
pygame.quit()
  
    


    #=============SUGGESTIONS===================# (write name and then suggestion)
    #Quincy:
    #Yall, I think we should research classes on this one. for orgnization and modular workflow in a way.
    #we might be able to define each type of moving object in the same class
    #and then change their functions. I sent some links in the discord.



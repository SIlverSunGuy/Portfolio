import pygame
from pygame.sprite import Group, collide_rect
from logo import OBJ

pygame.init()
GAME_SPEED = 60

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
# Kleuren worden aangeven met een tuple van 3 getallen - rood, groen, blauw - tussen 0 en 255.
# 0, 0, 0 betekend geen kleurm, dus zwart.
BACKGROUND_COLOR = (0, 0, 0)
pygame.display.set_caption("Werkplaats 1: PyGame")
clock = pygame.time.Clock()

canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


def quit_game_requested():
    halting = False
    # De lijst met "events" is een lijst met alle gebeurtenissen die
    # plaatsvonden sinds de vorige loop.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            halting = True
            break
    return halting


logo = Logo()
logo2 = Logo(x_start=300, y_start=300)
while not quit_game_requested():
    canvas.fill(BACKGROUND_COLOR)
    logo.update(canvas)  # Logo 1 verplaatst en wordt getekend
    logo2.update(canvas) # Logo 2verplaatst en wordt getekend

    # We controleren hier of de logos botsen. "colliderect" werkt alleen als beide objecten in de parameters:
    # - een "rect" attribuut hebben
    # - de klasse "Sprite" erven
    if collide_rect(logo, logo2):
        logo.reverse()
        logo2.reverse()
    pygame.display.flip()
    clock.tick(GAME_SPEED)

print("Game over!")
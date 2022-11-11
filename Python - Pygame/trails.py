import pygame as pg
from pygame.math import Vector2


class Player(pg.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pg.image.load("images/ob_circle.png").convert_alpha()
        #self.image.fill(pg.Color('sienna1'))
        self.rect = self.image.get_rect(center=pos)
        # A separate image for the trail (just a single-color circle).
        self.trail_image = pg.Surface((40, 40), pg.SRCALPHA)
        pg.draw.circle(self.trail_image, pg.Color('dodgerblue'), (20, 20), 20)
        self.trail_rect = self.trail_image.get_rect()

        self.vel = Vector2(0, 0)
        self.pos = Vector2(pos)

    def update(self):
        self.pos += self.vel
        self.rect.center = self.pos
        # Update the rect of the trail as well, because we'll blit it there.
        self.trail_rect.center = self.rect.center


def main():
    pg.init()
    screen = pg.display.set_mode((640, 480))
    # Blit objects with trails onto this surface instead of the screen.
    alpha_surf = pg.Surface(screen.get_size(), pg.SRCALPHA)
    clock = pg.time.Clock()
    all_sprites = pg.sprite.Group()
    sprites_with_trails = pg.sprite.Group()
    player = Player((150, 150), all_sprites, sprites_with_trails)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_d:
                    player.vel.x = 5
                elif event.key == pg.K_a:
                    player.vel.x = -5
                elif event.key == pg.K_w:
                    player.vel.y = -5
                elif event.key == pg.K_s:
                    player.vel.y = 5
            elif event.type == pg.KEYUP:
                if event.key == pg.K_d and player.vel.x > 0:
                    player.vel.x = 0
                elif event.key == pg.K_a and player.vel.x < 0:
                    player.vel.x = 0
                elif event.key == pg.K_w:
                    player.vel.y = 0
                elif event.key == pg.K_s:
                    player.vel.y = 0

        # Reduce the alpha of all pixels on this surface each frame.
        # Control the fade speed with the alpha value.
        alpha_surf.fill((255, 255, 255, 244), special_flags=pg.BLEND_RGBA_MULT)

        all_sprites.update()
        screen.fill((20, 50, 80))  # Clear the screen.
        # Blit the trails onto the alpha_surf.
        for sprite in sprites_with_trails:
            alpha_surf.blit(sprite.trail_image, sprite.trail_rect)
        screen.blit(alpha_surf, (0, 0))  # Blit the alpha_surf onto the screen.
        all_sprites.draw(screen)  # Draw the objects onto the alpha_surf.
        pg.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
    pg.quit()
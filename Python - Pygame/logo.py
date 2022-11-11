import pygame
from pygame.sprite import Sprite, Group, collide_rect


class OBJ(Sprite):
    def __init__(
        self,
        logo_speed_x=3,
        logo_speed_y=3,
        logo_image="images/ob_circle.png",
        x_start=0,
        y_start=0,
    ):
        super().__init__()
        self.logo_speed_x = logo_speed_x
        self.logo_speed_y = logo_speed_y
        self.current_speed = [self.logo_speed_x, self.logo_speed_y]
        self.image = pygame.image.load(logo_image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x_start
        self.rect.y = y_start

    def update(self, canvas):
        self.bounce_if_required(canvas.get_width(), canvas.get_height())
        self.rect = self.rect.move(self.current_speed)
        canvas.blit(self.image, self.rect)

    def bounce_if_required(self, screen_width, screen_height):
        # Linkerkant van het scherm geraakt?
        if self.rect.left <= 0:
            self.current_speed[0] = self.logo_speed_x
        # Rechterkant van het scherm geraakt?
        elif self.rect.right >= screen_width:
            self.current_speed[0] = -self.logo_speed_x

        # Bovenkant van het scherm geraakt?
        if self.rect.top <= 0:
            self.current_speed[1] = self.logo_speed_y
        # Onderkant van het scherm geraakt?
        elif self.rect.bottom >= screen_height:
            self.current_speed[1] = -self.logo_speed_y

    def reverse(self):
        self.current_speed[0] = -self.current_speed[0]
        self.current_speed[1] = -self.current_speed[1]
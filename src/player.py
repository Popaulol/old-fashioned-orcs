import src.solid as solid
import pygame

class Player(pygame.sprite.Sprite):
    # This is our player class. We derive it from pygame.sprite.Sprite in order to benefit from the group system
    # pygame has.
    def __init__(self):
        super().__init__()  # we need this to ensure the sprite will work correctly with groups
        # Surfaces are image objects. We can replace this with assets once they're made
        self.image = pygame.Surface((16, 16)).convert_alpha()
        # convert_alpha is a method to allow us to use PNG images with transparency, and also make them faster to
        # render on-screen
        self.image.fill("blue")  # For now, our player is just a random blue square though.
        # We make a rectangle object, which can then be used to locate the sprite on the screen.
        self.rect = self.image.get_rect(center=(80, 72))
        # In Pygame, (0, 0) is the topleft corner of the screen.
        # Adding 1 to self.rect.x will move self.rect 1 pixel to the right.
        # And so adding 1 to self.rect.y will move self.rect 1 pixel downwards.
        self.x_velocity = 1
        self.y_velocity = 0
        self.falling=True
    # The two methods below move the player.
    def move_left(self):
        self.rect.x-=self.x_velocity
    def move_right(self):
        self.rect.x+=self.x_velocity


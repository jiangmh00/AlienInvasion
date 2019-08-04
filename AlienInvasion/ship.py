import pygame
from pygame.sprite import Sprite
 
class Ship(Sprite):
    """A class to manage the ship."""
 
    def __init__(self, ai_settings, screen):
        """Initialize the ship and set its starting position."""
        super(Ship, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # Load the ship image and get its rect.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship at the bottom center of the screen.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Store a decimal value for the ship's position.
        self.x = float(self.rect.centerx)

        # Movement flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's posion based on movement flags."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.x -= self.ai_settings.ship_speed_factor

        # Update rect object from self.x.
        self.rect.centerx = self.x

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Center the ship on the screen."""
        self.x = self.screen_rect.centerx
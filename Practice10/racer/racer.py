import pygame, random
from pygame.locals import *

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
CROP = 20

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        source = pygame.image.load("images/Enemy.png").convert_alpha()
        crop_rect = pygame.Rect(
            CROP * 7,
            CROP,
            source.get_width() - 13.5 * CROP,
            source.get_height() - 2 * CROP
        )
        self.image = source.subsurface(crop_rect).copy()
        self.image = pygame.transform.scale(self.image, (60, 120))
        self.image = pygame.transform.rotate(self.image, 180)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
            return True
        return False

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        source = pygame.image.load("images/Player.png").convert_alpha()
        crop_rect = pygame.Rect(
            CROP * 8,
            CROP,
            source.get_width() - 16 * CROP,
            source.get_height() - 2 * CROP
        )
        self.image = source.subsurface(crop_rect).copy()
        self.image = pygame.transform.scale(self.image, (60, 120))
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/Coin.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
import os
import pygame
import random

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
LANES = [80, 150, 220, 290]
CROP = 20

class Player(pygame.sprite.Sprite):
    COLORS = {
        "blue": (0, 100, 255),
        "red": (220, 40, 40),
        "green": (0, 200, 80),
        "yellow": (240, 220, 40)
    }

    def __init__(self, color_name="blue"):
        super().__init__()
        self.color_name = color_name
        self.base_image = self._load_image("images/Player.png")
        self.image = self._tint(self.base_image, self.COLORS.get(color_name, (0, 100, 255)))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.speed = 6
        self.slow_until = 0

    def _load_image(self, path):
        source = pygame.image.load(path)
        crop_rect = pygame.Rect(
            CROP * 8,
            CROP,
            source.get_width() - 16 * CROP,
            source.get_height() - 2 * CROP
        )
        image = source.subsurface(crop_rect).copy()
        return pygame.transform.scale(image, (60, 120))

    def _tint(self, image, color):
        tinted = image.copy()
        overlay = pygame.Surface(tinted.get_size(), pygame.SRCALPHA)
        overlay.fill(color + (0,))
        tinted.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
        return tinted

    def set_color(self, color_name):
        self.color_name = color_name
        self.image = self._tint(self.base_image, self.COLORS.get(color_name, (0, 100, 255)))

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        move_speed = self.speed
        if pygame.time.get_ticks() < self.slow_until:
            move_speed = max(2, move_speed - 3)

        if self.rect.left > 0 and pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-move_speed, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(move_speed, 0)

        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(SCREEN_WIDTH, self.rect.right)

class TrafficCar(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.base_image = self._load_image("images/Enemy.png")
        self.image = self._tint_random(self.base_image)
        self.rect = self.image.get_rect()
        self.reset_position()

    def _load_image(self, path):
        source = pygame.image.load(os.path.join(BASE_DIR, path))
        crop_rect = pygame.Rect(
            CROP * 7,
            CROP,
            source.get_width() - 13.5 * CROP,
            source.get_height() - 2 * CROP
        )
        image = source.subsurface(crop_rect).copy()
        image = pygame.transform.scale(image, (60, 120))
        return pygame.transform.rotate(image, 180)

    def _tint_random(self, image):
        tinted = image.copy()
        overlay = pygame.Surface(tinted.get_size(), pygame.SRCALPHA)
        tint = random.choice([(255, 40, 40), (40, 40, 255), (40, 255, 40), (255, 220, 40)])
        overlay.fill(tint + (0,))
        tinted.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGB_ADD)
        return tinted

    def reset_position(self, avoid_rect=None):
        choices = LANES[:]
        if avoid_rect:
            choices = [x for x in choices if abs(x - avoid_rect.centerx) > 100]
            if not choices:
                choices = LANES[:]
        self.rect.centerx = random.choice(choices)
        self.rect.top = -random.randint(140, 320)

    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()
            return True
        return False

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join(BASE_DIR, "images", "Coin.png"))
        self.image = pygame.transform.scale(self.image, (36, 36))
        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self, avoid_rect=None):
        choices = LANES[:]
        if avoid_rect:
            choices = [x for x in choices if abs(x - avoid_rect.centerx) > 100]
            if not choices:
                choices = LANES[:]
        self.rect.centerx = random.choice(choices)
        self.rect.top = -random.randint(140, 320)

    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.reset_position()
            return True
        return False

class Hazard(pygame.sprite.Sprite):
    COLORS = {
        "barrier": (180, 20, 20),
        "oil": (20, 20, 30),
        "pothole": (90, 90, 90),
        "boost": (20, 180, 220)
    }

    def __init__(self, kind):
        super().__init__()
        self.kind = kind
        width = 80 if kind != "boost" else 100
        height = 30 if kind != "boost" else 20
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.image.fill(self.COLORS.get(kind, (255, 255, 255)))
        if kind == "boost":
            pygame.draw.rect(self.image, (255, 255, 255), self.image.get_rect(), 2)
        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self, avoid_rect=None):
        choices = LANES[:]
        if avoid_rect:
            choices = [x for x in choices if abs(x - avoid_rect.centerx) > 100]
            if not choices:
                choices = LANES[:]
        self.rect.centerx = random.choice(choices)
        self.rect.top = -random.randint(120, 360)

    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
            return True
        return False

class PowerUp(pygame.sprite.Sprite):
    COLORS = {
        "nitro": (40, 180, 255),
        "shield": (240, 220, 40),
        "repair": (100, 240, 100)
    }

    def __init__(self, kind):
        super().__init__()
        self.kind = kind
        self.spawn_time = pygame.time.get_ticks()
        self.image = pygame.Surface((36, 36), pygame.SRCALPHA)
        pygame.draw.circle(self.image, self.COLORS.get(kind, (255, 255, 255)), (18, 18), 18)
        self.rect = self.image.get_rect()
        self.reset_position()

    def reset_position(self, avoid_rect=None):
        choices = LANES[:]
        if avoid_rect:
            choices = [x for x in choices if abs(x - avoid_rect.centerx) > 100]
            if not choices:
                choices = LANES[:]
        self.rect.centerx = random.choice(choices)
        self.rect.top = -random.randint(180, 380)

    def move(self, speed):
        self.rect.move_ip(0, speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
            return True
        return False

    def expired(self):
        return pygame.time.get_ticks() - self.spawn_time > 9000

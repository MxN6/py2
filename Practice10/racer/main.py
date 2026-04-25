import pygame, sys, time, random
from pygame.locals import *
from racer import Coin, Enemy, Player, SCREEN_WIDTH, SCREEN_HEIGHT

pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

CARSPEED = 5
BCKSPEED = 3
SCORE = 0

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

background = pygame.image.load("images/background.jpg")
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
next_background = background.copy()

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

BY = 0
while True:
    for event in pygame.event.get():
        if event.type == INC_SPEED:
            CARSPEED += 0.5
            BCKSPEED += 0.5
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    DISPLAYSURF.blit(background, (0, BY))
    BY += BCKSPEED
    DISPLAYSURF.blit(next_background, (0, BY - SCREEN_HEIGHT))
    if BY >= SCREEN_HEIGHT:
        BY = 0
    scores = font_small.render(str(SCORE), True, BLACK)
    DISPLAYSURF.blit(scores, (10,10))

    P1.move()
    if E1.move(CARSPEED):
        SCORE += 1
    if C1.move(BCKSPEED):
        C1.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
    
    if pygame.sprite.spritecollideany(P1, coins):
        coin = pygame.sprite.spritecollide(P1, coins, False)
        pygame.mixer.Sound('sounds/coin.mp3').play()
        SCORE += 5
        C1.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)

    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('sounds/crash.mp3').play()
        time.sleep(0.5)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30,250))

        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    pygame.display.update()
    FramePerSec.tick(FPS)
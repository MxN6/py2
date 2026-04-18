import pygame
from ball import ball

pygame.init()

screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
running = True

Baller = ball(250, 250, 500, 500)

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            Baller.move(e.key)
    
    screen.fill((255,255,255))
    Baller.draw(screen)
    clock.tick(60)
    pygame.display.flip()
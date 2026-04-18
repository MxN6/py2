import pygame
from player import Player

pygame.init()

screen = pygame.display.set_mode((400, 400)) 
clock = pygame.time.Clock()
running = True

player = Player(screen)

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_p:
                player.play()  
            if e.key == pygame.K_q:
                running = False 
            if e.key == pygame.K_RIGHT:
                player.next_song()
            if e.key == pygame.K_LEFT:
                player.prev_song()
            if e.key == pygame.K_SPACE:
                player.pause()
            if e.key == pygame.K_s:
                player.stop()

    screen.fill((255, 255, 255))
    
    player.draw()

    # 3. REFRESH
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
import pygame, time
from pygame.locals import *
import random
from snake import Snake, Apple

pygame.init()
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()
running = True
FPS = 5

font = pygame.font.SysFont("Verdana", 30)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, "WHITE")

snake = Snake()
apples = []
CAP = 4
five = False

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                snake.change_direction('UP')
            elif event.key == K_DOWN:
                snake.change_direction('DOWN')
            elif event.key == K_LEFT:
                snake.change_direction('LEFT')
            elif event.key == K_RIGHT:
                snake.change_direction('RIGHT')

    snake.move()

    if len(apples) < CAP:
        x = random.randrange(0, 400, 20)
        y = random.randrange(0, 300, 20)
        pos = (x, y)
        if pos not in snake.body:
            apples.append(Apple(pos))

    head = snake.body[0]
    for apple in apples[:]:
        if head == apple.pos:
            snake.grow()
            apples.remove(apple)
    
    if len(snake.body)%5 == 0 and len(snake.body) > 0 and not five:
        five = True
        CAP += 1
        FPS += 2.5
    elif len(snake.body)%5 != 0:
        five = False

    if head[0] < 0 or head[0] >= 400 or head[1] < 0 or head[1] >= 300 or head in snake.body[1:]:
        time.sleep(0.5)
        screen.fill((0, 0, 0))
        screen.blit(game_over, (100, 100))
        pygame.display.flip()
        time.sleep(2)
        pygame.quit()

    screen.fill((0, 0, 0))
    snake.draw(screen)
    for apple in apples:
        apple.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)
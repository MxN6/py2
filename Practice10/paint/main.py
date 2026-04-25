import pygame
from pygame.locals import *
from paint import DrawRectangle, drawLineBetween

pygame.init()

screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()

running = True
radius = 5
mode = "blue"
draw = "line"
current_points = []
start, end = [], []
center, distance = [], 0
strokes = []
drawingAvailable = False

while running:
    screen.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            drawingAvailable = True
            if draw == "line":
                current_points = [event.pos]
            elif draw == "rectangle":
                start = event.pos
            elif draw == "circle":
                center = event.pos
        elif event.type == MOUSEBUTTONUP and event.button == 1:
            drawingAvailable = False
            if draw == "rectangle":
                end = event.pos
                strokes.append(("rectangle", start, end))
            elif draw == "circle":
                distance = ((event.pos[0] - center[0]) ** 2 + (event.pos[1] - center[1]) ** 2) ** 0.5
                strokes.append(("circle", center, distance))
            elif len(current_points) > 1:
                strokes.append(("line", list(current_points), radius, mode))
            current_points = []
        elif event.type == MOUSEMOTION and drawingAvailable:
            if draw == "line":
                current_points.append(event.pos)
                current_points = current_points[-256:]
        elif event.type == KEYDOWN:
            if event.key == K_b:
                mode = "blue"
            elif event.key == K_r:
                mode = "red"
            elif event.key == K_g:
                mode = "green"
            elif event.key == K_c:
                strokes = []
                current_points = []
            elif event.key == K_UP:
                radius = min(50, radius + 1)
            elif event.key == K_DOWN:
                radius = max(1, radius - 1)
            elif event.key == K_t:
                # Toggle rectangle mode
                draw = "rectangle" if draw == "line" else "line"
            elif event.key == K_e:
                # Eraser mode
                mode = "eraser"
            elif event.key == K_i:
                # circle mode
                draw = "circle"

    for stroke in strokes:
        if isinstance(stroke, tuple) and stroke[0] == "rectangle":
            DrawRectangle(screen, stroke[1], stroke[2])
        elif isinstance(stroke, tuple) and stroke[0] == "line":
            for i in range(len(stroke[1]) - 1):
                drawLineBetween(screen, i, stroke[1][i], stroke[1][i + 1], stroke[2], stroke[3])
        elif isinstance(stroke, tuple) and stroke[0] == "circle":
            pygame.draw.circle(screen, (255, 0, 0), stroke[1], int(stroke[2]), 1)

    if drawingAvailable:
        for i in range(len(current_points) - 1):
            drawLineBetween(screen, i, current_points[i], current_points[i + 1], radius, mode)

    pygame.display.flip()
    clock.tick(60)
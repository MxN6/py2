import pygame

def drawLineBetween(screen, index, start, end, width, color_mode):
    c1 = max(0, min(255, 2 * index - 256))
    c2 = max(0, min(255, 2 * index))

    if color_mode == "blue":
        color = (c1, c1, c2)
    elif color_mode == "red":
        color = (c2, c1, c1)
    elif color_mode == "green":
        color = (c1, c2, c1)
    else:
        color = (255, 255, 255)

    dx = end[0] - start[0]
    dy = end[1] - start[1]
    iterations = max(abs(dx), abs(dy))

    if iterations == 0:
        pygame.draw.circle(screen, color, start, width)
        return

    for i in range(iterations + 1):
        progress = i / iterations
        x = int(start[0] + dx * progress)
        y = int(start[1] + dy * progress)
        pygame.draw.circle(screen, color, (x, y), width)

def DrawRectangle(screen, top_left, right_bottom):
    pygame.draw.rect(screen, (0, 0, 0), (top_left[0], top_left[1], right_bottom[0] - top_left[0], right_bottom[1] - top_left[1]), 1)
    
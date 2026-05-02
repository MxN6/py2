import pygame
from pygame.locals import *
from paint import Brush
from datetime import datetime

pygame.init()
screen = pygame.display.set_mode((900, 600))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()

brush = Brush()
canvas = pygame.Surface((900, 600))
canvas.fill((255, 255, 255))
rt = 0

Font = pygame.font.SysFont(None, 24)
instructions = [
    "1-4: Color (Red, Green, Blue, Eraser)",
    "Q: Freehand | W: Circle | A: Rectangle | E: Square | R: Right Triangle | D: Equal Triangle | V: Rhombus | F: Flood Fill",
    "UP/DOWN: Adjust Brush Size | C: Clear Canvas"
]

running = True
while running:
    screen.fill((255, 255, 255))
    screen.blit(canvas, (0, 0))

    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            
        elif event.type == MOUSEBUTTONDOWN and event.button == 1:
            brush.active = True
            if brush.shape == "curve":
                brush.points = [event.pos]
            elif brush.shape == "rectangle" or brush.shape == "square" or brush.shape == "rhombus":
                brush.start_pos = event.pos
            elif brush.shape == "fill" or brush.shape == "right_triangle" or brush.shape == "equal_triangle":
                brush.start_pos = event.pos
            elif brush.shape == "text":
                brush.start_pos = event.pos
            elif brush.shape == "circle":
                brush.center_pos = event.pos

        elif event.type == MOUSEBUTTONUP and event.button == 1:
            if brush.active:
                if brush.shape == "rectangle" and brush.start_pos:
                    brush.draw_rectangle(canvas, brush.start_pos, event.pos, color=brush.get_solid_color())
                elif brush.shape == "circle" and brush.center_pos:
                    dist = ((event.pos[0] - brush.center_pos[0])**2 + (event.pos[1] - brush.center_pos[1])**2)**0.5
                    brush.draw_circle(canvas, brush.center_pos, dist, color=brush.get_solid_color())
                elif brush.shape == "curve" and len(brush.points) > 0:
                    for i in range(len(brush.points) - 1):
                        brush.draw_line_segment(canvas, i, brush.points[i], brush.points[i+1], brush.radius, color_mode=brush.mode)
                    if len(brush.points) == 1:
                        brush.draw_line_segment(canvas, 0, brush.points[0], brush.points[0], brush.radius, color_mode=brush.mode)
                elif brush.shape == "square" and brush.start_pos:
                    brush.draw_square(canvas, brush.start_pos, event.pos, color=brush.get_solid_color())
                elif brush.shape == "right_triangle" and brush.start_pos:
                    brush.draw_right_triangle(canvas, brush.start_pos, event.pos, color=brush.get_solid_color())
                elif brush.shape == "equal_triangle" and brush.start_pos:
                    brush.draw_equal_triangle(canvas, brush.start_pos, event.pos, color=brush.get_solid_color())
                elif brush.shape == "rhombus" and brush.start_pos:
                    brush.draw_rhombus(canvas, brush.start_pos, event.pos, color=brush.get_solid_color())
                elif brush.shape == "fill":
                    brush.flood_fill(canvas, event.pos)
            
            if brush.shape != "text":
                brush.active = False 
                brush.clear_session()

        elif event.type == MOUSEMOTION and brush.active:
            if brush.shape == "curve":
                brush.points.append(event.pos)
                if len(brush.points) > 256:
                    brush.points.pop(0)

        elif event.type == pygame.TEXTINPUT and brush.shape == "text" and brush.active:
            brush.text += event.text
        elif event.type == KEYDOWN:
            if event.key == K_1: brush.set_color("red")
            elif event.key == K_2: brush.set_color("green")
            elif event.key == K_3: brush.set_color("blue")
            elif event.key == K_4: brush.set_color("eraser")
            elif event.key == K_q: brush.set_shape("curve")
            elif event.key == K_w: brush.set_shape("circle")
            elif event.key == K_a: brush.set_shape("rectangle")
            elif event.key == K_e: brush.set_shape("square")
            elif event.key == K_r: brush.set_shape("right_triangle")
            elif event.key == K_d: brush.set_shape("equal_triangle")
            elif event.key == K_v: brush.set_shape("rhombus")
            elif event.key == K_f: brush.set_shape("fill")
            elif event.key == K_t: 
                brush.set_shape("text")
            elif event.key == K_LCTRL: brush.save = True
            if event.key == K_BACKSPACE and brush.shape == "text":
                brush.text = brush.text[:-1]
            elif event.key == K_RETURN and brush.shape == "text":
                brush.draw_text(canvas, brush.text, brush.start_pos, color=brush.get_solid_color())
                brush.text = ""
                brush.active = False
                brush.clear_session()
            elif event.key == K_s and brush.save:
                pygame.image.save(screen, 'image-{date:%Y-%m-%d_%H-%M-%S}.png'.format(date=datetime.now()))
            elif event.key == K_UP:
                rt = 90
                brush.adjust_radius(1)
            elif event.key == K_DOWN:
                rt = 90
                brush.adjust_radius(-1)
            elif event.key == K_c and not brush.active:
                canvas.fill((255, 255, 255))
                brush.clear_session()
        elif event.type == KEYUP:
            if event.key == K_LCTRL:
                brush.save = False
    if brush.active:
        if brush.shape == "curve":
            for i in range(len(brush.points) - 1):
                brush.draw_line_segment(screen, i, brush.points[i], brush.points[i+1], brush.radius)
        elif brush.shape == "rectangle" and brush.start_pos:
            brush.draw_rectangle(screen, brush.start_pos, pygame.mouse.get_pos(), is_preview=True)
        elif brush.shape == "circle" and brush.center_pos:
            m_pos = pygame.mouse.get_pos()
            dist = ((m_pos[0] - brush.center_pos[0])**2 + (m_pos[1] - brush.center_pos[1])**2)**0.5
            brush.draw_circle(screen, brush.center_pos, dist, is_preview=True)
        elif brush.shape == "square" and brush.start_pos:
            brush.draw_square(screen, brush.start_pos, pygame.mouse.get_pos(), is_preview=True)
        elif brush.shape == "right_triangle" and brush.start_pos:
            brush.draw_right_triangle(screen, brush.start_pos, pygame.mouse.get_pos(), is_preview=True)
        elif brush.shape == "equal_triangle" and brush.start_pos:
            brush.draw_equal_triangle(screen, brush.start_pos, pygame.mouse.get_pos(), is_preview=True)
        elif brush.shape == "rhombus" and brush.start_pos:
            brush.draw_rhombus(screen, brush.start_pos, pygame.mouse.get_pos(), is_preview=True)
        elif brush.shape == "text" and brush.start_pos:
            brush.draw_text(screen, brush.text + "|", brush.start_pos, color=brush.get_solid_color())

    keys = pygame.key.get_pressed()
    if keys[K_h] and not brush.active:
        for i, text in enumerate(instructions):
            img = Font.render(text, True, (0, 0, 0))
            screen.blit(img, (10, 10 + i * 30))
    if rt > 0: 
        rt -= 1
        image = Font.render(f"Brush Size: {brush.radius}", True, (0, 0, 0))
        screen.blit(image, (10, 10 + len(instructions) * 30))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
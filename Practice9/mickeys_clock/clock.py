import pygame 
import datetime
import math

pygame.init()

screen = pygame.display.set_mode((400, 300))
running = True

center_x, center_y = 200, 150
center = (center_x, center_y)
radius = 75

clock_bkg = pygame.image.load("images/clock-without-hands.png").convert_alpha()
clock_bkg = pygame.transform.scale(clock_bkg, (300, 300))
clock_crect = clock_bkg.get_rect(center = center)

mickey_head = pygame.image.load("images/mickey_head.png").convert_alpha()
mickey_head = pygame.transform.scale(mickey_head, (100, 100))
head_crect = mickey_head.get_rect(center = center)

mickey_point = pygame.image.load("images/mickey_point.png").convert_alpha()
mickey_point = pygame.transform.scale(mickey_point, (30, 30))
mickey_point = pygame.transform.rotate(mickey_point, -35)

mickey_hand = pygame.image.load("images/mickey_hand.png").convert_alpha()
mickey_hand = pygame.transform.scale(mickey_hand, (30, 30))
mickey_hand = pygame.transform.rotate(mickey_hand, -90)

clock = pygame.time.Clock()

print(datetime.datetime.now())

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now_time = datetime.datetime.now()
    minutes = now_time.minute
    seconds = now_time.second

    total_minutes = minutes + (seconds / 60)
    minute_angle = total_minutes * 6 - 100
    second_angle = seconds * 6 - 185

    minute_rad = math.radians(minute_angle)
    second_rad = math.radians(second_angle)

    minute_x = center_x + radius * math.cos(minute_rad)
    minute_y = center_y + radius * math.sin(minute_rad)

    second_x = center_x + radius * math.cos(second_rad)
    second_y = center_y + radius * math.sin(second_rad)

    rotate_min = pygame.transform.rotate(mickey_hand, -minute_angle)
    rotate_second = pygame.transform.rotate(mickey_point, -second_angle)
    
    hand_rect = rotate_min.get_rect(center=(minute_x, minute_y))
    point_rect = rotate_second.get_rect(center=(second_x, second_y))

    screen.fill((255, 255, 255))
    screen.blit(clock_bkg, clock_crect)
    screen.blit(mickey_head, head_crect)
    screen.blit(rotate_min, hand_rect)
    screen.blit(rotate_second, point_rect)

    dt = clock.tick(60)
    pygame.display.flip()

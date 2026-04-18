import pygame

def restrict_movement(x, y, width, height, step):
    first_condition = x - step < 0 or x + step > width
    second_condition = y - step < 0 or y + step > height
    if first_condition or second_condition:
        return False
    return True
 
class ball:
    def __init__(self, x, y, screen_x, screen_y):
        self.x = x
        self.y = y
        self.color = "RED"
        self.size = (50, 50)
        self.radius = 25
        self.step = 20
        self.sx = screen_x
        self. sy = screen_y
        self.cond = restrict_movement
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (self.x, self.y), self.radius)
    def move(self, key):
        next_x, next_y = self.x, self.y
        if key == pygame.K_UP:
            next_y -= self.step
        if key == pygame.K_DOWN:
            next_y += self.step
        if key == pygame.K_RIGHT:
            next_x += self.step
        if key == pygame.K_LEFT:
            next_x -= self.step
        if self.cond(next_x, next_y, self.sx, self.sy, self.step):
            self.x, self.y = next_x, next_y
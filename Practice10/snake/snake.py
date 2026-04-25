import pygame

class Snake:
    def __init__(self):
        self.dimension = (20, 20)
        self.body = [(40, 0), (20, 0)]
        self.direction = 'RIGHT'
        self.queue = []

    def move(self):
        head_x, head_y = self.body[0]
        if self.queue:
            self.direction = self.queue.pop(0)
        if self.direction == 'UP':
            new_head = (head_x, head_y - 20)
        elif self.direction == 'DOWN':
            new_head = (head_x, head_y + 20)
        elif self.direction == 'LEFT':
            new_head = (head_x - 20, head_y)
        else:
            new_head = (head_x + 20, head_y)

        for i in range(len(self.body) - 1, 0, -1):
            self.body[i] = self.body[i - 1]
        self.body[0] = new_head

    def grow(self):
        self.body.append(self.body[-1])

    def change_direction(self, new_direction):
        opposite_directions = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if new_direction != opposite_directions[self.direction]:
            self.queue.append(new_direction)

    def draw(self, surface):
        for segment in self.body:
            pygame.draw.rect(surface, (0, 255, 0), (*segment, *self.dimension))

class Apple:
    def __init__(self, pos: tuple):
        self.pos = pos

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), (*self.pos, 20, 20))
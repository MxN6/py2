import pygame
import random

CELL_SIZE = 20
WIDTH = 400
HEIGHT = 300
COLS = WIDTH // CELL_SIZE
ROWS = HEIGHT // CELL_SIZE

class Snake:
    def __init__(self, color=(0, 255, 0)):
        self.color = color
        self.reset()

    def reset(self):
        self.body = [(5, 7), (4, 7), (3, 7)]
        self.direction = "RIGHT"
        self.queue = []
        self.grow_count = 0

    @property
    def head(self):
        return self.body[0]

    def move(self):
        if self.queue:
            next_direction = self.queue.pop(0)
            if not self._is_opposite(next_direction):
                self.direction = next_direction

        head_x, head_y = self.head
        if self.direction == "UP":
            new_head = (head_x, head_y - 1)
        elif self.direction == "DOWN":
            new_head = (head_x, head_y + 1)
        elif self.direction == "LEFT":
            new_head = (head_x - 1, head_y)
        else:
            new_head = (head_x + 1, head_y)

        self.body.insert(0, new_head)
        if self.grow_count > 0:
            self.grow_count -= 1
        else:
            self.body.pop()

    def grow(self, count=1):
        self.grow_count += count

    def shrink(self, count=2):
        for _ in range(count):
            if len(self.body) > 1:
                self.body.pop()

    def change_direction(self, new_direction):
        if new_direction not in ("UP", "DOWN", "LEFT", "RIGHT"):
            return
        if not self._is_opposite(new_direction):
            self.queue.append(new_direction)

    def _is_opposite(self, new_direction):
        opposites = {"UP": "DOWN", "DOWN": "UP", "LEFT": "RIGHT", "RIGHT": "LEFT"}
        return opposites.get(new_direction) == self.direction

    def collides_with_self(self):
        return self.head in self.body[1:]

    def draw(self, surface, grid_on=True):
        for segment in self.body:
            rect = pygame.Rect(segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(surface, self.color, rect)
            if grid_on:
                pygame.draw.rect(surface, (30, 30, 30), rect, 1)

    def occupied(self):
        return set(self.body)

class Food:
    def __init__(self, kind, position, points):
        self.kind = kind
        self.position = position
        self.points = points
        self.spawn_time = pygame.time.get_ticks()
        self.duration = 8000

    @property
    def expired(self):
        return pygame.time.get_ticks() - self.spawn_time > self.duration

    def draw(self, surface):
        x, y = self.position
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        if self.kind == "poison":
            color = (120, 0, 0)
        else:
            color = (255, 50 + self.points * 30, 50)
        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, (255, 255, 255), rect, 1)

class PowerUp:
    COLORS = {
        "speed": (40, 180, 255),
        "slow": (255, 180, 40),
        "shield": (180, 255, 120),
    }

    def __init__(self, kind, position):
        self.kind = kind
        self.position = position
        self.spawn_time = pygame.time.get_ticks()
        self.duration = 8000

    @property
    def expired(self):
        return pygame.time.get_ticks() - self.spawn_time > self.duration

    def draw(self, surface):
        x, y = self.position
        rect = pygame.Rect(x * CELL_SIZE + 4, y * CELL_SIZE + 4, CELL_SIZE - 8, CELL_SIZE - 8)
        pygame.draw.ellipse(surface, self.COLORS.get(self.kind, (255, 255, 255)), rect)
        pygame.draw.ellipse(surface, (255, 255, 255), rect, 1)

class Obstacle:
    def __init__(self, position):
        self.position = position

    def draw(self, surface):
        x, y = self.position
        rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(surface, (90, 90, 90), rect)
        pygame.draw.rect(surface, (0, 0, 0), rect, 1)

def random_cell(exclude):
    choices = [(x, y) for x in range(COLS) for y in range(ROWS) if (x, y) not in exclude]
    return random.choice(choices) if choices else None

def generate_obstacles(count, exclude):
    positions = []
    forbidden = set(exclude)
    for _ in range(count):
        cell = random_cell(forbidden)
        if cell is None:
            break
        positions.append(cell)
        forbidden.add(cell)
    return [Obstacle(position) for position in positions]

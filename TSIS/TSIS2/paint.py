import pygame

class Brush:
    def __init__(self):
        self.radius = 5
        self.mode = "blue"      # Color mode: blue, red, green, or eraser
        self.shape = "curve"    # Shape mode: curve, rectangle, circle, fill
        self.active = False
        
        # Temporary storage for the shape currently being dragged
        self.points = []
        self.start_pos = None
        self.center_pos = None
        self.save = False

        self.text = ""

    def set_color(self, color_name):
        if not self.active:
            self.mode = color_name
            self.shape = "curve"

    def set_shape(self, shape_name):
        if not self.active:
            self.shape = shape_name

    def adjust_radius(self, amount):
        self.radius = max(1, min(50, self.radius + amount))

    def clear_session(self):
        self.points = []
        self.start_pos = None
        self.center_pos = None

    def get_solid_color(self):
        if self.mode == "blue":
            return (0, 0, 255)
        elif self.mode == "red":
            return (255, 0, 0)
        elif self.mode == "green":
            return (0, 255, 0)
        else:
            return (255, 255, 255)

    def _get_color(self, index):
        c1 = max(0, min(255, 2 * index - 256))
        c2 = max(0, min(255, 2 * index))

        if self.mode == "blue":
            return (c1, c1, c2)
        elif self.mode == "red":
            return (c2, c1, c1)
        elif self.mode == "green":
            return (c1, c2, c1)
        else:
            return (255, 255, 255)

    def draw_line_segment(self, screen, index, start, end, width, color_mode=None):
        original_mode = self.mode
        if color_mode:
            self.mode = color_mode

        color = self._get_color(index)
        dx, dy = end[0] - start[0], end[1] - start[1]
        iterations = max(abs(dx), abs(dy))

        if iterations == 0:
            pygame.draw.circle(screen, color, start, width)
        else:
            for i in range(iterations + 1):
                progress = i / iterations
                x = int(start[0] + dx * progress)
                y = int(start[1] + dy * progress)
                pygame.draw.circle(screen, color, (x, y), width)

        self.mode = original_mode

    def draw_rectangle(self, screen, top_left, right_bottom, is_preview=False, color=None):
        if color is None:
            color = self.get_solid_color() if not is_preview else (100, 100, 100)

        x = min(top_left[0], right_bottom[0])
        y = min(top_left[1], right_bottom[1])
        w = abs(right_bottom[0] - top_left[0])
        h = abs(right_bottom[1] - top_left[1])

        if w > 0 and h > 0:
            pygame.draw.rect(screen, color, (x, y, w, h), 1)

    def draw_square(self, screen, top_left, right_bottom, is_preview=False, color=None):
        if color is None:
            color = self.get_solid_color() if not is_preview else (100, 100, 100)

        raw_w = right_bottom[0] - top_left[0]
        raw_h = right_bottom[1] - top_left[1]
        side = max(abs(raw_w), abs(raw_h))

        start_x = top_left[0] if raw_w >= 0 else top_left[0] - side
        start_y = top_left[1] if raw_h >= 0 else top_left[1] - side

        if side > 0:
            pygame.draw.rect(screen, color, (start_x, start_y, side, side), 1)

    def draw_circle(self, screen, center, radius, is_preview=False, color=None):
        if color is None:
            color = self.get_solid_color() if not is_preview else (200, 0, 0)

        if radius > 0:
            pygame.draw.circle(screen, color, center, int(radius), 1)

    def draw_right_triangle(self, screen, start, end, is_preview=False, color=None):
        if color is None:
            color = self.get_solid_color() if not is_preview else (0, 200, 0)

        points = [start, (end[0], start[1]), end]
        pygame.draw.polygon(screen, color, points, 1)

    def draw_equal_triangle(self, screen, start, end, is_preview=False, color=None):
        if color is None:
            color = self.get_solid_color() if not is_preview else (0, 0, 200)

        mid_x = (start[0] + end[0]) // 2
        points = [(mid_x, start[1]), (end[0], end[1]), (start[0], end[1])]
        pygame.draw.polygon(screen, color, points, 1)

    def draw_rhombus(self, screen, start, end, is_preview=False, color=None):
        if color is None:
            color = self.get_solid_color() if not is_preview else (200, 200, 0)

        mid_x = (start[0] + end[0]) // 2
        mid_y = (start[1] + end[1]) // 2
        points = [(mid_x, start[1]), (end[0], mid_y), (mid_x, end[1]), (start[0], mid_y)]
        pygame.draw.polygon(screen, color, points, 1)

    def flood_fill(self, surface, start_pos):
        width, height = surface.get_size()
        x, y = start_pos
        if not (0 <= x < width and 0 <= y < height):
            return

        target_color = surface.get_at((x, y))
        replacement_color = self.get_solid_color()
        if target_color == replacement_color:
            return

        surface.lock()
        stack = [(x, y)]

        while stack:
            px, py = stack.pop()
            if px < 0 or px >= width or py < 0 or py >= height:
                continue
            if surface.get_at((px, py)) != target_color:
                continue

            surface.set_at((px, py), replacement_color)
            stack.append((px + 1, py))
            stack.append((px - 1, py))
            stack.append((px, py + 1))
            stack.append((px, py - 1))

        surface.unlock()
    def draw_text(self, surface, text, pos, color=(0,0,0)):
        font = pygame.font.SysFont(None, 24)
        img = font.render(text, True, color)
        surface.blit(img, pos)

import pygame

class Button:
    def __init__(self, rect, text, font, base_color=(40, 40, 40), hover_color=(70, 70, 70), text_color=(255, 255, 255)):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.base_color = base_color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hovered = False

    def draw(self, surface):
        color = self.hover_color if self.hovered else self.base_color
        pygame.draw.rect(surface, color, self.rect, border_radius=8)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)


def draw_text(surface, text, x, y, font, color=(255, 255, 255)):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))


def draw_text_center(surface, text, rect, font, color=(255, 255, 255)):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

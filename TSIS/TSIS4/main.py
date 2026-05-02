import os
import sys
import json
import random
import pygame
from pygame.locals import *
from snake import Snake, Food, PowerUp, Obstacle, random_cell, generate_obstacles
import db
import config

pygame.init()
pygame.mixer.init()
pygame.font.init()

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
CELL_SIZE = 20
FONT_LARGE = pygame.font.SysFont("Verdana", 42)
FONT_MEDIUM = pygame.font.SysFont("Verdana", 24)
FONT_SMALL = pygame.font.SysFont("Verdana", 16)

STATE_USERNAME = "username"
STATE_MAIN_MENU = "main_menu"
STATE_SETTINGS = "settings"
STATE_LEADERBOARD = "leaderboard"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"

DEFAULT_SETTINGS = {
    "snake_color": [0, 255, 0],
    "grid": True,
    "sound": True
}

BUTTON_COLOR = (50, 50, 70)
BUTTON_HOVER = (100, 100, 140)
BUTTON_TEXT = (255, 255, 255)
BACKGROUND_COLOR = (10, 10, 12)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

settings = {}
leaderboard_cache = []

class Button:
    def __init__(self, rect, text):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.hovered = False

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, surface):
        pygame.draw.rect(surface, BUTTON_HOVER if self.hovered else BUTTON_COLOR, self.rect, border_radius=6)
        text = FONT_MEDIUM.render(self.text, True, BUTTON_TEXT)
        surface.blit(text, text.get_rect(center=self.rect.center))

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


def load_settings():
    global settings
    try:
        with open(config.SETTINGS_PATH, "r", encoding="utf-8") as f:
            settings = json.load(f)
    except Exception:
        settings = DEFAULT_SETTINGS.copy()
        save_settings()
    if "snake_color" not in settings:
        settings["snake_color"] = DEFAULT_SETTINGS["snake_color"]
    if "grid" not in settings:
        settings["grid"] = DEFAULT_SETTINGS["grid"]
    if "sound" not in settings:
        settings["sound"] = DEFAULT_SETTINGS["sound"]


def save_settings():
    with open(config.SETTINGS_PATH, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=2)

load_settings()

def draw_text(surface, text, x, y, font, color=(255, 255, 255)):
    surface.blit(font.render(text, True, color), (x, y))


def draw_text_center(surface, text, rect, font, color=(255, 255, 255)):
    surface.blit(font.render(text, True, color), font.render(text, True, color).get_rect(center=rect.center))


def clamp(value, min_value, max_value):
    return max(min_value, min(max_value, value))


def get_personal_best(username):
    if not db.DB_AVAILABLE or not username:
        return 0
    return db.fetch_personal_best(username)


def get_leaderboard():
    if not db.DB_AVAILABLE:
        return []
    return db.fetch_leaderboard(10)


def play_sound(sound):
    if settings.get("sound", True) and sound:
        sound.play()


def draw_grid(surface):
    for x in range(0, SCREEN_WIDTH, CELL_SIZE):
        pygame.draw.line(surface, (25, 25, 25), (x, 0), (x, SCREEN_HEIGHT))
    for y in range(0, SCREEN_HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, (25, 25, 25), (0, y), (SCREEN_WIDTH, y))

class GameSession:
    def __init__(self, username):
        self.username = username
        self.reset()

    def reset(self):
        self.snake = Snake(tuple(settings["snake_color"]))
        self.foods = []
        self.powerup = None
        self.obstacles = []
        self.score = 0
        self.level = 1
        self.food_eaten = 0
        self.persona_best = get_personal_best(self.username)
        self.game_over = False
        self.reason = ""
        self.shield_active = False
        self.active_effect = None
        self.effect_end = 0
        self.last_move = pygame.time.get_ticks()
        self.spawned_at = pygame.time.get_ticks()
        self.spawn_foods(3)
        self.next_powerup = pygame.time.get_ticks() + 5000

    def base_delay(self):
        return max(60, 200 - (self.level - 1) * 12)

    def move_delay(self):
        delay = self.base_delay()
        if self.active_effect == "speed":
            delay = max(40, delay - 80)
        elif self.active_effect == "slow":
            delay = delay + 80
        return delay

    def spawn_foods(self, count=1):
        for _ in range(count):
            position = random_cell(self.occupied_positions())
            if not position:
                return
            if random.random() < 0.18:
                self.foods.append(Food("poison", position, 0))
            else:
                value = random.choice([1, 2, 3, 4, 5])
                self.foods.append(Food("normal", position, value))

    def spawn_powerup(self):
        if self.powerup:
            return
        position = random_cell(self.occupied_positions())
        if not position:
            return
        kind = random.choice(["speed", "slow", "shield"])
        self.powerup = PowerUp(kind, position)

    def spawn_obstacles(self):
        if self.level < 3:
            self.obstacles = []
            return
        exclude = self.occupied_positions()
        head = self.snake.head
        for dx in range(-2, 3):
            for dy in range(-2, 3):
                neighbor = (head[0] + dx, head[1] + dy)
                if 0 <= neighbor[0] < SCREEN_WIDTH // CELL_SIZE and 0 <= neighbor[1] < SCREEN_HEIGHT // CELL_SIZE:
                    exclude.add(neighbor)
        self.obstacles = generate_obstacles(min(6, self.level + 1), exclude)

    def occupied_positions(self):
        occupied = set(self.snake.occupied())
        occupied.update([food.position for food in self.foods])
        if self.powerup:
            occupied.add(self.powerup.position)
        occupied.update([obs.position for obs in self.obstacles])
        return occupied

    def update(self):
        now = pygame.time.get_ticks()
        if self.game_over:
            return

        if now - self.last_move >= self.move_delay():
            self.last_move = now
            self.snake.move()
            self.process_collisions()

        if len(self.foods) < 3:
            self.spawn_foods(1)

        if self.powerup is None and now >= self.next_powerup:
            self.spawn_powerup()

        if self.powerup and self.powerup.expired:
            self.powerup = None
            self.next_powerup = now + 6000

        self.foods = [food for food in self.foods if not food.expired]
        if not self.powerup and now >= self.next_powerup:
            self.spawn_powerup()

        if self.active_effect in ("speed", "slow") and now >= self.effect_end:
            self.active_effect = None

    def process_collisions(self):
        head = self.snake.head
        if head[0] < 0 or head[0] >= SCREEN_WIDTH // CELL_SIZE or head[1] < 0 or head[1] >= SCREEN_HEIGHT // CELL_SIZE:
            if self.shield_active:
                self.shield_active = False
                self.active_effect = None
                self.snake.body.pop(0)
            else:
                self.finish("Hit the wall")
                return

        if self.snake.collides_with_self():
            if self.shield_active:
                self.shield_active = False
            else:
                self.finish("Ran into yourself")
                return

        if any(head == obs.position for obs in self.obstacles):
            if self.shield_active:
                self.shield_active = False
            else:
                self.finish("Hit an obstacle")
                return

        for food in self.foods[:]:
            if food.position == head:
                if food.kind == "poison":
                    self.snake.shrink(2)
                    self.score = max(0, self.score - 5)
                    if len(self.snake.body) <= 1:
                        self.finish("Shrank too small")
                        return
                else:
                    self.snake.grow()
                    self.score += food.points * 10
                    self.food_eaten += 1
                    if self.food_eaten % 5 == 0:
                        self.level += 1
                        self.spawn_obstacles()
                self.foods.remove(food)
                break

        if self.powerup and self.powerup.position == head:
            if self.powerup.kind == "speed":
                self.active_effect = "speed"
                self.effect_end = pygame.time.get_ticks() + 5000
            elif self.powerup.kind == "slow":
                self.active_effect = "slow"
                self.effect_end = pygame.time.get_ticks() + 5000
            elif self.powerup.kind == "shield":
                self.shield_active = True
                self.active_effect = "shield"
            self.powerup = None
            self.next_powerup = pygame.time.get_ticks() + 12000

    def finish(self, reason):
        self.game_over = True
        self.reason = reason
        if db.DB_AVAILABLE and self.username:
            db.save_game_session(self.username, self.score, self.level)

    def draw(self, surface):
        surface.fill(BACKGROUND_COLOR)
        if settings.get("grid", True):
            draw_grid(surface)
        for obs in self.obstacles:
            obs.draw(surface)
        for food in self.foods:
            food.draw(surface)
        if self.powerup:
            self.powerup.draw(surface)
        self.snake.draw(surface, settings.get("grid", True))
        draw_text(surface, f"Score: {self.score}", 10, 10, FONT_SMALL)
        draw_text(surface, f"Level: {self.level}", 10, 28, FONT_SMALL)
        draw_text(surface, f"Best: {self.persona_best}", 10, 46, FONT_SMALL)
        if self.active_effect:
            remaining = max(0, int((self.effect_end - pygame.time.get_ticks()) / 1000))
            if self.active_effect == "shield" and self.shield_active:
                power_text = "Shield active"
            else:
                power_text = f"{self.active_effect.title()} ({remaining}s)"
            draw_text(surface, power_text, 10, 64, FONT_SMALL)


def draw_main_menu(username, message, personal_best):
    screen.fill(BACKGROUND_COLOR)
    title_rect = pygame.Rect(0, 20, SCREEN_WIDTH, 60)
    draw_text_center(screen, "Snake Adventure", title_rect, FONT_LARGE)
    buttons = [
        Button((120, 110, 160, 40), "Play"),
        Button((120, 165, 160, 40), "Leaderboard"),
        Button((120, 220, 160, 40), "Settings"),
        Button((120, 275, 160, 40), "Quit"),
    ]
    for button in buttons:
        button.update(pygame.mouse.get_pos())
        button.draw(screen)
    draw_text(screen, f"Player: {username}", 20, 330 - 40, FONT_SMALL)
    draw_text(screen, f"Best: {personal_best}", 220, 330 - 40, FONT_SMALL)
    if not db.DB_AVAILABLE:
        draw_text(screen, "DB unavailable: install psycopg2 or configure PostgreSQL", 20, 330 - 20, FONT_SMALL, (200, 100, 100))
    elif message:
        draw_text(screen, message, 20, 330 - 20, FONT_SMALL, (200, 200, 0))
    return buttons


def draw_username_screen(username, message):
    screen.fill(BACKGROUND_COLOR)
    title_rect = pygame.Rect(0, 40, SCREEN_WIDTH, 60)
    draw_text_center(screen, "Enter Username", title_rect, FONT_LARGE)
    box = pygame.Rect(50, 140, 300, 50)
    pygame.draw.rect(screen, BUTTON_COLOR, box, border_radius=6)
    pygame.draw.rect(screen, BUTTON_TEXT, box, 2, border_radius=6)
    draw_text(screen, username or "Type name and press Enter", 60, 155, FONT_MEDIUM, (220, 220, 220))
    if message:
        draw_text(screen, message, 40, 210, FONT_SMALL, (255, 180, 0))


def draw_settings_screen():
    screen.fill(BACKGROUND_COLOR)
    draw_text_center(screen, "Settings", pygame.Rect(0, 20, SCREEN_WIDTH, 40), FONT_LARGE)
    sound_button = Button((40, 80, 140, 35), f"Sound: {'On' if settings['sound'] else 'Off'}")
    grid_button = Button((220, 80, 140, 35), f"Grid: {'On' if settings['grid'] else 'Off'}")
    r_minus = Button((60, 150, 30, 30), "-")
    r_plus = Button((150, 150, 30, 30), "+")
    g_minus = Button((60, 190, 30, 30), "-")
    g_plus = Button((150, 190, 30, 30), "+")
    b_minus = Button((60, 230, 30, 30), "-")
    b_plus = Button((150, 230, 30, 30), "+")
    save_button = Button((120, 270, 160, 40), "Save & Back")

    mouse_pos = pygame.mouse.get_pos()
    for button in [sound_button, grid_button, r_minus, r_plus, g_minus, g_plus, b_minus, b_plus, save_button]:
        button.update(mouse_pos)
        button.draw(screen)

    draw_text(screen, "Snake color:", 40, 120, FONT_SMALL)
    color = tuple(settings["snake_color"])
    color_rect = pygame.Rect(220, 150, 120, 100)
    pygame.draw.rect(screen, color, color_rect)
    pygame.draw.rect(screen, BUTTON_TEXT, color_rect, 2)
    draw_text(screen, f"R: {color[0]}", 200, 155, FONT_SMALL)
    draw_text(screen, f"G: {color[1]}", 200, 195, FONT_SMALL)
    draw_text(screen, f"B: {color[2]}", 200, 235, FONT_SMALL)

    return {
        "sound": sound_button,
        "grid": grid_button,
        "r_minus": r_minus,
        "r_plus": r_plus,
        "g_minus": g_minus,
        "g_plus": g_plus,
        "b_minus": b_minus,
        "b_plus": b_plus,
        "save": save_button,
    }


def draw_leaderboard_screen(entries):
    screen.fill(BACKGROUND_COLOR)
    draw_text_center(screen, "Leaderboard", pygame.Rect(0, 20, SCREEN_WIDTH, 40), FONT_LARGE)
    if not entries:
        draw_text_center(screen, "No leaderboard records yet.", pygame.Rect(0, 120, SCREEN_WIDTH, 40), FONT_MEDIUM)
    else:
        draw_text(screen, "Rank  Username      Score  Level  Date", 20, 80, FONT_SMALL)
        for idx, row in enumerate(entries, start=1):
            date_text = row["played_at"].strftime("%Y-%m-%d") if hasattr(row["played_at"], "strftime") else str(row["played_at"])[:10]
            draw_text(screen, f"{idx:>2}. {row['username']:<12} {row['score']:<6} {row['level_reached']:<6} {date_text}", 20, 90 + idx * 22, FONT_SMALL)
    back_button = Button((120, 260, 160, 40), "Back")
    back_button.update(pygame.mouse.get_pos())
    back_button.draw(screen)
    return back_button


def draw_game_over_screen(session):
    screen.fill(BACKGROUND_COLOR)
    draw_text_center(screen, "Game Over", pygame.Rect(0, 20, SCREEN_WIDTH, 40), FONT_LARGE)
    draw_text(screen, f"Score: {session.score}", 120, 90, FONT_MEDIUM)
    draw_text(screen, f"Level: {session.level}", 120, 120, FONT_MEDIUM)
    draw_text(screen, f"Best: {session.persona_best}", 120, 150, FONT_MEDIUM)
    draw_text(screen, f"Reason: {session.reason}", 40, 190, FONT_SMALL)
    retry_button = Button((40, 240, 140, 40), "Retry")
    menu_button = Button((220, 240, 140, 40), "Main Menu")
    mouse_pos = pygame.mouse.get_pos()
    retry_button.update(mouse_pos)
    menu_button.update(mouse_pos)
    retry_button.draw(screen)
    menu_button.draw(screen)
    return retry_button, menu_button


def run():
    global leaderboard_cache
    load_settings()
    username = ""
    current_state = STATE_USERNAME
    message = ""
    session = None
    leaderboard_cache = get_leaderboard() if db.DB_AVAILABLE else []

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if current_state == STATE_USERNAME:
                if event.type == KEYDOWN:
                    if event.key == K_BACKSPACE:
                        username = username[:-1]
                    elif event.key == K_RETURN:
                        if username.strip():
                            current_state = STATE_MAIN_MENU
                            message = ""
                            leaderboard_cache = get_leaderboard()
                        else:
                            message = "Username cannot be empty."
                    elif len(username) < 12 and event.unicode.isalnum():
                        username += event.unicode
            elif current_state == STATE_MAIN_MENU:
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    buttons = draw_main_menu(username, message, get_personal_best(username))
                    if buttons[0].is_clicked(mouse_pos):
                        session = GameSession(username)
                        current_state = STATE_PLAYING
                    elif buttons[1].is_clicked(mouse_pos):
                        leaderboard_cache = get_leaderboard()
                        current_state = STATE_LEADERBOARD
                    elif buttons[2].is_clicked(mouse_pos):
                        current_state = STATE_SETTINGS
                    elif buttons[3].is_clicked(mouse_pos):
                        pygame.quit()
                        sys.exit()
            elif current_state == STATE_SETTINGS:
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    controls = draw_settings_screen()
                    if controls["sound"].is_clicked(mouse_pos):
                        settings["sound"] = not settings["sound"]
                    elif controls["grid"].is_clicked(mouse_pos):
                        settings["grid"] = not settings["grid"]
                    elif controls["r_minus"].is_clicked(mouse_pos):
                        settings["snake_color"][0] = clamp(settings["snake_color"][0] - 5, 0, 255)
                    elif controls["r_plus"].is_clicked(mouse_pos):
                        settings["snake_color"][0] = clamp(settings["snake_color"][0] + 5, 0, 255)
                    elif controls["g_minus"].is_clicked(mouse_pos):
                        settings["snake_color"][1] = clamp(settings["snake_color"][1] - 5, 0, 255)
                    elif controls["g_plus"].is_clicked(mouse_pos):
                        settings["snake_color"][1] = clamp(settings["snake_color"][1] + 5, 0, 255)
                    elif controls["b_minus"].is_clicked(mouse_pos):
                        settings["snake_color"][2] = clamp(settings["snake_color"][2] - 5, 0, 255)
                    elif controls["b_plus"].is_clicked(mouse_pos):
                        settings["snake_color"][2] = clamp(settings["snake_color"][2] + 5, 0, 255)
                    elif controls["save"].is_clicked(mouse_pos):
                        save_settings()
                        current_state = STATE_MAIN_MENU
            elif current_state == STATE_LEADERBOARD:
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    back_button = draw_leaderboard_screen(leaderboard_cache)
                    if back_button.is_clicked(mouse_pos):
                        current_state = STATE_MAIN_MENU
            elif current_state == STATE_PLAYING:
                if event.type == KEYDOWN:
                    if event.key == K_UP:
                        session.snake.change_direction("UP")
                    elif event.key == K_DOWN:
                        session.snake.change_direction("DOWN")
                    elif event.key == K_LEFT:
                        session.snake.change_direction("LEFT")
                    elif event.key == K_RIGHT:
                        session.snake.change_direction("RIGHT")
            elif current_state == STATE_GAME_OVER:
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    retry_button, menu_button = draw_game_over_screen(session)
                    if retry_button.is_clicked(mouse_pos):
                        session = GameSession(username)
                        current_state = STATE_PLAYING
                    elif menu_button.is_clicked(mouse_pos):
                        current_state = STATE_MAIN_MENU

        if current_state == STATE_USERNAME:
            draw_username_screen(username, message)
        elif current_state == STATE_MAIN_MENU:
            draw_main_menu(username, message, get_personal_best(username))
        elif current_state == STATE_SETTINGS:
            draw_settings_screen()
        elif current_state == STATE_LEADERBOARD:
            draw_leaderboard_screen(leaderboard_cache)
        elif current_state == STATE_PLAYING:
            if session:
                session.update()
                session.draw(screen)
                if session.game_over:
                    current_state = STATE_GAME_OVER
        elif current_state == STATE_GAME_OVER:
            draw_game_over_screen(session)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    run()

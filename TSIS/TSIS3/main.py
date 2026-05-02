import os
import sys
import random
import pygame
from pygame.locals import *

pygame.init()
pygame.font.init()
try:
    pygame.mixer.init()
except Exception:
    pass

from racer import Player, TrafficCar, Coin, Hazard, PowerUp, SCREEN_WIDTH, SCREEN_HEIGHT, LANES
from persistence import load_settings, save_settings, load_leaderboard, add_leaderboard_entry
from ui import Button, draw_text, draw_text_center

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer Arcade")
clock = pygame.time.Clock()

FONT_LARGE = pygame.font.SysFont("Verdana", 48)
FONT_MEDIUM = pygame.font.SysFont("Verdana", 26)
FONT_SMALL = pygame.font.SysFont("Verdana", 18)

STATE_USERNAME = "username"
STATE_MAIN_MENU = "main_menu"
STATE_SETTINGS = "settings"
STATE_LEADERBOARD = "leaderboard"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"

DIFFICULTY_CONFIG = {
    "easy": {
        "base_speed": 4,
        "traffic_rate": 1700,
        "hazard_rate": 2400,
        "powerup_rate": 9000,
        "target_distance": 5000
    },
    "medium": {
        "base_speed": 5,
        "traffic_rate": 1400,
        "hazard_rate": 2100,
        "powerup_rate": 8200,
        "target_distance": 7500
    },
    "hard": {
        "base_speed": 6,
        "traffic_rate": 1100,
        "hazard_rate": 1800,
        "powerup_rate": 7400,
        "target_distance": 10000
    }
}

CAR_COLORS = ["blue", "red", "green", "yellow"]
POWERUP_TYPES = ["nitro", "shield", "repair"]
HAZARD_TYPES = ["barrier", "oil", "pothole", "boost"]

settings = load_settings()
leaderboard = load_leaderboard()

background_path = os.path.join(os.path.dirname(__file__), "images", "background.jpg")
background = pygame.image.load(background_path).convert()
background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

coin_sound = None
crash_sound = None
if pygame.mixer.get_init():
    try:
        coin_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sounds", "coin.mp3"))
        crash_sound = pygame.mixer.Sound(os.path.join(os.path.dirname(__file__), "sounds", "crash.mp3"))
    except Exception:
        coin_sound = None
        crash_sound = None


def play_sound(sound):
    if settings.get("sound", True) and sound:
        sound.play()


def clamp(value, minimum, maximum):
    return max(minimum, min(maximum, value))


def get_setting_label():
    sound_label = "On" if settings.get("sound", True) else "Off"
    return f"Sound: {sound_label}"


def draw_split_title(surface, title, y):
    title_rect = pygame.Rect(0, y, SCREEN_WIDTH, 60)
    draw_text_center(surface, title, title_rect, FONT_LARGE)


class GameSession:
    def __init__(self, username, settings):
        self.username = username
        self.settings = settings
        self.reset()

    def reset(self):
        self.player = Player(self.settings.get("car_color", "blue"))
        self.player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)

        self.coins = pygame.sprite.Group(Coin())
        self.traffic = pygame.sprite.Group()
        self.hazards = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()

        self.distance = 0
        self.score = 0
        self.coins_collected = 0
        self.powerup_bonus = 0
        self.active_powerup = None
        self.powerup_end_time = 0
        self.shield_active = False
        self.slow_until = 0
        self.game_over_reason = ""
        self.finished = False
        self.saved_to_leaderboard = False

        self.difficulty = self.settings.get("difficulty", "medium")
        self.difficulty_config = DIFFICULTY_CONFIG.get(self.difficulty, DIFFICULTY_CONFIG["medium"])
        self.target_distance = self.difficulty_config["target_distance"]
        self.last_spawn = pygame.time.get_ticks()
        self.next_traffic = pygame.time.get_ticks()
        self.next_hazard = pygame.time.get_ticks()
        self.next_powerup = pygame.time.get_ticks()

    def current_speed(self):
        speed = self.difficulty_config["base_speed"] + (self.distance / 2500.0)
        if self.active_powerup == "Nitro":
            speed += 3.5
        if self.slow_until > pygame.time.get_ticks():
            speed = max(2, speed - 2)
        return speed

    def total_score(self):
        return self.score + int(self.distance / 10) + self.powerup_bonus

    def _spawn_lane_x(self):
        choices = [x for x in LANES if abs(x - self.player.rect.centerx) > 100]
        if not choices:
            choices = LANES[:]
        return random.choice(choices)

    def spawn_traffic(self):
        car = TrafficCar()
        car.reset_position(self.player.rect)
        self.traffic.add(car)

    def spawn_hazard(self):
        kind = random.choices(HAZARD_TYPES, weights=[35, 25, 25, 15], k=1)[0]
        hazard = Hazard(kind)
        hazard.reset_position(self.player.rect)
        self.hazards.add(hazard)

    def spawn_powerup(self):
        kind = random.choice(POWERUP_TYPES)
        powerup = PowerUp(kind)
        powerup.reset_position(self.player.rect)
        self.powerups.add(powerup)

    def activate_powerup(self, kind):
        if kind == "nitro":
            self.active_powerup = "Nitro"
            self.powerup_end_time = pygame.time.get_ticks() + random.randint(3000, 5000)
            self.powerup_bonus += 10
        elif kind == "shield":
            self.active_powerup = "Shield"
            self.shield_active = True
            self.powerup_end_time = 0
            self.powerup_bonus += 8
        elif kind == "repair":
            self.apply_repair()
            self.active_powerup = "Repair"
            self.powerup_end_time = pygame.time.get_ticks() + 1000
            self.powerup_bonus += 5

    def apply_repair(self):
        self.slow_until = pygame.time.get_ticks()
        if self.hazards:
            hazard = next(iter(self.hazards))
            hazard.kill()

    def update_powerup_state(self):
        if self.active_powerup == "Nitro" and pygame.time.get_ticks() > self.powerup_end_time:
            self.active_powerup = None
        if self.active_powerup == "Repair" and pygame.time.get_ticks() > self.powerup_end_time:
            self.active_powerup = None

    def update(self, dt):
        if self.finished:
            return

        now = pygame.time.get_ticks()
        self.player.move()

        speed = self.current_speed()
        self.distance += speed * dt * 0.04

        if now >= self.next_traffic:
            self.spawn_traffic()
            interval = max(600, self.difficulty_config["traffic_rate"] - int(self.distance / 20))
            self.next_traffic = now + interval

        if now >= self.next_hazard:
            self.spawn_hazard()
            interval = max(900, self.difficulty_config["hazard_rate"] - int(self.distance / 25))
            self.next_hazard = now + interval

        if now >= self.next_powerup:
            self.spawn_powerup()
            interval = max(7000, self.difficulty_config["powerup_rate"] - int(self.distance / 40))
            self.next_powerup = now + interval

        for coin in list(self.coins):
            coin.move(speed)
            if coin.rect.top > SCREEN_HEIGHT:
                coin.reset_position(self.player.rect)

        for car in list(self.traffic):
            car.move(speed)

        for hazard in list(self.hazards):
            hazard.move(speed)

        for powerup in list(self.powerups):
            if powerup.expired():
                powerup.kill()
            else:
                powerup.move(speed)

        self.handle_collisions()
        self.update_powerup_state()

        if self.distance >= self.target_distance:
            self.finished = True
            self.game_over_reason = "Finish line reached!"

    def handle_collisions(self):
        coin_hit = pygame.sprite.spritecollideany(self.player, self.coins)
        if coin_hit:
            value = random.choices(list(range(1, 6)), weights=[20, 10, 10, 5, 2], k=1)[0]
            self.score += value
            self.coins_collected += 1
            play_sound(coin_sound)
            coin_hit.reset_position(self.player.rect)

        traffic_hit = pygame.sprite.spritecollideany(self.player, self.traffic)
        if traffic_hit:
            if self.shield_active:
                self.shield_active = False
                self.active_powerup = None
                traffic_hit.kill()
                self.score += 5
            else:
                self.game_over_reason = "Crashed into traffic"
                self.finished = True
                play_sound(crash_sound)
                return

        hazard_hit = pygame.sprite.spritecollideany(self.player, self.hazards)
        if hazard_hit:
            if hazard_hit.kind == "barrier":
                if self.shield_active:
                    self.shield_active = False
                    self.active_powerup = None
                    self.score += 5
                else:
                    self.game_over_reason = "Hit a barrier"
                    self.finished = True
                    play_sound(crash_sound)
                    return
            elif hazard_hit.kind == "oil":
                self.slow_until = pygame.time.get_ticks() + 1500
                self.score = max(0, self.score - 2)
            elif hazard_hit.kind == "pothole":
                self.score = max(0, self.score - 3)
            elif hazard_hit.kind == "boost":
                if self.active_powerup is None:
                    self.activate_powerup("nitro")
            hazard_hit.kill()

        powerup_hit = pygame.sprite.spritecollideany(self.player, self.powerups)
        if powerup_hit:
            if powerup_hit.kind == "repair":
                self.apply_repair()
                self.active_powerup = "Repair"
                self.powerup_end_time = pygame.time.get_ticks() + 1200
            elif self.active_powerup is None:
                self.activate_powerup(powerup_hit.kind)
            powerup_hit.kill()

    def draw(self, surface, bg_y):
        surface.blit(background, (0, bg_y))
        surface.blit(background, (0, bg_y - SCREEN_HEIGHT))

        for lane_x in LANES:
            for y in range(0, SCREEN_HEIGHT, 40):
                pygame.draw.line(surface, (180, 180, 180), (lane_x, y), (lane_x, y + 20), 4)

        self.coins.draw(surface)
        self.hazards.draw(surface)
        self.powerups.draw(surface)
        self.traffic.draw(surface)
        surface.blit(self.player.image, self.player.rect)

        score_text = f"Score: {self.score}"
        draw_text(surface, score_text, 10, 10, FONT_SMALL)
        draw_text(surface, f"Coins: {self.coins_collected}", 10, 32, FONT_SMALL)
        draw_text(surface, f"Distance: {int(self.distance)}m / {self.target_distance}m", 10, 54, FONT_SMALL)
        powerup_text = self.active_powerup or "None"
        if self.active_powerup == "Nitro":
            remaining = max(0, int((self.powerup_end_time - pygame.time.get_ticks()) / 1000))
            powerup_text = f"Nitro ({remaining}s)"
        draw_text(surface, f"Power-Up: {powerup_text}", 10, 76, FONT_SMALL)
        draw_text(surface, f"Difficulty: {self.difficulty.title()}", 10, 98, FONT_SMALL)

    def collect_end_score(self):
        return {
            "name": self.username,
            "score": self.total_score(),
            "distance": int(self.distance),
            "coins": self.coins_collected
        }


def draw_main_menu():
    screen.fill((30, 30, 40))
    draw_split_title(screen, "Racer Arcade", 40)
    buttons = [
        Button((110, 170, 180, 50), "Play", FONT_MEDIUM),
        Button((110, 240, 180, 50), "Leaderboard", FONT_MEDIUM),
        Button((110, 310, 180, 50), "Settings", FONT_MEDIUM),
        Button((110, 380, 180, 50), "Quit", FONT_MEDIUM)
    ]
    mouse_pos = pygame.mouse.get_pos()
    for button in buttons:
        button.update(mouse_pos)
        button.draw(screen)
    return buttons


def draw_username_screen(username):
    screen.fill((20, 20, 30))
    draw_split_title(screen, "Enter Driver Name", 120)
    prompt_rect = pygame.Rect(50, 240, SCREEN_WIDTH - 100, 60)
    pygame.draw.rect(screen, (50, 50, 70), prompt_rect, border_radius=10)
    draw_text_center(screen, username or "Type name and press Enter", prompt_rect, FONT_MEDIUM, (200, 200, 200))
    draw_text(screen, "Use letters and numbers only.", 80, 340, FONT_SMALL, (180, 180, 180))


def draw_settings_screen():
    screen.fill((24, 24, 30))
    draw_split_title(screen, "Settings", 40)
    sound_button = Button((110, 160, 180, 45), get_setting_label(), FONT_MEDIUM)
    color_buttons = [Button((50 + i * 90, 240, 80, 40), name.title(), FONT_SMALL) for i, name in enumerate(CAR_COLORS)]
    difficulty_buttons = [Button((50 + i * 90, 320, 80, 40), level.title(), FONT_SMALL) for i, level in enumerate(DIFFICULTY_CONFIG.keys())]
    back_button = Button((120, 420, 160, 45), "Back", FONT_MEDIUM)

    draw_text(screen, "Car Color:", 50, 210, FONT_SMALL)
    draw_text(screen, "Difficulty:", 50, 290, FONT_SMALL)

    mouse_pos = pygame.mouse.get_pos()
    for button in color_buttons + difficulty_buttons + [sound_button, back_button]:
        button.update(mouse_pos)
        button.draw(screen)
        if button.text.lower() == settings.get("car_color", "blue"):
            pygame.draw.rect(screen, (255, 255, 255), button.rect, 2, border_radius=8)
        if button.text.lower() == settings.get("difficulty", "medium"):
            pygame.draw.rect(screen, (255, 255, 255), button.rect, 2, border_radius=8)

    return sound_button, color_buttons, difficulty_buttons, back_button


def draw_leaderboard_screen(scores):
    screen.fill((20, 20, 25))
    draw_split_title(screen, "Leaderboard", 30)
    y = 120
    if not scores:
        draw_text_center(screen, "No scores yet", pygame.Rect(0, y, SCREEN_WIDTH, 40), FONT_MEDIUM, (200, 200, 200))
    else:
        draw_text(screen, "Rank  Name       Score   Distance", 30, y, FONT_SMALL)
        y += 30
        for index, entry in enumerate(scores, start=1):
            line = f"{index:>2}. {entry['name'][:8]:<8}  {entry['score']:<6}  {entry['distance']:>5}m"
            draw_text(screen, line, 40, y, FONT_SMALL)
            y += 28
    back_button = Button((120, 500, 160, 45), "Back", FONT_MEDIUM)
    back_button.update(pygame.mouse.get_pos())
    back_button.draw(screen)
    return back_button


def draw_game_over_screen(session):
    screen.fill((30, 10, 10))
    draw_split_title(screen, "Game Over", 40)
    draw_text_center(screen, session.game_over_reason or "Run Complete", pygame.Rect(0, 120, SCREEN_WIDTH, 40), FONT_MEDIUM)
    draw_text(screen, f"Total Score: {session.total_score()}", 90, 200, FONT_MEDIUM)
    draw_text(screen, f"Distance: {int(session.distance)}m", 90, 240, FONT_MEDIUM)
    draw_text(screen, f"Coins: {session.coins_collected}", 90, 280, FONT_MEDIUM)
    retry_button = Button((50, 360, 130, 45), "Retry", FONT_MEDIUM)
    menu_button = Button((220, 360, 130, 45), "Menu", FONT_MEDIUM)
    mouse_pos = pygame.mouse.get_pos()
    for button in (retry_button, menu_button):
        button.update(mouse_pos)
        button.draw(screen)
    return retry_button, menu_button


def main():
    state = STATE_USERNAME
    username = ""
    session = None
    bg_y = 0
    running = True

    while running:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif state == STATE_USERNAME:
                if event.type == KEYDOWN:
                    if event.key == K_BACKSPACE:
                        username = username[:-1]
                    elif event.key == K_RETURN:
                        if username.strip():
                            state = STATE_MAIN_MENU
                    elif event.unicode.isalnum() and len(username) < 12:
                        username += event.unicode
            elif state == STATE_MAIN_MENU:
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    mx, my = event.pos
                    play_btn, leader_btn, settings_btn, quit_btn = draw_main_menu()
                    if play_btn.is_clicked((mx, my)):
                        session = GameSession(username, settings)
                        state = STATE_PLAYING
                    elif leader_btn.is_clicked((mx, my)):
                        state = STATE_LEADERBOARD
                    elif settings_btn.is_clicked((mx, my)):
                        state = STATE_SETTINGS
                    elif quit_btn.is_clicked((mx, my)):
                        running = False
            elif state == STATE_SETTINGS:
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    sound_btn, color_buttons, difficulty_buttons, back_btn = draw_settings_screen()
                    pos = event.pos
                    if sound_btn.is_clicked(pos):
                        settings["sound"] = not settings.get("sound", True)
                        save_settings(settings)
                        if session:
                            pass
                    for button in color_buttons:
                        if button.is_clicked(pos):
                            chosen = button.text.lower()
                            settings["car_color"] = chosen
                            save_settings(settings)
                            if session:
                                session.player.set_color(chosen)
                    for button in difficulty_buttons:
                        if button.is_clicked(pos):
                            settings["difficulty"] = button.text.lower()
                            save_settings(settings)
                            if session:
                                session.difficulty = settings["difficulty"]
                                session.difficulty_config = DIFFICULTY_CONFIG[settings["difficulty"]]
                                session.target_distance = session.difficulty_config["target_distance"]
                    if back_btn.is_clicked(pos):
                        state = STATE_MAIN_MENU
            elif state == STATE_LEADERBOARD:
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    back_btn = draw_leaderboard_screen(leaderboard)
                    if back_btn.is_clicked(event.pos):
                        state = STATE_MAIN_MENU
            elif state == STATE_GAME_OVER:
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    retry_btn, menu_btn = draw_game_over_screen(session)
                    if retry_btn.is_clicked(event.pos):
                        session = GameSession(username, settings)
                        state = STATE_PLAYING
                    elif menu_btn.is_clicked(event.pos):
                        state = STATE_MAIN_MENU

        if state == STATE_MAIN_MENU:
            buttons = draw_main_menu()
        elif state == STATE_USERNAME:
            draw_username_screen(username)
        elif state == STATE_SETTINGS:
            draw_settings_screen()
        elif state == STATE_LEADERBOARD:
            draw_leaderboard_screen(leaderboard)
        elif state == STATE_PLAYING:
            if session is None:
                session = GameSession(username, settings)
            session.update(dt)
            bg_y = (bg_y + session.current_speed()) % SCREEN_HEIGHT
            session.draw(screen, bg_y)
            if session.finished:
                if not session.saved_to_leaderboard:
                    leaderboard_entry = session.collect_end_score()
                    leaderboard = add_leaderboard_entry(leaderboard_entry)
                    session.saved_to_leaderboard = True
                state = STATE_GAME_OVER
        elif state == STATE_GAME_OVER:
            draw_game_over_screen(session)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

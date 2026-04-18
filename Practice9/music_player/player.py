import pygame
from pathlib import Path

def centering(something, surface):
    s_w, s_h = surface.get_size()
    obj_w, obj_h = something.get_size()
    
    # Calculate the top-left corner needed to center it
    center_x = (s_w - obj_w) // 2
    center_y = (s_h - obj_h) // 2
    
    return (center_x, center_y)

class Player:
    def __init__(self, screen):
        dir_path = Path('music')
        self.list = [child.name for child in dir_path.iterdir() if child.suffix == '.mp3']
        self.iter = 0
        self.screen = screen
        self.current_song_name = ""
        self.font = pygame.font.SysFont("sans", 24)
        self.toggle = False

    def next_song(self):
        self.iter = (self.iter + 1) % len(self.list)
        self.play()

    def prev_song(self):
        self.iter = (self.iter - 1) if self.iter > 0 else len(self.list) - 1 
        self.play()

    def play(self):
        self.toggle = True
        if not self.list:
            print("No music files found!")
            return

        selected = self.list[self.iter]
        path = f"music/{selected}"
        
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()
        
        self.current_song_name = selected[:-4]

    def draw(self):
        if not self.current_song_name: return

        text_surface = self.font.render(self.current_song_name, True, (0, 0, 0))
        self.screen.blit(text_surface, centering(text_surface, self.screen))

    def stop(self):
        pygame.mixer.music.stop()
        self.current_song_name = ""
        self.toggle = False
    def pause(self):
        if self.toggle:
            pygame.mixer.music.pause()
            self.toggle = False
        else:
            pygame.mixer.music.unpause()
            self.toggle = True
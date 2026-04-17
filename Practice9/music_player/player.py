import pygame
import os

class Player:
    def __init__(self):
        pygame.mixer.init()
        self.songs = []
        self.current = 0
        
        
        if os.path.exists("music"):
            self.songs = [os.path.join("music", f) for f in os.listdir("music") if f.endswith(('.mp3', '.wav'))]

    def play(self):
        if self.songs:
            pygame.mixer.music.load(self.songs[self.current])
            pygame.mixer.music.play()

    def stop(self):
        pygame.mixer.music.stop()

    def next(self):
        if self.songs:
            self.current = (self.current + 1) % len(self.songs)
            self.play()

    def prev(self):
        if self.songs:
            self.current = (self.current - 1) % len(self.songs)
            self.play()

    def get_name(self):
        if self.songs:
            return os.path.basename(self.songs[self.current])
        return "No music"
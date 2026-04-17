import pygame

class Ball:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.step = 20

    def move_up(self):
        if self.y - self.step >= self.radius:
            self.y -= self.step

    def move_down(self, screen_height):
        if self.y + self.step <= screen_height - self.radius:
            self.y += self.step

    def move_left(self):
        if self.x - self.step >= self.radius:
            self.x -= self.step

    def move_right(self, screen_width):
        if self.x + self.step <= screen_width - self.radius:
            self.x += self.step

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
import pygame
from color_palette import *
import random

pygame.init()

WIDTH = 600
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

CELL = 30

score = 0
level = 1
FPS = 5


def draw_grid():
    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colorGRAY, (i * CELL, j * CELL, CELL, CELL), 1)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0

    def move(self):
        # Двигаем тело змейки за головой
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y

        # Двигаем голову
        self.body[0].x += self.dx
        self.body[0].y += self.dy

    def draw(self):
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))

        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_wall_collision(self):
        head = self.body[0]

        # Если змейка вышла за границу — game over
        if head.x < 0 or head.x >= WIDTH // CELL:
            return True

        if head.y < 0 or head.y >= HEIGHT // CELL:
            return True

        return False

    def check_self_collision(self):
        head = self.body[0]

        # Проверяем, ударилась ли голова об тело
        for segment in self.body[1:]:
            if head.x == segment.x and head.y == segment.y:
                return True

        return False

    def check_food_collision(self, food):
        global score, level, FPS

        head = self.body[0]

        if head.x == food.pos.x and head.y == food.pos.y:
            score += 1

            # Добавляем новый сегмент
            self.body.append(Point(head.x, head.y))

            # Каждые 3 еды повышаем уровень
            if score % 3 == 0:
                level += 1
                FPS += 2

            food.generate_random_pos(self)


class Food:
    def __init__(self):
        self.pos = Point(9, 9)

    def draw(self):
        pygame.draw.rect(screen, colorGREEN, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    def generate_random_pos(self, snake):
        while True:
            x = random.randint(0, WIDTH // CELL - 1)
            y = random.randint(0, HEIGHT // CELL - 1)

            # Еда не должна появляться на змейке
            on_snake = False
            for segment in snake.body:
                if segment.x == x and segment.y == y:
                    on_snake = True
                    break

            if not on_snake:
                self.pos = Point(x, y)
                break


clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 25)

food = Food()
snake = Snake()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and snake.dx != -1:
                snake.dx = 1
                snake.dy = 0
            elif event.key == pygame.K_LEFT and snake.dx != 1:
                snake.dx = -1
                snake.dy = 0
            elif event.key == pygame.K_DOWN and snake.dy != -1:
                snake.dx = 0
                snake.dy = 1
            elif event.key == pygame.K_UP and snake.dy != 1:
                snake.dx = 0
                snake.dy = -1

    screen.fill(colorBLACK)
    draw_grid()

    snake.move()

    # Проверка стены и тела
    if snake.check_wall_collision() or snake.check_self_collision():
        running = False

    snake.check_food_collision(food)

    snake.draw()
    food.draw()

    # Score и Level
    text = font.render(f"Score: {score}  Level: {level}", True, colorWHITE)
    screen.blit(text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
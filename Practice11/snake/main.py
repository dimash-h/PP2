import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Константы
WIDTH = 600
HEIGHT = 400
BLOCK_SIZE = 20

# Цвета
from color_palette import *

WHITE = colorWHITE
BLACK = colorBLACK
GREEN = colorGREEN  # Цвет змейки
RED   = colorRED  # Еда с весом 1
YELLOW= colorYELLOW # Еда с весом 2
BLUE  = colorBLUE  # Еда с весом 3

FOOD_TIMER_MS = 5000 # Еда исчезает через 5 секунд

# Настройка экрана
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

# Шрифты
font = pygame.font.SysFont("Verdana", 20)
font_large = pygame.font.SysFont("Verdana", 50)

def generate_food(snake_body):
    """
    Генерирует случайную позицию и вес для еды.
    Убеждается, что еда не появляется внутри стены или на теле змейки.
    Возвращает словарь с позицией, весом и временем появления.
    """
    while True:
        # Генерация случайных координат с выравниванием по сетке
        food_x = random.randrange(0, WIDTH, BLOCK_SIZE)
        food_y = random.randrange(0, HEIGHT, BLOCK_SIZE)
        
        # Проверка, что еда не на теле змейки
        if [food_x, food_y] not in snake_body:
            weight = random.choice([1, 2, 3])
            return {
                'pos': [food_x, food_y],
                'weight': weight,
                'time': pygame.time.get_ticks()
            }

def game_over_screen(score, level):
    """Отображает экран Game Over с финальным счетом и уровнем."""
    DISPLAYSURF.fill(BLACK)
    
    # Отрисовка текста
    go_text = font_large.render("Game Over!", True, RED)
    score_text = font.render(f"Final Score: {score} | Final Level: {level}", True, WHITE)
    
    # Центрирование текста
    go_rect = go_text.get_rect(center=(WIDTH/2, HEIGHT/2 - 20))
    score_rect = score_text.get_rect(center=(WIDTH/2, HEIGHT/2 + 30))
    
    DISPLAYSURF.blit(go_text, go_rect)
    DISPLAYSURF.blit(score_text, score_rect)
    
    pygame.display.update()
    pygame.time.delay(3000)
    pygame.quit()
    sys.exit()

def main():
    # Начальная позиция змейки и её тело
    snake_pos = [100, 60]
    snake_body = [[100, 60], [80, 60], [60, 60]]
    
    # Генерация первой еды
    food = generate_food(snake_body)
    food_spawn = True
    
    # Переменные направления
    direction = 'RIGHT'
    change_to = direction
    
    # Переменные состояния игры
    score = 0
    level = 1
    speed = 10 # Начальное количество кадров в секунду (скорость)
    
    clock = pygame.time.Clock()

    while True:
        # 1. Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Обработка нажатий клавиш для смены направления
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'

        # Предотвращение движения змейки в противоположном направлении
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # 2. Движение змейки
        if direction == 'UP':
            snake_pos[1] -= BLOCK_SIZE
        if direction == 'DOWN':
            snake_pos[1] += BLOCK_SIZE
        if direction == 'LEFT':
            snake_pos[0] -= BLOCK_SIZE
        if direction == 'RIGHT':
            snake_pos[0] += BLOCK_SIZE

        # 3. Механизм роста тела змейки
        snake_body.insert(0, list(snake_pos))
        
        # Проверка, съедена ли еда
        if snake_pos[0] == food['pos'][0] and snake_pos[1] == food['pos'][1]:
            score += food['weight']
            # Увеличение уровня каждые 4 очка
            new_level = 1 + (score // 4)
            if new_level > level:
                speed += 2 * (new_level - level) # Динамическое увеличение скорости
                level = new_level
            food_spawn = False
        else:
            # Если еда не съедена, удаляем последний сегмент хвоста
            snake_body.pop()

        # Проверка истечения таймера еды
        current_time = pygame.time.get_ticks()
        if current_time - food['time'] > FOOD_TIMER_MS:
            food_spawn = False # Принудительное создание новой еды

        # Генерация новой еды при необходимости
        if not food_spawn:
            food = generate_food(snake_body)
        food_spawn = True

        # 4. Проверка столкновений (логика Game Over)
        # Проверка столкновения с границами экрана (стенами)
        if snake_pos[0] < 0 or snake_pos[0] > WIDTH - BLOCK_SIZE:
            game_over_screen(score, level)
        if snake_pos[1] < 0 or snake_pos[1] > HEIGHT - BLOCK_SIZE:
            game_over_screen(score, level)

        # Проверка столкновения с собственным телом
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over_screen(score, level)

        # 5. Фаза отрисовки
        DISPLAYSURF.fill(BLACK) # Очистка экрана

        # Отрисовка змейки
        for pos in snake_body:
            pygame.draw.rect(DISPLAYSURF, GREEN, pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
            
        # Отрисовка еды в зависимости от её веса
        food_color = {1: RED, 2: YELLOW, 3: BLUE}[food['weight']]
        pygame.draw.rect(DISPLAYSURF, food_color, pygame.Rect(food['pos'][0], food['pos'][1], BLOCK_SIZE, BLOCK_SIZE))

        # Отображение счета и уровня в левом верхнем углу
        score_text = font.render(f"Score: {score}  |  Level: {level}", True, WHITE)
        DISPLAYSURF.blit(score_text, (10, 10))

        # Обновление экрана и счетчик кадров
        pygame.display.update()
        clock.tick(speed)

if __name__ == "__main__":
    main()

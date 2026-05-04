import pygame
import random
#Вся логика игры — змейка, еда, бонусы, столкновения
BLOCK_SIZE = 20
WIDTH = 600
HEIGHT = 400

class Food:
    """
    Класс для управления едой
    """
    def __init__(self, is_poison=False):
        self.is_poison = is_poison
        self.pos = [0, 0]
        self.weight = 1 if is_poison else random.choice([1, 2, 3])
        self.time = pygame.time.get_ticks()

    def generate(self, snake_body, obstacles): # Позиция еды
        while True:
            x = random.randrange(0, WIDTH, BLOCK_SIZE)
            y = random.randrange(0, HEIGHT, BLOCK_SIZE)
            if [x, y] not in snake_body and [x, y] not in obstacles:
                self.pos = [x, y]
                self.time = pygame.time.get_ticks()
                break

class PowerUp:
    """
    Класс для бонусов
    """
    def __init__(self):
        self.type = random.choice(['speed', 'slow', 'shield'])
        self.pos = [0, 0]
        self.spawn_time = pygame.time.get_ticks()
        self.active = True

    def generate(self, snake_body, obstacles, foods):
        while True:
            x = random.randrange(0, WIDTH, BLOCK_SIZE)
            y = random.randrange(0, HEIGHT, BLOCK_SIZE)
            if [x, y] not in snake_body and [x, y] not in obstacles and all([x, y] != f.pos for f in foods):
                self.pos = [x, y]
                self.spawn_time = pygame.time.get_ticks()
                self.active = True
                break

class GameState:
    """
    Основной класс состояния игры
    """
    def __init__(self, username, pb):
        self.username = username
        self.pb = pb  # Personal Best
        self.reset() #чтобы не дублировать код

    def reset(self):
        """Сбрасывает игру в начальное состояние при старте и рестарте."""
        self.snake_pos = [WIDTH//2, HEIGHT//2]
        self.snake_body = [[self.snake_pos[0], self.snake_pos[1]],
                           [self.snake_pos[0] - BLOCK_SIZE, self.snake_pos[1]],
                           [self.snake_pos[0] - 2 * BLOCK_SIZE, self.snake_pos[1]]]
        self.direction = 'RIGHT'
        self.change_to = self.direction
        self.score = 0
        self.level = 1
        self.base_speed = 10
        self.speed = self.base_speed
        
        self.obstacles = []
        self.foods = [Food(is_poison=False)]
        self.foods[0].generate(self.snake_body, self.obstacles)
        
        self.poison_food = None
        self.powerup = None
        
        self.shield_active = False
        self.effect_timer = 0
        self.effect_duration = 0
        self.active_effect = None # 'speed' or 'slow'
        
        self.game_over = False

    def generate_obstacles(self):
        """
        Генерация препятствий начиная с 3-го уровня.
        Убеждаемся, что препятствия не появляются прямо на змейке.
        """
        self.obstacles = []
        if self.level >= 3:
            num_blocks = self.level * 2 # Чем выше уровень — тем больше препятствий
            for _ in range(num_blocks):
                while True:
                    x = random.randrange(0, WIDTH, BLOCK_SIZE)
                    y = random.randrange(0, HEIGHT, BLOCK_SIZE)
                   #препятствие не рядом со змейкой
                    dist = abs(self.snake_pos[0] - x) + abs(self.snake_pos[1] - y)
                    if [x, y] not in self.snake_body and dist > 4 * BLOCK_SIZE:
                        if all([x, y] != f.pos for f in self.foods) and \
                           (not self.poison_food or [x, y] != self.poison_food.pos) and \
                           (not self.powerup or [x, y] != self.powerup.pos):
                            self.obstacles.append([x, y])
                            break

    def update(self):
        """
        Обновление логики игры на каждый кадр:
        """
        if self.game_over:
            return

        # Обработка движения
        if self.change_to == 'UP' and self.direction != 'DOWN':
            self.direction = 'UP'
        if self.change_to == 'DOWN' and self.direction != 'UP':
            self.direction = 'DOWN'
        if self.change_to == 'LEFT' and self.direction != 'RIGHT':
            self.direction = 'LEFT'
        if self.change_to == 'RIGHT' and self.direction != 'LEFT':
            self.direction = 'RIGHT'

        # Движение змейки
        if self.direction == 'UP':
            self.snake_pos[1] -= BLOCK_SIZE
        if self.direction == 'DOWN':
            self.snake_pos[1] += BLOCK_SIZE
        if self.direction == 'LEFT':
            self.snake_pos[0] -= BLOCK_SIZE
        if self.direction == 'RIGHT':
            self.snake_pos[0] += BLOCK_SIZE

        self.snake_body.insert(0, list(self.snake_pos))

        ate_food = False
        
        # Проверка обычной еды
        for f in self.foods:
            if self.snake_pos == f.pos:
                self.score += f.weight
                ate_food = True
                f.generate(self.snake_body, self.obstacles)
                # Повышение уровня каждые 5 очков
                new_level = 1 + (self.score // 5)
                if new_level > self.level:
                    self.level = new_level
                    self.base_speed += 1 # Скорость растёт с каждым уровнем
                    self.generate_obstacles()
                break
                
        # Проверка ядовитой еды
        if self.poison_food and self.snake_pos == self.poison_food.pos:
            if len(self.snake_body) > 4:
                # Отрезаем 2 сегмента
                self.snake_body = self.snake_body[:-2]
                self.poison_food = None
            else:
                self.game_over = True
                return

        # Проверка бонусов
        if self.powerup and self.powerup.active and self.snake_pos == self.powerup.pos:
            if self.powerup.type == 'speed':
                self.active_effect = 'speed'
                self.effect_timer = pygame.time.get_ticks()
                self.effect_duration = 5000 #5 секунд
                self.speed = self.base_speed + 5
            elif self.powerup.type == 'slow':
                self.active_effect = 'slow'
                self.effect_timer = pygame.time.get_ticks()
                self.effect_duration = 5000
                self.speed = max(5, self.base_speed - 5)
            elif self.powerup.type == 'shield':
                self.shield_active = True
            self.powerup = None
        #хвост
        if not ate_food:
            self.snake_body.pop()

        # Таймеры
        curr_time = pygame.time.get_ticks()
        
        # Спавн бонусов
        if not self.powerup and random.random() < 0.01: # 1% шанс
            self.powerup = PowerUp()
            self.powerup.generate(self.snake_body, self.obstacles, self.foods)
        elif self.powerup and curr_time - self.powerup.spawn_time > 8000: # Бонус исчезает через 8 секунд
            self.powerup = None

        # Ядовитая еда
        if not self.poison_food and random.random() < 0.02:
            self.poison_food = Food(is_poison=True)
            self.poison_food.generate(self.snake_body, self.obstacles)
        elif self.poison_food and curr_time - self.poison_food.time > 6000:
            self.poison_food = None

        # Таймер обычной еды
        for f in self.foods:
            if curr_time - f.time > 5000:
                f.generate(self.snake_body, self.obstacles)

        # Таймер эффекта скорости
        if self.active_effect and curr_time - self.effect_timer > self.effect_duration:
            self.active_effect = None
            self.speed = self.base_speed

        # Проверка столкновений
        #границы
        collision = False
        if self.snake_pos[0] < 0 or self.snake_pos[0] >= WIDTH or \
           self.snake_pos[1] < 0 or self.snake_pos[1] >= HEIGHT:
            collision = True
        #с самим собой
        for block in self.snake_body[1:]:
            if self.snake_pos == block:
                collision = True
                break
        
        #с препятствиями
        if self.snake_pos in self.obstacles:
            collision = True

        if collision:
            if self.shield_active:
                self.shield_active = False
                if len(self.snake_body) > 1:
                    self.snake_body.pop(0) # Убираем голову которая влетела в стену
                    self.snake_pos = list(self.snake_body[0]) # Откатываем позицию на предыдущий сегмент
                else:
                    self.game_over = True
            else:
                self.game_over = True

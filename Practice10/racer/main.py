import pygame
import random
import time

pygame.init()

WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

image_background = pygame.image.load('resources/AnimatedStreet.png')
image_player = pygame.image.load('resources/Player.png')
image_enemy = pygame.image.load('resources/Enemy.png')

pygame.mixer.music.load('resources/background.wav')
pygame.mixer.music.play(-1) #играет беск

sound_crash = pygame.mixer.Sound('resources/crash.wav')

font_big = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 25)

image_game_over = font_big.render("Game Over", True, "black")
image_game_over_rect = image_game_over.get_rect(center=(WIDTH // 2, HEIGHT // 2))

coins_count = 0


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_player
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT
        self.speed = 5

    def move(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)

        # Машина не выходит за экран
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_enemy
        self.rect = self.image.get_rect()
        self.speed = 10
        self.generate_random_rect()

    def generate_random_rect(self):
        self.rect.left = random.randint(0, WIDTH - self.rect.w)
        self.rect.bottom = 0

    def move(self):
        self.rect.move_ip(0, self.speed)

        if self.rect.top > HEIGHT:
            self.generate_random_rect()


class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Создаем монету как желтый кружок
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, "yellow", (15, 15), 15)

        self.rect = self.image.get_rect()
        self.speed = 5
        self.generate_random_rect()

    def generate_random_rect(self):
        self.rect.left = random.randint(0, WIDTH - self.rect.w)
        self.rect.bottom = random.randint(-600, -50)

    def move(self):
        self.rect.move_ip(0, self.speed)

        # Если монета ушла вниз, создаем новую сверху
        if self.rect.top > HEIGHT:
            self.generate_random_rect()


running = True
clock = pygame.time.Clock()
FPS = 60

player = Player()
enemy = Enemy()
coin = Coin()

all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
coin_sprites = pygame.sprite.Group()

all_sprites.add(player, enemy, coin)
enemy_sprites.add(enemy)
coin_sprites.add(coin)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.move()

    screen.blit(image_background, (0, 0))

    for entity in all_sprites:
        entity.move()
        screen.blit(entity.image, entity.rect)

    # Если игрок собрал монету
    if pygame.sprite.spritecollideany(player, coin_sprites):
        coins_count += 1
        coin.generate_random_rect()

    # Вывод количества монет справа сверху
    coins_text = font_small.render(f"Coins: {coins_count}", True, "black")
    screen.blit(coins_text, (WIDTH - 140, 10))

    # Если игрок столкнулся с врагом
    if pygame.sprite.spritecollideany(player, enemy_sprites):
        sound_crash.play()
        time.sleep(1)
        running = False

        screen.fill("red")
        screen.blit(image_game_over, image_game_over_rect)
        pygame.display.flip()
        time.sleep(3)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
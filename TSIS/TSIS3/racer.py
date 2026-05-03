"""
Логика игры Racer: машинки, монетки, враги, препятствия, бонусы и т.д.
"""
import pygame
import random
import sys

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
RED    = (255, 0, 0)
BLUE   = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
GREEN  = (0, 255, 0)
CYAN   = (0, 255, 255)
PURPLE = (128, 0, 128)
GRAY   = (100, 100, 100)

class Player(pygame.sprite.Sprite):
    def __init__(self, color_name):
        super().__init__()
        self.image_orig = pygame.image.load('assets/Player.png').convert_alpha()
        self.image = self.image_orig.copy()
        
        # Tinting the car based on settings
        tint_color = WHITE
        if color_name == "Red": tint_color = (255, 100, 100)
        elif color_name == "Blue": tint_color = (100, 100, 255)
        elif color_name == "Green": tint_color = (100, 255, 100)
        
        if tint_color != WHITE:
            tint_surface = pygame.Surface(self.image.get_size(), pygame.SRCALPHA)
            tint_surface.fill((*tint_color, 255))
            self.image.blit(tint_surface, (0,0), special_flags=pygame.BLEND_MULT)

        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)
        
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-5, 0)
        if pressed_keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.move_ip(5, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, speed_offset):
        super().__init__()
        self.image = pygame.image.load('assets/Enemy.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -100)
        self.speed_offset = speed_offset

    def move(self, base_speed):
        # Машины врагов (Enemy.png) обычно повернуты "лицом" вниз (встречный трафик).
        # Поэтому они должны ехать быстрее дороги, чтобы казалось, что они едут навстречу.
        enemy_speed = self.speed_offset + 3 
        screen_speed = base_speed + enemy_speed
            
        self.rect.move_ip(0, screen_speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.weight = random.choices([1, 2, 3], weights=[0.6, 0.3, 0.1])[0]
        radius = 15 if self.weight == 1 else 20 if self.weight == 2 else 25
        color = YELLOW if self.weight == 1 else ORANGE if self.weight == 2 else GREEN
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -50)

    def move(self, base_speed):
        self.rect.move_ip(0, base_speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # 0: Oil spill, 1: Barrier
        self.type = random.choice([0, 1])
        if self.type == 0:
            self.image = pygame.Surface((60, 40), pygame.SRCALPHA)
            pygame.draw.ellipse(self.image, BLACK, [0, 0, 60, 40])
        else:
            self.image = pygame.Surface((50, 20))
            self.image.fill((150, 50, 50))
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -50)

    def move(self, base_speed):
        self.rect.move_ip(0, base_speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.type = random.choice(["Nitro", "Shield", "Repair"])
        self.image = pygame.Surface((30, 30))
        
        font = pygame.font.SysFont("Verdana", 20, bold=True)
        if self.type == "Nitro": 
            self.image.fill(CYAN)
            text = font.render("N", True, BLACK)
        elif self.type == "Shield": 
            self.image.fill(PURPLE)
            text = font.render("S", True, WHITE)
        elif self.type == "Repair": 
            self.image.fill(WHITE)
            text = font.render("R", True, BLACK)
            
        text_rect = text.get_rect(center=(15, 15))
        self.image.blit(text, text_rect)
        
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -50)

    def move(self, base_speed):
        self.rect.move_ip(0, base_speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()

def run_game(screen, settings, username):
    clock = pygame.time.Clock()
    bg_image = pygame.image.load('assets/AnimatedStreet.png').convert()
    bg_y = 0
    
    font = pygame.font.SysFont("Verdana", 20)
    
    base_speed = 5
    if settings.get("difficulty") == "Hard": base_speed = 7
    elif settings.get("difficulty") == "Easy": base_speed = 3
    
    player = Player(settings.get("car_color", "Red"))
    
    enemies = pygame.sprite.Group()
    coins = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    powerups = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(player)
    
    SPAWN_ENEMY = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_ENEMY, max(500, int(2000 - base_speed*100)))
    SPAWN_COIN = pygame.USEREVENT + 2
    pygame.time.set_timer(SPAWN_COIN, 1500)
    SPAWN_OBST = pygame.USEREVENT + 3
    pygame.time.set_timer(SPAWN_OBST, 3000)
    SPAWN_PWR = pygame.USEREVENT + 4
    pygame.time.set_timer(SPAWN_PWR, 10000)
    
    score = 0
    coins_collected = 0
    distance = 0
    lives = 1
    
    active_powerup = None
    powerup_timer = 0
    
    running = True
    
    if settings.get("sound"):
        try:
            pygame.mixer.music.load('assets/background.wav')
            pygame.mixer.music.play(-1)
        except: pass
        try: crash_sound = pygame.mixer.Sound('assets/crash.wav')
        except: crash_sound = None
    else:
        crash_sound = None

    while running:
        dt = clock.tick(60)
        
        current_speed = base_speed
        if active_powerup == "Nitro":
            current_speed += 5
            powerup_timer -= dt
            if powerup_timer <= 0:
                active_powerup = None
        elif active_powerup == "Shield":
            pass # Persistent until hit
        
        distance += current_speed * (dt / 1000.0) * 10
        score = int(distance) + coins_collected * 10
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SPAWN_ENEMY:
                e = Enemy(random.randint(0, 2))
                while pygame.sprite.spritecollideany(e, all_sprites):
                    e.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -100)
                enemies.add(e)
                all_sprites.add(e)
            if event.type == SPAWN_COIN:
                c = Coin()
                while pygame.sprite.spritecollideany(c, all_sprites):
                    c.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -50)
                coins.add(c)
                all_sprites.add(c)
            if event.type == SPAWN_OBST:
                o = Obstacle()
                while pygame.sprite.spritecollideany(o, all_sprites):
                    o.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -50)
                obstacles.add(o)
                all_sprites.add(o)
            if event.type == SPAWN_PWR:
                p = PowerUp()
                while pygame.sprite.spritecollideany(p, all_sprites):
                    p.rect.center = (random.randint(40, SCREEN_WIDTH - 40), -50)
                powerups.add(p)
                all_sprites.add(p)

        # Scrolling Background
        bg_y += current_speed
        bg_y %= SCREEN_HEIGHT
        screen.blit(bg_image, (0, bg_y))
        screen.blit(bg_image, (0, bg_y - SCREEN_HEIGHT))

        player.move()
        for e in enemies: e.move(current_speed)
        for c in coins: c.move(current_speed)
        for o in obstacles: o.move(current_speed)
        for p in powerups: p.move(current_speed)

        all_sprites.draw(screen)
        
        # Shield visual
        if active_powerup == "Shield":
            pygame.draw.circle(screen, PURPLE, player.rect.center, 40, 3)
            
        # UI
        text_score = font.render(f"Score: {score}", True, BLACK)
        text_dist = font.render(f"Dist: {int(distance)}m / 10000m", True, BLACK)
        text_coins = font.render(f"Coins: {coins_collected}", True, BLACK)
        text_lives = font.render(f"Lives: {lives}", True, BLACK)
        screen.blit(text_score, (10, 10))
        screen.blit(text_dist, (10, 35))
        screen.blit(text_coins, (10, 60))
        screen.blit(text_lives, (10, 85))

        # Check Win Condition
        if distance >= 10000:
            running = False

        if active_powerup and active_powerup != "None":
            if active_powerup == "Nitro":
                p_text = font.render(f"Nitro: {max(0, powerup_timer//1000)}s", True, CYAN)
            elif active_powerup == "Shield":
                p_text = font.render(f"Shield Active", True, PURPLE)
            screen.blit(p_text, (SCREEN_WIDTH - 150, 10))

        # Collisions
        # PowerUps
        hit_pwr = pygame.sprite.spritecollideany(player, powerups)
        if hit_pwr:
            if hit_pwr.type == "Nitro":
                active_powerup = "Nitro"
                powerup_timer = 4000
            elif hit_pwr.type == "Shield":
                active_powerup = "Shield"
            elif hit_pwr.type == "Repair":
                lives += 1
                # Не сбрасываем active_powerup, так как Repair - мгновенный бонус (instant)
            hit_pwr.kill()

        # Coins
        hit_coins = pygame.sprite.spritecollide(player, coins, True)
        for c in hit_coins:
            coins_collected += c.weight
            if coins_collected % 20 == 0:  # Каждые 20 монет увеличиваем скорость
                base_speed += 1  # Только целые числа для идеальной плавности
                pygame.time.set_timer(SPAWN_ENEMY, max(400, int(2000 - base_speed*100)))

        # Obstacles and Enemies
        hit_obs = pygame.sprite.spritecollideany(player, obstacles)
        hit_enemy = pygame.sprite.spritecollideany(player, enemies)
        
        if hit_obs or hit_enemy:
            if hit_obs:
                hit_sprite = hit_obs
            else:
                hit_sprite = hit_enemy

            if active_powerup == "Shield":
                active_powerup = None
                hit_sprite.kill()
            else:
                lives -= 1
                if hit_obs and hit_obs.type == 0:
                    base_speed = max(2, base_speed - 2)
                hit_sprite.kill()
                if lives <= 0:
                    if settings.get("sound") and crash_sound:
                        pygame.mixer.music.stop()
                        crash_sound.play()
                    running = False

        pygame.display.flip()
        
    pygame.time.delay(1000)
    return score, distance, coins_collected

import pygame
import random
from config import *
from ui import draw_text

# ══════════════════════════════════════════
#  TRACK OBJECT CLASSES
# ══════════════════════════════════════════

class Enemy:
    def __init__(self, speed):
        # Randomly assign a lane and calculate center X position
        self.lane = random.randint(0, LANE_COUNT - 1)
        self.x = self.lane * LANE_WIDTH + LANE_WIDTH // 2
        self.y = -100
        # Give enemies slightly varied speeds for more dynamic gameplay
        self.speed = speed + random.randint(1, 3)

    def update(self):
        self.y += self.speed

    def draw(self, screen):
        # Render enemy (Red Car)
        x, y = self.x - 18, self.y - 28
        # Main body
        pygame.draw.rect(screen, RED, (x, y, 36, 56), border_radius=6)
        # Windshield
        pygame.draw.rect(screen, BLACK, (x + 5, y + 8, 26, 14), border_radius=3)

class Obstacle:
    def __init__(self, speed):
        # Choose a random hazard type
        self.type = random.choice(["oil", "barrier", "pothole"])
        self.lane = random.randint(0, LANE_COUNT - 1)
        self.x = self.lane * LANE_WIDTH + LANE_WIDTH // 2
        self.y = -100
        self.speed = speed

    def update(self):
        self.y += self.speed

    def draw(self, screen):
        if self.type == "oil":
            # Slippery oil slick
            pygame.draw.ellipse(screen, (30, 10, 50), (self.x - 25, self.y - 15, 50, 30))
        elif self.type == "barrier":
            # Road barrier with a white stripe
            pygame.draw.rect(screen, (255, 140, 0), (self.x - 35, self.y - 10, 70, 20), border_radius=4)
            pygame.draw.rect(screen, WHITE, (self.x - 35, self.y - 2, 70, 4))
        elif self.type == "pothole":
            # Simple black circle representing a hole
            pygame.draw.circle(screen, BLACK, (self.x, self.y), 20)

class PowerUp:
    def __init__(self, speed):
        self.type = random.choice(["nitro", "shield", "repair"])
        self.lane = random.randint(0, LANE_COUNT - 1)
        self.x = self.lane * LANE_WIDTH + LANE_WIDTH // 2
        self.y = -50
        self.speed = speed
        # Color coding based on effect type
        self.color = CYAN if self.type == "nitro" else (GREEN if self.type == "shield" else PURPLE)

    def update(self):
        self.y += self.speed

    def draw(self, screen):
        # Glowing orb appearance
        pygame.draw.circle(screen, self.color, (self.x, self.y), 15)
        pygame.draw.circle(screen, WHITE, (self.x, self.y), 15, 2)

class Coin:
    def __init__(self, speed):
        self.lane = random.randint(0, LANE_COUNT - 1)
        self.x = self.lane * LANE_WIDTH + LANE_WIDTH // 2
        self.y = -50
        self.speed = speed

    def update(self):
        self.y += self.speed

    def draw(self, screen):
        # Gold coin with a darker border
        pygame.draw.circle(screen, YELLOW, (self.x, self.y), 12)
        pygame.draw.circle(screen, (200, 150, 0), (self.x, self.y), 12, 2)

# ══════════════════════════════════════════
#  PLAYER CLASS
# ══════════════════════════════════════════

class Player:
    def __init__(self, color):
        self.lane = 1
        self.x = self.get_lane_x(self.lane)
        self.y = HEIGHT - 100
        self.color = color
        self.shield_active = False

    def get_lane_x(self, lane):
        """Calculates horizontal center of a specific lane."""
        return lane * LANE_WIDTH + LANE_WIDTH // 2

    def move(self, direction):
        """Updates lane based on player input."""
        if direction == "LEFT" and self.lane > 0: self.lane -= 1
        if direction == "RIGHT" and self.lane < LANE_COUNT - 1: self.lane += 1
        self.x = self.get_lane_x(self.lane)

    def draw(self, screen):
        # Draw Wheels
        for dx in [-22, 18]:
            for dy in [-25, 15]:
                pygame.draw.rect(screen, BLACK, (self.x + dx, self.y + dy, 6, 12))
        
        # Main Chassis
        pygame.draw.rect(screen, self.color, (self.x - 20, self.y - 30, 40, 60), border_radius=7)
        
        # Details: Windshield and Racing Stripes
        pygame.draw.rect(screen, (150, 220, 255), (self.x - 15, self.y - 20, 30, 14), border_radius=3)
        pygame.draw.line(screen, WHITE, (self.x - 7, self.y + 5), (self.x - 7, self.y + 25), 2)
        pygame.draw.line(screen, WHITE, (self.x + 7, self.y + 5), (self.x + 7, self.y + 25), 2)
        
        # Front Headlights
        pygame.draw.circle(screen, YELLOW, (self.x - 12, self.y - 28), 4)
        pygame.draw.circle(screen, YELLOW, (self.x + 12, self.y - 28), 4)
        
        # Visual Shield Effect
        if self.shield_active:
            pygame.draw.circle(screen, GREEN, (self.x, self.y), 45, 3)

# ══════════════════════════════════════════
#  MAIN RACING FUNCTION
# ══════════════════════════════════════════

def run_game(screen, clock, settings, username):
    player = Player(settings['car_color'])
    # Object pools
    enemies, obstacles, powerups, coins = [], [], [], []
    
    distance, total_coins = 0, 0
    game_speed = BASE_SPEED
    active_effect = None
    effect_timer = 0
    
    font = pygame.font.SysFont("Consolas", 20, bold=True)
    running = True

    while running:
        screen.fill(ROAD_COLOR)
        
        # Power-up Timer Logic
        if effect_timer > 0:
            effect_timer -= 1
        else:
            active_effect = None
            player.shield_active = False

        # Increase speed if Nitro is active
        current_speed = game_speed * 1.7 if active_effect == "nitro" else game_speed

        # Render road lane dividers
        for i in range(1, LANE_COUNT):
            pygame.draw.line(screen, GRAY, (i * LANE_WIDTH, 0), (i * LANE_WIDTH, HEIGHT), 1)

        # Input Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return {"score": 0, "distance": 0, "coins": 0}
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: player.move("LEFT")
                if event.key == pygame.K_RIGHT: player.move("RIGHT")

        # Dynamic Spawning (Difficulty scales with distance)
        spawn_rate = max(15, 60 - int(distance // 400))
        if random.randint(1, spawn_rate) == 1:
            enemies.append(Enemy(current_speed))
        if random.randint(1, 120) == 1:
            obstacles.append(Obstacle(current_speed))
        if random.randint(1, 400) == 1:
            powerups.append(PowerUp(current_speed))
        if random.randint(1, 80) == 1:
            coins.append(Coin(current_speed))

        # --- Collision and Update Handling ---
        player_rect = pygame.Rect(player.x - 18, player.y - 28, 36, 56)

        # 1. Enemies
        for e in enemies[:]:
            e.update(); e.draw(screen)
            if player_rect.colliderect(pygame.Rect(e.x-18, e.y-28, 36, 56)):
                if player.shield_active:
                    player.shield_active = False
                    active_effect = None
                    enemies.remove(e)
                else: running = False # Game Over
            elif e.y > HEIGHT: enemies.remove(e)

        # 2. Obstacles
        for ob in obstacles[:]:
            ob.update(); ob.draw(screen)
            if player_rect.colliderect(pygame.Rect(ob.x-20, ob.y-10, 40, 20)):
                if ob.type in ["barrier", "pothole"]:
                    if player.shield_active: 
                        player.shield_active = False; obstacles.remove(ob)
                    else: running = False # Game Over
                elif ob.type == "oil": active_effect = None # Oil slick cancels Nitro
            elif ob.y > HEIGHT: obstacles.remove(ob)

        # 3. Power-ups
        for p in powerups[:]:
            p.update(); p.draw(screen)
            if player_rect.colliderect(pygame.Rect(p.x-15, p.y-15, 30, 30)):
                active_effect = p.type
                if p.type == "nitro": effect_timer = 180
                elif p.type == "shield": player.shield_active = True; effect_timer = 600
                elif p.type == "repair": enemies.clear(); active_effect = None # Clears screen
                powerups.remove(p)
            elif p.y > HEIGHT: powerups.remove(p)

        # 4. Coins
        for c in coins[:]:
            c.update(); c.draw(screen)
            if player_rect.collidepoint(c.x, c.y):
                total_coins += 1; coins.remove(c)
            elif c.y > HEIGHT: coins.remove(c)

        # Update Game Stats
        distance += current_speed / 20
        # Gradually increase game speed over time
        game_speed = min(MAX_SPEED, BASE_SPEED + (distance // 500))
        
        # Calculate final score (distance + coin bonus)
        score = int(distance + (total_coins * 100))
        
        # Display HUD (Heads-Up Display)
        draw_text(screen, font, f"SCORE: {score}", WHITE, 10, 15, center=False)
        draw_text(screen, font, f"COINS: {total_coins}", YELLOW, 10, 40, center=False)
        if active_effect:
            draw_text(screen, font, f"BOOST: {active_effect.upper()}", CYAN, WIDTH-150, 15, center=False)

        player.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    # Return results for leaderboard processing
    return {"score": score, "distance": int(distance), "coins": total_coins}
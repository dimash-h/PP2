import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Setup Screen and Framerate
FPS = 60
FramePerSec = pygame.time.Clock()

# Colors
WHITE  = (255, 255, 255)
BLACK  = (0, 0, 0)
RED    = (255, 0, 0)
BLUE   = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY   = (50, 50, 50)

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Create display surface
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")

# Fonts
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Game Variables
SPEED = 5
SCORE = 0       # Internal score based on avoided cars
COIN_SCORE = 0  # Collected coins

class Enemy(pygame.sprite.Sprite):
    """Enemy car class dropping from the top."""
    def __init__(self):
        super().__init__() 
        self.image = pygame.Surface((40, 60))
        self.image.fill(RED) # Represent enemy with red rectangle
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        # Reset enemy at top if it goes off screen
        if self.rect.bottom > SCREEN_HEIGHT + 60:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

class Player(pygame.sprite.Sprite):
    """Player car controlled by left and right arrow keys."""
    def __init__(self):
        super().__init__() 
        self.image = pygame.Surface((40, 60))
        self.image.fill(BLUE) # Represent player with blue rectangle
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 80)
        
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT]:
            if self.rect.left > 0:
                self.rect.move_ip(-5, 0)
        if pressed_keys[pygame.K_RIGHT]:
            if self.rect.right < SCREEN_WIDTH:
                self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    """Coin that randomly appears and moves down."""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(self.image, YELLOW, (15, 15), 15)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        
    def move(self):
        self.rect.move_ip(0, SPEED)
        # Respawn coin if it goes off screen
        if self.rect.bottom > SCREEN_HEIGHT + 30:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Instantiate objects
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Sprite Groups for collision detection and drawing
enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
all_sprites.add(C1)

# Custom Event to slowly increase game speed
INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

def main():
    global SPEED, COIN_SCORE
    
    while True:
        # Event Loop
        for event in pygame.event.get():
            if event.type == INC_SPEED:
                SPEED += 0.5
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Draw Background
        DISPLAYSURF.fill(GRAY)

        # Draw Coins Score at top right
        coin_text = font_small.render(f"Coins: {COIN_SCORE}", True, WHITE)
        DISPLAYSURF.blit(coin_text, (SCREEN_WIDTH - coin_text.get_width() - 10, 10))

        # Move and Draw all Sprites
        for entity in all_sprites:
            entity.move()
            DISPLAYSURF.blit(entity.image, entity.rect)

        # Check collision between Player and Coins
        # Returns a list of coins the player collided with
        collected_coins = pygame.sprite.spritecollide(P1, coins, False)
        for coin in collected_coins:
            COIN_SCORE += 1
            # Respawn the collected coin
            coin.rect.top = 0
            coin.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

        # Check collision between Player and Enemies
        if pygame.sprite.spritecollideany(P1, enemies):
            # Fill screen red and show Game Over
            DISPLAYSURF.fill(RED)
            DISPLAYSURF.blit(game_over, (30, 250))
            pygame.display.update()
            
            # Remove all sprites and stop
            for entity in all_sprites:
                entity.kill() 
            
            pygame.time.delay(2000)
            pygame.quit()
            sys.exit()

        # Update Display and tick framerate
        pygame.display.update()
        FramePerSec.tick(FPS)

if __name__ == "__main__":
    main()

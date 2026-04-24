import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
WIDTH = 600
HEIGHT = 400
BLOCK_SIZE = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)  # Snake color
RED   = (255, 0, 0)  # Food weight 1
YELLOW= (255, 255, 0) # Food weight 2
BLUE  = (0, 0, 255)  # Food weight 3

FOOD_TIMER_MS = 5000 # Food disappears after 5 seconds

# Setup Display
DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

# Fonts
font = pygame.font.SysFont("Verdana", 20)
font_large = pygame.font.SysFont("Verdana", 50)

def generate_food(snake_body):
    """
    Generates a random position and weight for the food.
    Ensures that the food does not spawn inside the wall or on the snake's body.
    Returns a dictionary with position, weight, and spawn time.
    """
    while True:
        # Generate random coordinates aligned with the grid
        food_x = random.randrange(0, WIDTH, BLOCK_SIZE)
        food_y = random.randrange(0, HEIGHT, BLOCK_SIZE)
        
        # Check if the food is on the snake's body
        if [food_x, food_y] not in snake_body:
            weight = random.choice([1, 2, 3])
            return {
                'pos': [food_x, food_y],
                'weight': weight,
                'time': pygame.time.get_ticks()
            }

def game_over_screen(score, level):
    """Displays the Game Over screen with final score and level."""
    DISPLAYSURF.fill(BLACK)
    
    # Render texts
    go_text = font_large.render("Game Over!", True, RED)
    score_text = font.render(f"Final Score: {score} | Final Level: {level}", True, WHITE)
    
    # Center texts
    go_rect = go_text.get_rect(center=(WIDTH/2, HEIGHT/2 - 20))
    score_rect = score_text.get_rect(center=(WIDTH/2, HEIGHT/2 + 30))
    
    DISPLAYSURF.blit(go_text, go_rect)
    DISPLAYSURF.blit(score_text, score_rect)
    
    pygame.display.update()
    pygame.time.delay(3000)
    pygame.quit()
    sys.exit()

def main():
    # Initial Snake position and body
    snake_pos = [100, 60]
    snake_body = [[100, 60], [80, 60], [60, 60]]
    
    # Generate initial food
    food = generate_food(snake_body)
    food_spawn = True
    
    # Movement variables
    direction = 'RIGHT'
    change_to = direction
    
    # Game state variables
    score = 0
    level = 1
    speed = 10 # Initial frames per second (speed)
    
    clock = pygame.time.Clock()

    while True:
        # 1. Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Handle key presses to change direction
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'

        # Prevent snake from reversing its direction
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        # 2. Move Snake
        if direction == 'UP':
            snake_pos[1] -= BLOCK_SIZE
        if direction == 'DOWN':
            snake_pos[1] += BLOCK_SIZE
        if direction == 'LEFT':
            snake_pos[0] -= BLOCK_SIZE
        if direction == 'RIGHT':
            snake_pos[0] += BLOCK_SIZE

        # 3. Snake body growing mechanism
        snake_body.insert(0, list(snake_pos))
        
        # Check if food is eaten
        if snake_pos[0] == food['pos'][0] and snake_pos[1] == food['pos'][1]:
            score += food['weight']
            # Increase level every 4 score points collected
            new_level = 1 + (score // 4)
            if new_level > level:
                speed += 2 * (new_level - level) # Increase speed dynamically
                level = new_level
            food_spawn = False
        else:
            # If food is not eaten, remove the tail segment
            snake_body.pop()

        # Check if food timer has expired
        current_time = pygame.time.get_ticks()
        if current_time - food['time'] > FOOD_TIMER_MS:
            food_spawn = False # Force respawn

        # Generate new food if needed
        if not food_spawn:
            food = generate_food(snake_body)
        food_spawn = True

        # 4. Check Collisions (Game Over logic)
        # Border (wall) collision check
        if snake_pos[0] < 0 or snake_pos[0] > WIDTH - BLOCK_SIZE:
            game_over_screen(score, level)
        if snake_pos[1] < 0 or snake_pos[1] > HEIGHT - BLOCK_SIZE:
            game_over_screen(score, level)

        # Self collision check
        for block in snake_body[1:]:
            if snake_pos[0] == block[0] and snake_pos[1] == block[1]:
                game_over_screen(score, level)

        # 5. Drawing phase
        DISPLAYSURF.fill(BLACK) # Clear screen

        # Draw Snake
        for pos in snake_body:
            pygame.draw.rect(DISPLAYSURF, GREEN, pygame.Rect(pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
            
        # Draw Food based on its weight
        food_color = {1: RED, 2: YELLOW, 3: BLUE}[food['weight']]
        pygame.draw.rect(DISPLAYSURF, food_color, pygame.Rect(food['pos'][0], food['pos'][1], BLOCK_SIZE, BLOCK_SIZE))

        # Show Score and Level in top-left
        score_text = font.render(f"Score: {score}  |  Level: {level}", True, WHITE)
        DISPLAYSURF.blit(score_text, (10, 10))

        # Refresh display and tick clock
        pygame.display.update()
        clock.tick(speed)

if __name__ == "__main__":
    main()

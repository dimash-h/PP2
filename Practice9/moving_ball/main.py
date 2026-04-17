import pygame
from ball import Ball

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")


my_ball = Ball(WIDTH // 2, HEIGHT // 2, 25, (255, 0, 0))
clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                my_ball.move_up()
            elif event.key == pygame.K_DOWN:
                my_ball.move_down(HEIGHT)
            elif event.key == pygame.K_LEFT:
                my_ball.move_left()
            elif event.key == pygame.K_RIGHT:
                my_ball.move_right(WIDTH)

    screen.fill((255, 255, 255)) 
    my_ball.draw(screen)
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
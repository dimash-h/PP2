import pygame
from clock import get_angles

pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey's Clock")


bg = pygame.image.load("images/mickeyclock.jpeg")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))


min_hand_image = pygame.image.load("images/right_hand.png")
sec_hand_image = pygame.image.load("images/left_hand.png")

# 
min_hand_image = pygame.transform.scale(min_hand_image, (500, 950))
sec_hand_image = pygame.transform.scale(sec_hand_image, (500, 900))

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

   
    min_angle, sec_angle = get_angles()

    
    screen.blit(bg, (0, 0))

   
    min_hand = pygame.transform.rotate(min_hand_image, min_angle)
    min_rect = min_hand.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(min_hand, min_rect)

   
    sec_hand = pygame.transform.rotate(sec_hand_image, sec_angle)
    sec_rect = sec_hand.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(sec_hand, sec_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
import pygame
from player import Player

pygame.init()
screen = pygame.display.set_mode((500, 300))
pygame.display.set_caption("Music Player")
font = pygame.font.SysFont(None, 30)

music_player = Player()

running = True
while running:
    screen.fill((50, 50, 50))
    
   
    text_track = font.render(f"Track: {music_player.get_name()}", True, (255, 255, 0))
    text_keys = font.render("P:Play | S:Stop | N:Next | B:Prev | Q:Quit", True, (255, 255, 255))
    
    screen.blit(text_track, (20, 100))
    screen.blit(text_keys, (20, 150))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p: music_player.play()
            elif event.key == pygame.K_s: music_player.stop()
            elif event.key == pygame.K_n: music_player.next()
            elif event.key == pygame.K_b: music_player.prev()
            elif event.key == pygame.K_q: running = False

    pygame.display.flip()

pygame.quit()
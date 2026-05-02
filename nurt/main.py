import pygame
import sys
import os

# Import game constants and configurations
from config import *
from config import MUSIC_PATH
from ui import draw_bg, draw_text, draw_button, is_hovered
from racer import run_game
from persistence import (load_settings, save_settings, 
                         load_leaderboard, add_record)

# ══════════════════════════════════════════
#  MUSIC MANAGEMENT
# ══════════════════════════════════════════
def manage_music(sound_on):
    """Handles starting, stopping, and loading background music."""
    if sound_on:
        # Only start if music isn't already playing
        if not pygame.mixer.music.get_busy():
            if os.path.exists(MUSIC_PATH):
                try:
                    pygame.mixer.music.load(MUSIC_PATH)
                    pygame.mixer.music.play(-1)  # -1 loops indefinitely
                    pygame.mixer.music.set_volume(0.5)
                    print("--- Music started successfully! ---")
                except Exception as e:
                    print(f"Playback error: {e}")
            else:
                # If file is missing, print the full path to help debugging
                print(f"ERROR: File not found at: {MUSIC_PATH}")
    else:
        pygame.mixer.music.stop()

# ══════════════════════════════════════════
#  1. SCREEN: NAME ENTRY
# ══════════════════════════════════════════
def screen_enter_name(screen, clock, font_big, font):
    """Displays a screen for the player to type their username."""
    name = ""
    while True:
        draw_bg(screen)
        draw_text(screen, font_big, "ENTER YOUR NAME", CYAN, WIDTH//2, 200)
        draw_text(screen, font, name + "_", YELLOW, WIDTH//2, 280)
        draw_text(screen, font, "Press ENTER to Start", LGRAY, WIDTH//2, 400)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name.strip():
                    return name.strip()
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                else:
                    # Limit name length to 12 characters
                    if len(name) < 12:
                        name += event.unicode
        
        pygame.display.flip()
        clock.tick(30)

# ══════════════════════════════════════════
#  2. SCREEN: MAIN MENU
# ══════════════════════════════════════════
def screen_menu(screen, clock, font_big, font, name):
    """Main navigation hub for the game."""
    while True:
        draw_bg(screen)
        mouse = pygame.mouse.get_pos()
        draw_text(screen, font_big, f"HELLO, {name.upper()}!", WHITE, WIDTH//2, 100)
        
        # Define button hitboxes
        btn_play = pygame.Rect(WIDTH//2 - 110, 200, 220, 50)
        btn_sett = pygame.Rect(WIDTH//2 - 110, 270, 220, 50) 
        btn_lead = pygame.Rect(WIDTH//2 - 110, 340, 220, 50)
        btn_exit = pygame.Rect(WIDTH//2 - 110, 410, 220, 50)

        # Render buttons with hover effects
        draw_button(screen, font, "START RACE", btn_play, is_hovered(btn_play, mouse))
        draw_button(screen, font, "SETTINGS", btn_sett, is_hovered(btn_sett, mouse))
        draw_button(screen, font, "LEADERBOARD", btn_lead, is_hovered(btn_lead, mouse))
        draw_button(screen, font, "QUIT", btn_exit, is_hovered(btn_exit, mouse))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_hovered(btn_play, mouse): return "play"
                if is_hovered(btn_sett, mouse): return "settings"
                if is_hovered(btn_lead, mouse): return "leaderboard"
                if is_hovered(btn_exit, mouse): return "quit"
        
        pygame.display.flip()
        clock.tick(30)

# ══════════════════════════════════════════
#  3. SCREEN: SETTINGS
# ══════════════════════════════════════════
def screen_settings(screen, clock, font_big, font, settings):
    """Allows players to toggle sound on/off."""
    while True:
        draw_bg(screen)
        mouse = pygame.mouse.get_pos()
        draw_text(screen, font_big, "SETTINGS", CYAN, WIDTH//2, 100)
        
        # Determine sound status display
        sound_status = "ON" if settings['sound'] else "OFF"
        
        btn_sound = pygame.Rect(WIDTH//2 - 110, 250, 220, 50)
        btn_back = pygame.Rect(WIDTH//2 - 110, 350, 220, 50)

        draw_button(screen, font, f"SOUND: {sound_status}", btn_sound, is_hovered(btn_sound, mouse))
        draw_button(screen, font, "BACK", btn_back, is_hovered(btn_back, mouse))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_hovered(btn_sound, mouse):
                    # Toggle sound setting
                    settings['sound'] = not settings['sound']
                    # Save preference to settings.json
                    save_settings(settings) 
                    # Update audio engine state
                    manage_music(settings['sound']) 
                if is_hovered(btn_back, mouse):
                    return

        pygame.display.flip()
        clock.tick(30)

# ══════════════════════════════════════════
#  4. SCREEN: LEADERBOARD
# ══════════════════════════════════════════
def screen_leaderboard(screen, clock, font_big, font):
    """Loads and displays the top scores."""
    records = load_leaderboard()
    while True:
        draw_bg(screen)
        draw_text(screen, font_big, "TOP 10 RACERS", CYAN, WIDTH//2, 60)
        # Format table header
        header = "{:<3} {:<12} {:<8}".format("#", "NAME", "SCORE")
        draw_text(screen, font, header, YELLOW, WIDTH//2, 120)

        # Display up to 10 rows of data
        for i, rec in enumerate(records[:10]):
            y_pos = 170 + (i * 35)
            row = "{:<3} {:<12} {:<8}".format(i + 1, rec['name'][:10], rec['score'])
            draw_text(screen, font, row, WHITE, WIDTH//2, y_pos)

        btn_back = pygame.Rect(WIDTH//2 - 70, HEIGHT - 70, 140, 40)
        mouse = pygame.mouse.get_pos()
        draw_button(screen, font, "BACK", btn_back, is_hovered(btn_back, mouse))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_hovered(btn_back, mouse): return
        
        pygame.display.flip()
        clock.tick(30)

# ══════════════════════════════════════════
#  5. SCREEN: GAME OVER
# ══════════════════════════════════════════
def screen_game_over(screen, clock, font_big, font, results):
    """Shows results after a crash and offers return to menu."""
    while True:
        draw_bg(screen)
        draw_text(screen, font_big, "GAME OVER", RED, WIDTH//2, 150)
        draw_text(screen, font, f"Your Score: {results['score']}", WHITE, WIDTH//2, 220)
        draw_text(screen, font, f"Distance: {results['distance']}m", LGRAY, WIDTH//2, 260)
        
        btn_restart = pygame.Rect(WIDTH//2 - 100, 350, 200, 50)
        mouse = pygame.mouse.get_pos()
        draw_button(screen, font, "MAIN MENU", btn_restart, is_hovered(btn_restart, mouse))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if is_hovered(btn_restart, mouse): return

        pygame.display.flip()
        clock.tick(30)

# ══════════════════════════════════════════
#  6. MAIN LOOP (APPLICATION CONTROLLER)
# ══════════════════════════════════════════
def main():
    pygame.init()
    pygame.mixer.init() # Initialize sound engine
    
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Racer TSIS 3/4")
    clock = pygame.time.Clock()
    
    # Initialize fonts
    font_big = pygame.font.SysFont("Arial", 42, bold=True)
    font = pygame.font.SysFont("Courier New", 22, bold=True)

    # Load persistent settings and start music if applicable
    settings = load_settings()
    manage_music(settings['sound'])
    
    # First step: Get user's name
    username = screen_enter_name(screen, clock, font_big, font)

    running = True
    while running:
        # Show menu and wait for user selection
        choice = screen_menu(screen, clock, font_big, font, username)

        if choice == "quit":
            running = False
        elif choice == "settings":
            screen_settings(screen, clock, font_big, font, settings)
        elif choice == "leaderboard":
            screen_leaderboard(screen, clock, font_big, font)
        elif choice == "play":
            # Launch actual gameplay
            game_results = run_game(screen, clock, settings, username)
            # Save the score to the leaderboard
            add_record(username, game_results['score'], game_results['distance'], game_results['coins'])
            # Show game over stats
            screen_game_over(screen, clock, font_big, font, game_results)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
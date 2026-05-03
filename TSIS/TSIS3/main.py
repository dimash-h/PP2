"""
TSIS 3: Главный файл для запуска игры Racer.
Управляет состоянием игры и переключением экранов.
"""
import pygame
import sys
import persistence
import ui
import racer

def main():
    pygame.init()
    screen = pygame.display.set_mode(
        (racer.SCREEN_WIDTH, racer.SCREEN_HEIGHT), 
        pygame.DOUBLEBUF, 
        vsync=1
    )
    pygame.display.set_caption("Racer Game")
    clock = pygame.time.Clock()

    settings = persistence.load_settings()
    
    state = "MENU"
    username = ""
    last_score, last_distance, last_coins = 0, 0, 0
    
    # UI Elements
    btn_play = ui.Button(100, 200, 200, 50, "Play")
    btn_leaderboard = ui.Button(100, 270, 200, 50, "Leaderboard")
    btn_settings = ui.Button(100, 340, 200, 50, "Settings")
    btn_quit = ui.Button(100, 410, 200, 50, "Quit")

    input_user = ui.TextInput(100, 250, 200, 40, "")
    btn_start = ui.Button(100, 320, 200, 50, "Start")
    btn_back_user = ui.Button(100, 390, 200, 50, "Back")

    btn_retry = ui.Button(100, 400, 200, 50, "Retry")
    btn_menu_go = ui.Button(100, 470, 200, 50, "Main Menu")

    btn_back_ld = ui.Button(100, 500, 200, 50, "Back")
    
    btn_snd = ui.Button(200, 150, 150, 40, f"Sound: {'On' if settings.get('sound') else 'Off'}")
    btn_color = ui.Button(200, 220, 150, 40, f"Color: {settings.get('car_color')}")
    btn_diff = ui.Button(200, 290, 150, 40, f"Diff: {settings.get('difficulty')}")
    btn_back_set = ui.Button(100, 500, 200, 50, "Back")

    while True:
        screen.fill(ui.WHITE)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if state == "MENU":
                if btn_play.handle_event(event): state = "USERNAME"
                if btn_leaderboard.handle_event(event): state = "LEADERBOARD"
                if btn_settings.handle_event(event): state = "SETTINGS"
                if btn_quit.handle_event(event):
                    pygame.quit()
                    sys.exit()
                    
            elif state == "USERNAME":
                if input_user.handle_event(event): 
                    pass
                if btn_start.handle_event(event) and len(input_user.text) > 0:
                    username = input_user.text
                    state = "PLAY"
                if btn_back_user.handle_event(event):
                    state = "MENU"
                    
            elif state == "SETTINGS":
                if btn_snd.handle_event(event):
                    settings["sound"] = not settings["sound"]
                    btn_snd.text = f"Sound: {'On' if settings['sound'] else 'Off'}"
                if btn_color.handle_event(event):
                    colors = ["Red", "Blue", "Green"]
                    idx = (colors.index(settings.get("car_color", "Red")) + 1) % len(colors)
                    settings["car_color"] = colors[idx]
                    btn_color.text = f"Color: {settings['car_color']}"
                if btn_diff.handle_event(event):
                    diffs = ["Easy", "Normal", "Hard"]
                    idx = (diffs.index(settings.get("difficulty", "Normal")) + 1) % len(diffs)
                    settings["difficulty"] = diffs[idx]
                    btn_diff.text = f"Diff: {settings['difficulty']}"
                if btn_back_set.handle_event(event):
                    persistence.save_settings(settings)
                    state = "MENU"
                    
            elif state == "GAME_OVER":
                if btn_retry.handle_event(event): state = "PLAY"
                if btn_menu_go.handle_event(event): state = "MENU"
                
            elif state == "LEADERBOARD":
                if btn_back_ld.handle_event(event): state = "MENU"

        if state == "MENU":
            ui.draw_text(screen, "MAIN MENU", 200, 100, center=True)
            btn_play.draw(screen)
            btn_leaderboard.draw(screen)
            btn_settings.draw(screen)
            btn_quit.draw(screen)
            
        elif state == "USERNAME":
            ui.draw_text(screen, "ENTER NAME:", 200, 180, center=True)
            input_user.draw(screen)
            btn_start.draw(screen)
            btn_back_user.draw(screen)

        elif state == "PLAY":
            last_score, last_distance, last_coins = racer.run_game(screen, settings, username)
            persistence.add_score(username, last_score, int(last_distance))
            state = "GAME_OVER"

        elif state == "GAME_OVER":
            ui.draw_text(screen, "GAME OVER", 200, 100, center=True)
            ui.draw_text(screen, f"Score: {last_score}", 200, 200, font=ui.SMALL_FONT, center=True)
            ui.draw_text(screen, f"Distance: {int(last_distance)}m", 200, 250, font=ui.SMALL_FONT, center=True)
            ui.draw_text(screen, f"Coins: {last_coins}", 200, 300, font=ui.SMALL_FONT, center=True)
            btn_retry.draw(screen)
            btn_menu_go.draw(screen)

        elif state == "SETTINGS":
            ui.draw_text(screen, "SETTINGS", 200, 80, center=True)
            ui.draw_text(screen, "Audio:", 50, 150, font=ui.SMALL_FONT)
            btn_snd.draw(screen)
            ui.draw_text(screen, "Car Color:", 50, 220, font=ui.SMALL_FONT)
            btn_color.draw(screen)
            ui.draw_text(screen, "Difficulty:", 50, 290, font=ui.SMALL_FONT)
            btn_diff.draw(screen)
            btn_back_set.draw(screen)

        elif state == "LEADERBOARD":
            ui.draw_text(screen, "LEADERBOARD", 200, 50, center=True)
            board = persistence.load_leaderboard()
            y = 120
            for i, entry in enumerate(board[:10]):
                name = entry.get("name", "Unknown")
                score = entry.get("score", 0)
                dist = entry.get("distance", 0)
                txt = f"{i+1}. {name} - {score} pts ({dist}m)"
                ui.draw_text(screen, txt, 50, y, font=ui.SMALL_FONT)
                y += 35
            btn_back_ld.draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()

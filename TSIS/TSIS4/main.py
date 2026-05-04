import pygame
import sys
from game import GameState, WIDTH, HEIGHT, BLOCK_SIZE
from config import load_settings, save_settings
from db import init_db, save_score, get_top_10, get_personal_best
#Главный файл — окно, меню, отрисовка, игровой цикл

pygame.init()
pygame.mixer.init()
try:
    pygame.mixer.music.load("assets/background.wav")
    pygame.mixer.music.set_volume(0.3)
except:
    pass

DISPLAYSURF = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Advanced Snake")
font = pygame.font.SysFont("Verdana", 20)
font_large = pygame.font.SysFont("Verdana", 40)
font_small = pygame.font.SysFont("Verdana", 14, bold=True)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_RED = (150, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
ORANGE = (255, 165, 0)

settings = load_settings()

def draw_text(text, fnt, color, surface, x, y, center=False):
    """
    Универсальная функция для отрисовки текста на экране
    """
    textobj = fnt.render(text, True, color)
    textrect = textobj.get_rect()
    if center:
        textrect.center = (x, y)
    else:
        textrect.topleft = (x, y)
    surface.blit(textobj, textrect)
    return textrect

mouse_was_down = False # Чтобы кнопка не нажималась несколько раз при зажатой мышке

def button(text, x, y, w, h, inactive_color, active_color, action=None):
    """
    Отрисовка и обработка кнопок. Возвращает True, если на кнопку нажали
    """
    global mouse_was_down
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    if click[0] == 0:
        mouse_was_down = False
        
    clicked = False
    if x + w > mouse[0] > x and y + h > mouse[1] > y: # Мышь внутри кнопки
        pygame.draw.rect(DISPLAYSURF, active_color, (x, y, w, h)) # Подсвечиваем кнопку
        if click[0] == 1 and not mouse_was_down:
            mouse_was_down = True
            clicked = True
    else:
        pygame.draw.rect(DISPLAYSURF, inactive_color, (x, y, w, h))
        
    draw_text(text, font, BLACK, DISPLAYSURF, x + w/2, y + h/2, center=True)
    return clicked

def get_text_input(prompt, x, y):
    """
    Окно для ввода текста.
    """
    input_text = ""
    active = True
    while active:
        DISPLAYSURF.fill(BLACK)
        draw_text(prompt, font_large, WHITE, DISPLAYSURF, WIDTH//2, HEIGHT//2 - 50, center=True)
        draw_text(input_text, font, YELLOW, DISPLAYSURF, WIDTH//2, HEIGHT//2, center=True)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return input_text
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if len(input_text) < 20:
                        input_text += event.unicode

def main_menu():
    """
    Главное меню игры.
    """
    global settings
    username = ""
    while True:
        DISPLAYSURF.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        draw_text("Snake Game", font_large, GREEN, DISPLAYSURF, WIDTH//2, 80, center=True)
        
        if username: # Показываем имя игрока
            draw_text(f"Player: {username}", font, WHITE, DISPLAYSURF, WIDTH//2, 130, center=True)
        
        if button("Play", 200, 160, 200, 40, GRAY, WHITE):
            if not username: # Если имя не введено, запрашиваем
                username = get_text_input("Enter Username:", WIDTH//2, HEIGHT//2)
            if username:
                pb = get_personal_best(username)
                game_loop(username, pb)
        if button("Leaderboard", 200, 220, 200, 40, GRAY, WHITE):
            leaderboard_screen()
        if button("Settings", 200, 280, 200, 40, GRAY, WHITE):
            settings_screen()
        if button("Quit", 200, 340, 200, 40, GRAY, WHITE):
            pygame.quit()
            sys.exit()
            
        pygame.display.update()

def leaderboard_screen():
    """
    Экран таблицы лидеров
    """
    top10 = get_top_10()
    while True:
        DISPLAYSURF.fill(BLACK)
        draw_text("Top 10 Leaderboard", font_large, YELLOW, DISPLAYSURF, WIDTH//2, 40, center=True)
        
        y = 100
        for i, row in enumerate(top10):
            # row = (username, score, level, played_at)
            text = f"{i+1}. {row[0][:10]} - Score: {row[1]} (Lvl {row[2]})" #обрезаем имя до 10 символов
            draw_text(text, font, WHITE, DISPLAYSURF, WIDTH//2, y, center=True)
            y += 25
            
        if button("Back", 200, 350, 200, 40, GRAY, WHITE):
            return
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        pygame.display.update()

def settings_screen():
    """
    Экран настроек: включение сетки, звука, выбор цвета змейки.
    """
    global settings
    colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0)]
    color_names = ["Green", "Red", "Blue", "Yellow"]
    
    while True:
        DISPLAYSURF.fill(BLACK)
        draw_text("Settings", font_large, WHITE, DISPLAYSURF, WIDTH//2, 50, center=True)
        
        grid_status = "ON" if settings["grid"] else "OFF"
        if button(f"Grid Overlay: {grid_status}", 150, 120, 300, 40, GRAY, WHITE):
            settings["grid"] = not settings["grid"]
            
        sound_status = "ON" if settings["sound"] else "OFF"
        if button(f"Sound: {sound_status}", 150, 180, 300, 40, GRAY, WHITE):
            settings["sound"] = not settings["sound"]
            
        # Выбор цвета змейки
        draw_text("Snake Color:", font, WHITE, DISPLAYSURF, WIDTH//2, 250, center=True)
        c_idx = 0
        try:
            c_idx = colors.index(tuple(settings["snake_color"]))
        except ValueError:
            pass
            
        if button(f"Color: {color_names[c_idx]}", 150, 280, 300, 40, GRAY, WHITE):
            c_idx = (c_idx + 1) % len(colors) # Следующий цвет по кругу
            settings["snake_color"] = list(colors[c_idx])
            
        if button("Save & Back", 200, 350, 200, 40, GRAY, WHITE):
            save_settings(settings)
            return
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        pygame.display.update()

def game_over_screen(username, score, level, pb):
    """
    Экран конца игры. Показывает финальный счет, уровень и личный рекорд.
    Сохраняет результат в базу данных.
    """
    save_score(username, score, level)
    pygame.mixer.music.stop()
    
    while True:
        DISPLAYSURF.fill(BLACK)
        draw_text("GAME OVER", font_large, RED, DISPLAYSURF, WIDTH//2, 80, center=True)
        draw_text(f"Final Score: {score}", font, WHITE, DISPLAYSURF, WIDTH//2, 140, center=True)
        draw_text(f"Level Reached: {level}", font, WHITE, DISPLAYSURF, WIDTH//2, 180, center=True)
        draw_text(f"Personal Best: {pb}", font, YELLOW, DISPLAYSURF, WIDTH//2, 220, center=True)
        
        if button("Retry", 150, 280, 120, 40, GRAY, WHITE):
            game_loop(username, pb)
            return
        if button("Main Menu", 330, 280, 120, 40, GRAY, WHITE):
            return
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        pygame.display.update()

def draw_game(state):
    """
    Отрисовка всех игровых элементов на поле: сетки, змейки, еды, бонусов и препятствий.
    """
    DISPLAYSURF.fill(BLACK)
    # Отрисовка сетки
    if settings["grid"]:
        for x in range(0, WIDTH, BLOCK_SIZE):
            pygame.draw.line(DISPLAYSURF, (30, 30, 30), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, BLOCK_SIZE):
            pygame.draw.line(DISPLAYSURF, (30, 30, 30), (0, y), (WIDTH, y))

    # Змейка
    scolor = tuple(settings["snake_color"])
    if state.shield_active:
        # щит
        head = state.snake_body[0]
        pygame.draw.rect(DISPLAYSURF, CYAN, (head[0]-2, head[1]-2, BLOCK_SIZE+4, BLOCK_SIZE+4), 2)
        
    for i, pos in enumerate(state.snake_body):
        color = scolor if i == 0 else (max(0, scolor[0]-50), max(0, scolor[1]-50), max(0, scolor[2]-50))
        pygame.draw.rect(DISPLAYSURF, color, (pos[0], pos[1], BLOCK_SIZE, BLOCK_SIZE))
        
    # Еда
    for f in state.foods:
        color = {1: GREEN, 2: YELLOW, 3: BLUE}.get(f.weight, RED)
        pygame.draw.rect(DISPLAYSURF, color, (f.pos[0], f.pos[1], BLOCK_SIZE, BLOCK_SIZE))
        draw_text(str(f.weight), font_small, BLACK, DISPLAYSURF, f.pos[0] + BLOCK_SIZE//2, f.pos[1] + BLOCK_SIZE//2, center=True)
        
    if state.poison_food:
        pygame.draw.rect(DISPLAYSURF, DARK_RED, (state.poison_food.pos[0], state.poison_food.pos[1], BLOCK_SIZE, BLOCK_SIZE))
        draw_text("X", font_small, WHITE, DISPLAYSURF, state.poison_food.pos[0] + BLOCK_SIZE//2, state.poison_food.pos[1] + BLOCK_SIZE//2, center=True)
        
    # Бонусы
    if state.powerup:
        p_color = {'speed': CYAN, 'slow': MAGENTA, 'shield': WHITE}[state.powerup.type]
        pygame.draw.circle(DISPLAYSURF, p_color, (state.powerup.pos[0] + BLOCK_SIZE//2, state.powerup.pos[1] + BLOCK_SIZE//2), BLOCK_SIZE//2)
        letter = {'speed': 'F', 'slow': 'S', 'shield': 'D'}[state.powerup.type]
        draw_text(letter, font_small, BLACK, DISPLAYSURF, state.powerup.pos[0] + BLOCK_SIZE//2, state.powerup.pos[1] + BLOCK_SIZE//2, center=True)

    # Препятствия
    for obs in state.obstacles:
        pygame.draw.rect(DISPLAYSURF, GRAY, (obs[0], obs[1], BLOCK_SIZE, BLOCK_SIZE))
        
    # UI
    draw_text(f"Score: {state.score}  Lvl: {state.level}  PB: {max(state.pb, state.score)}", font, WHITE, DISPLAYSURF, 10, 5)

    pygame.display.update()

def game_loop(username, pb):
    """
    Главный игровой цикл: обработка событий управления, обновление логики и отрисовка.
    """
    state = GameState(username, pb) # Создаём новое состояние игры
    clock = pygame.time.Clock()
    
    if settings["sound"]:
        try:
            pygame.mixer.music.play(-1)
        except:
            pass
            
    while not state.game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    state.change_to = 'UP'
                if event.key == pygame.K_DOWN:
                    state.change_to = 'DOWN'
                if event.key == pygame.K_LEFT:
                    state.change_to = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    state.change_to = 'RIGHT'
                    
        state.update()
        if state.game_over:
            break
            
        draw_game(state)
        clock.tick(state.speed)
        
    game_over_screen(username, state.score, state.level, max(pb, state.score))

if __name__ == "__main__":
    init_db()
    main_menu()

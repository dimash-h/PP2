"""
TSIS 2: Paint (Рисовалка).
Программа для рисования различных фигур: линии, прямоугольники, круги, треугольники, ромбы и текст.
"""
import pygame
from datetime import datetime
import os
from tools import calculate_rect, calculate_square, get_right_tri_points, get_equilateral_tri_points, get_rhombus_points, flood_fill

pygame.init()

WIDTH = 1000
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint Application")

base_layer = pygame.Surface((WIDTH, HEIGHT))
base_layer.fill((255, 255, 255))
screen.fill((255, 255, 255))

colorRED = (255, 0, 0)
colorBLUE = (0, 0, 255)
colorGREEN = (0, 255, 0)
colorBLACK = (0, 0, 0)
colorWHITE = (255, 255, 255)
colorYELLOW = (255, 255, 0)
colorORANGE = (255, 165, 0)
colorPURPLE = (160, 32, 240)

clock = pygame.time.Clock()

LMBpressed = False
THICKNESS = 5

currX = 0
currY = 0
prevX = 0
prevY = 0

current_color = colorBLACK
tool = "brush"

# Переменные для текста
text_mode = False
current_text = ""
text_pos = (0, 0)
# Используем стандартный шрифт Pygame, он самый надежный и не выдаст черных квадратов
font_text = pygame.font.Font(None, 40) 

save_message_timer = 0

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            # Сохранение (Ctrl+S или Command+S для Mac)
            mods = pygame.key.get_mods()
            if event.key == pygame.K_s and (mods & pygame.KMOD_CTRL or mods & pygame.KMOD_META):
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                save_dir = os.path.dirname(os.path.abspath(__file__))
                save_path = os.path.join(save_dir, f"paint_{timestamp}.png")
                
                # Сохраняем холст вместе с недописанным текстом, если он есть
                save_surface = base_layer.copy()
                if text_mode and current_text:
                    text_surf = font_text.render(current_text, True, current_color)
                    save_surface.blit(text_surf, text_pos)
                    
                pygame.image.save(save_surface, save_path)
                continue

            # Ввод текста
            if text_mode:
                if event.key == pygame.K_RETURN:
                    # Печатаем текст навсегда на base_layer
                    text_surf = font_text.render(current_text, True, current_color)
                    base_layer.blit(text_surf, text_pos)
                    text_mode = False
                elif event.key == pygame.K_ESCAPE:
                    text_mode = False
                elif event.key == pygame.K_BACKSPACE:
                    current_text = current_text[:-1]
                else:
                    # Игнорируем системные символы (чтобы не было "квадратиков" или мусора)
                    if event.unicode.isprintable():
                        current_text += event.unicode
                continue
            else:
                # Очистка экрана (Clear) кнопкой X
                if event.key == pygame.K_x:
                    base_layer.fill(colorWHITE)
                    screen.fill(colorWHITE)

            # Толщина кисти
            if event.key == pygame.K_1: THICKNESS = 2
            if event.key == pygame.K_2: THICKNESS = 5
            if event.key == pygame.K_3: THICKNESS = 10
            
            # Инструменты
            if event.key == pygame.K_p: tool = "brush"
            if event.key == pygame.K_l: tool = "line"
            if event.key == pygame.K_r: tool = "rectangle"
            if event.key == pygame.K_g: tool = "circle"
            if event.key == pygame.K_e: tool = "eraser"
            if event.key == pygame.K_f: tool = "fill"
            if event.key == pygame.K_t: tool = "text"
            if event.key == pygame.K_q: tool = "square"
            if event.key == pygame.K_d: tool = "right_tri"
            if event.key == pygame.K_y: tool = "equil_tri"
            if event.key == pygame.K_h: tool = "rhombus"

            # Цвета
            if event.key == pygame.K_z: current_color = colorBLACK
            if event.key == pygame.K_w: current_color = colorRED
            if event.key == pygame.K_c: current_color = colorGREEN
            if event.key == pygame.K_v: current_color = colorBLUE
            if event.key == pygame.K_b: current_color = colorYELLOW
            if event.key == pygame.K_n: current_color = colorORANGE
            if event.key == pygame.K_m: current_color = colorPURPLE

        # Нажали кнопку мыши
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            LMBpressed = True
            prevX = event.pos[0]
            prevY = event.pos[1]
            currX = event.pos[0]
            currY = event.pos[1]
            
            if tool == "text":
                text_mode = True
                text_pos = event.pos
                current_text = ""
            elif tool == "fill":
                flood_fill(base_layer, event.pos, current_color)
            elif tool == "brush":
                # Радиус кружка должен быть половиной толщины линии
                radius = THICKNESS // 2 if THICKNESS > 1 else 1
                pygame.draw.circle(base_layer, current_color, (currX, currY), radius)
            elif tool == "eraser":
                # Ластик работает так же, только он толще (THICKNESS * 4) и рисует белым
                radius = (THICKNESS * 4) // 2
                pygame.draw.circle(base_layer, colorWHITE, (currX, currY), radius)

        # Движение мыши
        if event.type == pygame.MOUSEMOTION:
            if LMBpressed:
                currX = event.pos[0]
                currY = event.pos[1]
                
                # Рисуем "превью" фигур (копируем базу, чтобы затереть прошлый кадр, и рисуем поверх нее на экране)
                if tool == "rectangle":
                    screen.blit(base_layer, (0, 0))
                    pygame.draw.rect(screen, current_color, calculate_rect((prevX, prevY), (currX, currY)), THICKNESS)
                
                elif tool == "square":
                    screen.blit(base_layer, (0, 0))
                    pygame.draw.rect(screen, current_color, calculate_square((prevX, prevY), (currX, currY)), THICKNESS)
                
                elif tool == "circle":
                    screen.blit(base_layer, (0, 0))
                    radius = int(((currX - prevX) ** 2 + (currY - prevY) ** 2) ** 0.5 / 2)
                    center = (prevX + (currX - prevX) // 2, prevY + (currY - prevY) // 2)
                    pygame.draw.circle(screen, current_color, center, radius, THICKNESS)
                
                elif tool == "right_tri":
                    screen.blit(base_layer, (0, 0))
                    pygame.draw.polygon(screen, current_color, get_right_tri_points((prevX, prevY), (currX, currY)), THICKNESS)
                
                elif tool == "equil_tri":
                    screen.blit(base_layer, (0, 0))
                    pygame.draw.polygon(screen, current_color, get_equilateral_tri_points((prevX, prevY), (currX, currY)), THICKNESS)
                
                elif tool == "rhombus":
                    screen.blit(base_layer, (0, 0))
                    pygame.draw.polygon(screen, current_color, get_rhombus_points((prevX, prevY), (currX, currY)), THICKNESS)
                
                elif tool == "line":
                    screen.blit(base_layer, (0, 0))
                    pygame.draw.line(screen, current_color, (prevX, prevY), (currX, currY), THICKNESS)
                
                # Кисть и ластик рисуются прямо на base_layer чтобы оставлять след
                # Добавлен draw.circle на каждом шаге для "закругления" концов линии (убирает угловатые шлейфы)
                elif tool == "brush":
                    pygame.draw.line(base_layer, current_color, (prevX, prevY), (currX, currY), THICKNESS)
                    pygame.draw.circle(base_layer, current_color, (currX, currY), THICKNESS // 2 if THICKNESS > 1 else 1)
                    prevX, prevY = currX, currY
                    
                elif tool == "eraser":
                    pygame.draw.line(base_layer, colorWHITE, (prevX, prevY), (currX, currY), THICKNESS * 4)
                    pygame.draw.circle(base_layer, colorWHITE, (currX, currY), (THICKNESS * 4) // 2)
                    prevX, prevY = currX, currY

        # Отпустили кнопку мыши
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            LMBpressed = False
            currX = event.pos[0]
            currY = event.pos[1]
            
            # Окончательная отрисовка фигур ПРЯМО НА BASE_LAYER (важно для Mac Retina и сохранения!)
            if tool == "rectangle":
                pygame.draw.rect(base_layer, current_color, calculate_rect((prevX, prevY), (currX, currY)), THICKNESS)
            elif tool == "square":
                pygame.draw.rect(base_layer, current_color, calculate_square((prevX, prevY), (currX, currY)), THICKNESS)
            elif tool == "circle":
                radius = int(((currX - prevX) ** 2 + (currY - prevY) ** 2) ** 0.5 / 2)
                center = (prevX + (currX - prevX) // 2, prevY + (currY - prevY) // 2)
                pygame.draw.circle(base_layer, current_color, center, radius, THICKNESS)
            elif tool == "right_tri":
                pygame.draw.polygon(base_layer, current_color, get_right_tri_points((prevX, prevY), (currX, currY)), THICKNESS)
            elif tool == "equil_tri":
                pygame.draw.polygon(base_layer, current_color, get_equilateral_tri_points((prevX, prevY), (currX, currY)), THICKNESS)
            elif tool == "rhombus":
                pygame.draw.polygon(base_layer, current_color, get_rhombus_points((prevX, prevY), (currX, currY)), THICKNESS)
            elif tool == "line":
                pygame.draw.line(base_layer, current_color, (prevX, prevY), (currX, currY), THICKNESS)

    # Обновление экрана: всегда показываем актуальную базу перед UI
    screen.blit(base_layer, (0, 0))

    # Если мы рисуем превью фигуры, рисуем его поверх базы только на screen
    if LMBpressed and tool in ("rectangle", "square", "circle", "right_tri", "equil_tri", "rhombus", "line"):
        if tool == "rectangle":
            pygame.draw.rect(screen, current_color, calculate_rect((prevX, prevY), (currX, currY)), THICKNESS)
        elif tool == "square":
            pygame.draw.rect(screen, current_color, calculate_square((prevX, prevY), (currX, currY)), THICKNESS)
        elif tool == "circle":
            radius = int(((currX - prevX) ** 2 + (currY - prevY) ** 2) ** 0.5 / 2)
            center = (prevX + (currX - prevX) // 2, prevY + (currY - prevY) // 2)
            pygame.draw.circle(screen, current_color, center, radius, THICKNESS)
        elif tool == "right_tri":
            pygame.draw.polygon(screen, current_color, get_right_tri_points((prevX, prevY), (currX, currY)), THICKNESS)
        elif tool == "equil_tri":
            pygame.draw.polygon(screen, current_color, get_equilateral_tri_points((prevX, prevY), (currX, currY)), THICKNESS)
        elif tool == "rhombus":
            pygame.draw.polygon(screen, current_color, get_rhombus_points((prevX, prevY), (currX, currY)), THICKNESS)
        elif tool == "line":
            pygame.draw.line(screen, current_color, (prevX, prevY), (currX, currY), THICKNESS)

    # ==========================================
    # UI-ДИЗАЙН (ТЕМНЫЙ СТИЛЬ С КРУПНЫМ ТЕКСТОМ)
    # ==========================================
    ui_height = 85
    pygame.draw.rect(screen, (50, 50, 50), (0, 0, WIDTH, ui_height)) # Серый фон
    pygame.draw.line(screen, (200, 200, 200), (0, ui_height), (WIDTH, ui_height), 2)
    pygame.draw.line(screen, (100, 100, 100), (0, 42), (WIDTH, 42), 1) # Разделитель строк
    pygame.draw.line(screen, (100, 100, 100), (0, 64), (WIDTH, 64), 1) # Разделитель инструментов и цветов

    font_large = pygame.font.SysFont("Verdana", 16, bold=True) # Немного уменьшили для компактности
    font_small = pygame.font.SysFont("Verdana", 11, bold=True) # Чтобы все тулсы 100% влезли

    # --- Строка 1 ---
    # TOOL: PENCIL
    tool_text = font_large.render(f"TOOL: {tool.upper()}", True, colorWHITE)
    screen.blit(tool_text, (15, 10))
    
    # Квадрат цвета
    box_x = 15 + tool_text.get_width() + 15
    pygame.draw.rect(screen, current_color, (box_x, 8, 26, 26))
    pygame.draw.rect(screen, colorWHITE, (box_x, 8, 26, 26), 2)
    
    # BRUSH SIZE
    brush_text = font_large.render("BRUSH SIZE:", True, colorWHITE)
    screen.blit(brush_text, (box_x + 40, 10))
    
    b_x = box_x + 40 + brush_text.get_width() + 15
    for i, size_val in enumerate([2, 5, 10]):
        is_active = (THICKNESS == size_val)
        btn_bg = colorWHITE if is_active else (80, 80, 80)
        btn_text = colorBLACK if is_active else colorWHITE
        
        pygame.draw.rect(screen, btn_bg, (b_x, 8, 26, 26))
        pygame.draw.rect(screen, colorWHITE, (b_x, 8, 26, 26), 2)
        
        num_surf = font_large.render(str(i+1), True, btn_text)
        screen.blit(num_surf, (b_x + (26 - num_surf.get_width())//2, 8 + (26 - num_surf.get_height())//2))
        b_x += 35

    # CLEAR и SAVE
    clear_text = font_large.render("CLEAR: [X]", True, (255, 50, 50))
    screen.blit(clear_text, (b_x + 20, 10))
    
    save_text = font_large.render("SAVE: [Ctrl+S]", True, (50, 255, 50))
    screen.blit(save_text, (b_x + 140, 10))

    if text_mode:
        blink_color = (100, 255, 100) if (pygame.time.get_ticks() // 500) % 2 == 0 else colorWHITE
        mode_text = font_large.render("(Press ENTER)", True, blink_color)
        screen.blit(mode_text, (b_x + 320, 10))

    # --- Строка 2 (Инструменты) ---
    tools_arr = ["[P] Pencil", "[L] Line", "[F] Fill", "[T] Text", "[E] Eraser", "[R] Rect", "[G] Circle", "[Q] Square", "[D] R.Tri", "[Y] Eq.Tri", "[H] Rhomb"]
    x_offset = 12
    for t_str in tools_arr:
        t_surf = font_small.render(t_str, True, colorWHITE)
        screen.blit(t_surf, (x_offset, 46))
        x_offset += t_surf.get_width() + 12
        if t_str != tools_arr[-1]:
            pygame.draw.line(screen, (150, 150, 150), (x_offset, 44), (x_offset, 62), 1)
            x_offset += 12

    # --- Строка 3 (Цвета) ---
    colors_arr = ["[Z] Black", "[W] Red", "[C] Green", "[V] Blue", "[B] Yellow", "[N] Orange", "[M] Purple"]
    x_offset = 12
    for c_str in colors_arr:
        c_surf = font_small.render(c_str, True, colorWHITE)
        screen.blit(c_surf, (x_offset, 68))
        x_offset += c_surf.get_width() + 12
        if c_str != colors_arr[-1]:
            pygame.draw.line(screen, (150, 150, 150), (x_offset, 66), (x_offset, 83), 1)
            x_offset += 12
    # ==========================================

    # Отрисовка текста при наборе (ПОВЕРХ ВСЕГО)
    if text_mode and text_pos:
        display_text = current_text + "|" if (pygame.time.get_ticks() // 500) % 2 == 0 else current_text
        # Добавляем светло-серый фон во время набора текста, чтобы его было 100% видно
        text_surf = font_text.render(display_text, True, current_color, (220, 220, 220))
        screen.blit(text_surf, text_pos)

    # Уведомление об успешном сохранении (показывается 2 секунды)
    if save_message_timer > 0 and pygame.time.get_ticks() - save_message_timer < 2000:
        save_msg = font_large.render("IMAGE SAVED TO TSIS2 FOLDER!", True, (50, 255, 50))
        bg_rect = save_msg.get_rect(center=(WIDTH//2, HEIGHT//2))
        pygame.draw.rect(screen, (30, 30, 30), bg_rect.inflate(20, 20))
        pygame.draw.rect(screen, (50, 255, 50), bg_rect.inflate(20, 20), 2)
        screen.blit(save_msg, bg_rect)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()

"""
Вспомогательные инструменты для Paint: функции для рисования сложных геометрических фигур (ромб, треугольники и т.д.).
"""
import pygame
import math

def calculate_rect(p1, p2):
    """Вычисляет координаты прямоугольника по двум точкам (начало и конец)."""
    x1, y1 = p1
    x2, y2 = p2
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))

def calculate_square(p1, p2):
    """Создает ровный квадрат, беря за основу максимальную сторону."""
    x1, y1 = p1
    x2, y2 = p2
    side = max(abs(x2 - x1), abs(y2 - y1))
    rx = x1 if x2 > x1 else x1 - side
    ry = y1 if y2 > y1 else y1 - side
    return pygame.Rect(rx, ry, side, side)

def get_right_tri_points(p1, p2):
    """Возвращает 3 точки для прямоугольного треугольника."""
    return [p1, (p1[0], p2[1]), p2]

def get_equilateral_tri_points(p1, p2):
    """Рассчитывает точки для равностороннего треугольника (все стороны равны)."""
    x1, y1 = p1
    x2, y2 = p2
    side = abs(x2 - x1)
    height = side * math.sqrt(3) / 2
    
    y_dir = 1 if y2 > y1 else -1
    x_dir = 1 if x2 > x1 else -1
    
    p_top = (int(x1 + (x2 - x1) / 2), int(y1))
    p_left = (int(x1), int(y1 + y_dir * height))
    p_right = (int(x1 + x_dir * side), int(y1 + y_dir * height))
    return [p_top, p_left, p_right]

def get_rhombus_points(p1, p2):
    """Возвращает 4 точки для ромба внутри заданного прямоугольника."""
    rect = calculate_rect(p1, p2)
    return [(rect.centerx, rect.top), (rect.right, rect.centery), 
            (rect.centerx, rect.bottom), (rect.left, rect.centery)]

def flood_fill(surface, position, fill_color):
    """
    Алгоритм заливки (Flood-Fill).
    Ищет соседние пиксели такого же цвета и закрашивает их.

    """
    target_color = surface.get_at(position)[:3]  #берём только RGB
    fill_color_rgb = fill_color[:3] if len(fill_color) == 4 else fill_color
    
    # Если цвет уже такой, какой нам нужен - ничего не делаем
    if target_color == fill_color_rgb:
        return

    width = surface.get_width()
    height = surface.get_height()
    
    # Стек — список пикселей которые нужно обработать
    stack = [position]
    surface.set_at(position, fill_color)
    
    while stack:
        x, y = stack.pop()
        
        # Проверяем 4 соседних пикселя: влево, вправо, вверх, вниз
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            # Убеждаемся, что не вышли за края экрана
            if 0 <= nx < width and 0 <= ny < height:
                if surface.get_at((nx, ny))[:3] == target_color:
                    surface.set_at((nx, ny), fill_color)
                    stack.append((nx, ny))

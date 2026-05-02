import pygame
from config import *

# 1. DRAW BACKGROUND
def draw_bg(screen):
    """Fills the screen with a dark color (from config.py)."""
    screen.fill(DARK)

# 2. DRAW TEXT
def draw_text(screen, font, text, color, x, y, center=True):
    """
    Simplifies drawing text. 
    If center=True, (x, y) is the middle of the text.
    """
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    
    if center:
        text_rect.center = (x, y)
    else:
        text_rect.topleft = (x, y)
        
    screen.blit(text_surface, text_rect)

# 3. DRAW BUTTON
def draw_button(screen, font, text, rect, is_hovered):
    """
    Draws a rectangle button that changes color when the mouse is over it.
    """
    # Change color based on 'is_hovered' (True/False)
    base_color = (50, 160, 80) if is_hovered else (25, 80, 45)
    border_color = WHITE if is_hovered else LGRAY
    
    # Draw the box
    pygame.draw.rect(screen, base_color, rect, border_radius=10)
    # Draw a thin outline
    pygame.draw.rect(screen, border_color, rect, 2, border_radius=10)
    
    # Draw the text in the middle of the button
    draw_text(screen, font, text, WHITE, rect.centerx, rect.centery)

# 4. CHECK MOUSE HOVER
def is_hovered(rect, mouse_pos):
    """Returns True if the mouse cursor is inside the button rectangle."""
    return rect.collidepoint(mouse_pos)
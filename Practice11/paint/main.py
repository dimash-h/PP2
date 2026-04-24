import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors for selection
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

COLORS = [BLACK, RED, GREEN, BLUE]
COLOR_NAMES = ["BLACK", "RED", "GREEN", "BLUE"]

# Setup Display and Fonts
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint - Tools: P(Pen), E(Eraser), R(Rect), C(Circ), S(Square), T(Right Tri), Y(Eq Tri), H(Rhombus)")
font = pygame.font.SysFont("Verdana", 15)

# Tool modes
TOOL_PEN = 'pen'
TOOL_RECT = 'rect'
TOOL_CIRCLE = 'circle'
TOOL_ERASER = 'eraser'
TOOL_SQUARE = 'square'
TOOL_RIGHT_TRI = 'right_tri'
TOOL_EQUILATERAL_TRI = 'equilateral_tri'
TOOL_RHOMBUS = 'rhombus'

def calculate_rect(p1, p2):
    """
    Calculates a pygame.Rect safely given two coordinate tuples.
    This allows drawing rectangles in any direction (up/left/down/right).
    """
    x1, y1 = p1
    x2, y2 = p2
    return pygame.Rect(min(x1, x2), min(y1, y2), abs(x1 - x2), abs(y1 - y2))

def calculate_square(p1, p2):
    """Calculates a square based on the drag distance."""
    x1, y1 = p1
    x2, y2 = p2
    side = max(abs(x2 - x1), abs(y2 - y1))
    rx = x1 if x2 > x1 else x1 - side
    ry = y1 if y2 > y1 else y1 - side
    return pygame.Rect(rx, ry, side, side)

def get_right_tri_points(p1, p2):
    """Returns points for a right triangle."""
    return [p1, (p1[0], p2[1]), p2]

def get_equilateral_tri_points(p1, p2):
    """Returns points for an equilateral triangle based on drag width."""
    x1, y1 = p1
    x2, y2 = p2
    side = abs(x2 - x1)
    height = side * math.sqrt(3) / 2
    
    y_dir = 1 if y2 > y1 else -1
    x_dir = 1 if x2 > x1 else -1
    
    p_top = (x1 + (x2 - x1) / 2, y1)
    p_left = (x1, y1 + y_dir * height)
    p_right = (x1 + x_dir * side, y1 + y_dir * height)
    return [p_top, p_left, p_right]

def get_rhombus_points(p1, p2):
    """Returns points for a rhombus inscribed in the bounding rect."""
    rect = calculate_rect(p1, p2)
    return [(rect.centerx, rect.top), (rect.right, rect.centery), 
            (rect.centerx, rect.bottom), (rect.left, rect.centery)]

def main():
    clock = pygame.time.Clock()
    
    # Main drawing canvas. We draw here permanently.
    canvas = pygame.Surface((WIDTH, HEIGHT))
    canvas.fill(WHITE)
    
    # Application State Variables
    current_color = BLACK
    current_color_idx = 0
    current_tool = TOOL_PEN
    
    brush_size = 5
    eraser_size = 20
    
    # Drawing State
    drawing = False
    start_pos = None
    last_pos = None

    while True:
        # 1. Event Handling Phase
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            # Keyboard shortcuts to change tools and colors
            if event.type == pygame.KEYDOWN:
                # Colors
                if event.key == pygame.K_1: current_color_idx = 0; current_color = COLORS[0]
                if event.key == pygame.K_2: current_color_idx = 1; current_color = COLORS[1]
                if event.key == pygame.K_3: current_color_idx = 2; current_color = COLORS[2]
                if event.key == pygame.K_4: current_color_idx = 3; current_color = COLORS[3]
                
                # Tools
                if event.key == pygame.K_p: current_tool = TOOL_PEN
                if event.key == pygame.K_e: current_tool = TOOL_ERASER
                if event.key == pygame.K_r: current_tool = TOOL_RECT
                if event.key == pygame.K_c: current_tool = TOOL_CIRCLE
                if event.key == pygame.K_s: current_tool = TOOL_SQUARE
                if event.key == pygame.K_t: current_tool = TOOL_RIGHT_TRI
                if event.key == pygame.K_y: current_tool = TOOL_EQUILATERAL_TRI
                if event.key == pygame.K_h: current_tool = TOOL_RHOMBUS

            # Mouse Input for Drawing
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Left click initiates drawing
                    drawing = True
                    start_pos = event.pos
                    last_pos = event.pos

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                    # Finalize drawing for shapes
                    if current_tool == TOOL_RECT and start_pos:
                        rect = calculate_rect(start_pos, event.pos)
                        pygame.draw.rect(canvas, current_color, rect, brush_size)
                    elif current_tool == TOOL_CIRCLE and start_pos:
                        # Circle radius derived from bounding box hypotenuse
                        rect = calculate_rect(start_pos, event.pos)
                        radius = int(math.hypot(rect.width, rect.height) / 2)
                        # Center point is midpoint between start_pos and current mouse pos
                        center = (start_pos[0] + (event.pos[0] - start_pos[0]) // 2, 
                                  start_pos[1] + (event.pos[1] - start_pos[1]) // 2)
                        if radius > 0:
                            pygame.draw.circle(canvas, current_color, center, radius, brush_size)
                    elif current_tool == TOOL_SQUARE and start_pos:
                        rect = calculate_square(start_pos, event.pos)
                        pygame.draw.rect(canvas, current_color, rect, brush_size)
                    elif current_tool == TOOL_RIGHT_TRI and start_pos:
                        points = get_right_tri_points(start_pos, event.pos)
                        pygame.draw.polygon(canvas, current_color, points, brush_size)
                    elif current_tool == TOOL_EQUILATERAL_TRI and start_pos:
                        points = get_equilateral_tri_points(start_pos, event.pos)
                        # Polygon needs at least 3 points, which it has
                        pygame.draw.polygon(canvas, current_color, points, brush_size)
                    elif current_tool == TOOL_RHOMBUS and start_pos:
                        points = get_rhombus_points(start_pos, event.pos)
                        pygame.draw.polygon(canvas, current_color, points, brush_size)
                    
                    # Reset points
                    start_pos = None
                    last_pos = None

            if event.type == pygame.MOUSEMOTION:
                if drawing:
                    # Pen draws continuous lines between events
                    if current_tool == TOOL_PEN:
                        pygame.draw.line(canvas, current_color, last_pos, event.pos, brush_size)
                        last_pos = event.pos
                    # Eraser draws thick white circles
                    elif current_tool == TOOL_ERASER:
                        pygame.draw.circle(canvas, WHITE, event.pos, eraser_size)

        # 2. Rendering Phase
        # Blit the permanent canvas to screen
        screen.blit(canvas, (0, 0))

        # Render shape preview dynamically if user is currently dragging
        if drawing and start_pos:
            mouse_pos = pygame.mouse.get_pos()
            if current_tool == TOOL_RECT:
                rect = calculate_rect(start_pos, mouse_pos)
                pygame.draw.rect(screen, current_color, rect, brush_size)
            elif current_tool == TOOL_CIRCLE:
                rect = calculate_rect(start_pos, mouse_pos)
                radius = int(math.hypot(rect.width, rect.height) / 2)
                center = (start_pos[0] + (mouse_pos[0] - start_pos[0]) // 2, 
                          start_pos[1] + (mouse_pos[1] - start_pos[1]) // 2)
                if radius > 0:
                    pygame.draw.circle(screen, current_color, center, radius, brush_size)
            elif current_tool == TOOL_SQUARE:
                rect = calculate_square(start_pos, mouse_pos)
                pygame.draw.rect(screen, current_color, rect, brush_size)
            elif current_tool == TOOL_RIGHT_TRI:
                points = get_right_tri_points(start_pos, mouse_pos)
                pygame.draw.polygon(screen, current_color, points, brush_size)
            elif current_tool == TOOL_EQUILATERAL_TRI:
                points = get_equilateral_tri_points(start_pos, mouse_pos)
                pygame.draw.polygon(screen, current_color, points, brush_size)
            elif current_tool == TOOL_RHOMBUS:
                points = get_rhombus_points(start_pos, mouse_pos)
                pygame.draw.polygon(screen, current_color, points, brush_size)

        # Render UI Information Overlay
        info_text = f"Tool: {current_tool.upper()} | Color: {COLOR_NAMES[current_color_idx]}"
        ui_surface = font.render(info_text, True, BLACK)
        
        # White background for text readability
        pygame.draw.rect(screen, WHITE, (5, 5, ui_surface.get_width() + 10, 25))
        pygame.draw.rect(screen, BLACK, (5, 5, ui_surface.get_width() + 10, 25), 1) # Border
        screen.blit(ui_surface, (10, 10))

        # Update Display and tick clock
        pygame.display.update()
        clock.tick(FPS)

if __name__ == "__main__":
    main()

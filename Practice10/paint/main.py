import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

base_layer = pygame.Surface((WIDTH, HEIGHT))
base_layer.fill((255, 255, 255))
screen.fill((255, 255, 255))

colorRED = (255, 0, 0)
colorBLUE = (0, 0, 255)
colorWHITE = (255, 255, 255)
colorBLACK = (0, 0, 0)
colorGREEN = (0, 255, 0)

clock = pygame.time.Clock()

LMBpressed = False
THICKNESS = 5

currX = 0
currY = 0
prevX = 0
prevY = 0

current_color = colorBLACK
tool = "brush"


def calculate_rect(x1, y1, x2, y2):
    return pygame.Rect(
        min(x1, x2),
        min(y1, y2),
        abs(x1 - x2),
        abs(y1 - y2)
    )


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Нажали левую кнопку мыши
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            LMBpressed = True
            prevX = event.pos[0]
            prevY = event.pos[1]

        # Движение мыши
        if event.type == pygame.MOUSEMOTION:
            currX = event.pos[0]
            currY = event.pos[1]

            if LMBpressed:
                if tool == "rectangle":
                    screen.blit(base_layer, (0, 0))
                    pygame.draw.rect(
                        screen,
                        current_color,
                        calculate_rect(prevX, prevY, currX, currY),
                        THICKNESS
                    )

                elif tool == "circle":
                    screen.blit(base_layer, (0, 0))
                    radius = int(((currX - prevX) ** 2 + (currY - prevY) ** 2) ** 0.5)
                    pygame.draw.circle(
                        screen,
                        current_color,
                        (prevX, prevY),
                        radius,
                        THICKNESS
                    )

                elif tool == "brush":
                    pygame.draw.circle(screen, current_color, (currX, currY), THICKNESS)

                elif tool == "eraser":
                    pygame.draw.circle(screen, colorWHITE, (currX, currY), THICKNESS * 2)

        # Отпустили левую кнопку мыши
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            LMBpressed = False
            currX = event.pos[0]
            currY = event.pos[1]

            if tool == "rectangle":
                pygame.draw.rect(
                    screen,
                    current_color,
                    calculate_rect(prevX, prevY, currX, currY),
                    THICKNESS
                )

            elif tool == "circle":
                radius = int(((currX - prevX) ** 2 + (currY - prevY) ** 2) ** 0.5)
                pygame.draw.circle(
                    screen,
                    current_color,
                    (prevX, prevY),
                    radius,
                    THICKNESS
                )

            # Сохраняем рисунок на base_layer
            base_layer.blit(screen, (0, 0))

        # Управление с клавиатуры
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_EQUALS:
                THICKNESS += 1

            if event.key == pygame.K_MINUS:
                THICKNESS -= 1
                if THICKNESS < 1:
                    THICKNESS = 1

            # Выбор инструментов
            if event.key == pygame.K_b:
                tool = "brush"

            if event.key == pygame.K_r:
                tool = "rectangle"

            if event.key == pygame.K_c:
                tool = "circle"

            if event.key == pygame.K_e:
                tool = "eraser"

            # Выбор цвета
            if event.key == pygame.K_1:
                current_color = colorBLACK

            if event.key == pygame.K_2:
                current_color = colorRED

            if event.key == pygame.K_3:
                current_color = colorGREEN

            if event.key == pygame.K_4:
                current_color = colorBLUE

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
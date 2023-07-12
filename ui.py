import pygame
from maze_generator import Maze, MazeController

WIDTH = 400
HEIGHT = 200
RES = WIDTH, HEIGHT

COLOR = (100, 100, 100)
WHITE = (255, 255, 255)
color_passive = (200, 200, 200)
BLACk = (0, 0, 0)

active = False

pygame.init()
sc = pygame.display.set_mode(RES)
font = pygame.font.Font('freesansbold.ttf', 30)
text = font.render("Maze Generator", True, WHITE)
textRect = text.get_rect()
textRect.center = (WIDTH // 2, HEIGHT // 5)
base_font = pygame.font.Font(None, 32)
user_text = ""

input_rect = pygame.Rect(253, 96, 57, 32)
button_box = pygame.Rect(140, 150, 108, 32)
length = True

while True:
    sc.fill(pygame.Color(COLOR))
    text_surface = base_font.render(user_text, True, BLACk)
    text_surface2 = base_font.render("Enter Maze Size:", True, WHITE)
    button = base_font.render("Continue", True, WHITE)
    mouse = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if 253 <= mouse[0] <= 310 and 96 <= mouse[1] <= 128:
                active = True
            else:
                active = False
            if 140 <= mouse[0] <= 140 + 108 and 150 <= mouse[1] <= 150 + 32:
                maze_controller = MazeController(int(user_text))
                maze_controller.run()

        if event.type == pygame.KEYDOWN:
            if active:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode

        while len(user_text) > 3:
            user_text = user_text[:-1]

    pygame.draw.rect(sc, WHITE, input_rect)
    pygame.draw.rect(sc, WHITE, button_box, 2)

    sc.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
    sc.blit(text_surface2, (50, 100))
    sc.blit(text, textRect)
    sc.blit(button, (button_box.x + 5, button_box.y + 5))

    pygame.display.flip()

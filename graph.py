import pygame
from random import choice

WIDTH = 1200
HEIGHT = 900
RES = WIDTH, HEIGHT
TILE = 20
cols, rows = WIDTH // TILE, HEIGHT // TILE

pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()


def find_index(x, y):
    return x + y * cols


class Cell:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self.visited = False

    def draw_current_cell(self):
        x = self.x * TILE
        y = self.y * TILE
        pygame.draw.rect(sc, pygame.Color("pink"), (x + 2, y + 2, TILE - 2, TILE - 2))

    def draw(self):
        x = self.x * TILE
        y = self.y * TILE

        if self.visited:
            pygame.draw.rect(sc, pygame.Color("darkgreen"), (x, y, TILE, TILE))

        if self.walls["top"]:
            pygame.draw.line(sc, pygame.Color("white"), (x, y), (x + TILE, y), 2)
        if self.walls["right"]:
            pygame.draw.line(sc, pygame.Color("white"), (x + TILE, y), (x + TILE, y + TILE), 2)
        if self.walls["bottom"]:
            pygame.draw.line(sc, pygame.Color("white"), (x + TILE, y + TILE), (x, y + TILE), 2)
        if self.walls["left"]:
            pygame.draw.line(sc, pygame.Color("white"), (x, y + TILE), (x, y), 2)

    @staticmethod
    def check_cell(x, y):
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x, y)]

    def check_neighbors(self):
        neighbors = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)

        return choice(neighbors) if neighbors else False


def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls["left"] = False
        next.walls["right"] = False
    elif dx == -1:
        current.walls["right"] = False
        next.walls["left"] = False
    dy = current.y - next.y
    if dy == 1:
        current.walls["top"] = False
        next.walls["bottom"] = False
    elif dy == -1:
        current.walls["bottom"] = False
        next.walls["top"] = False


grid_cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
current_cell = grid_cells[0]
stack = []

while True:
    sc.fill(pygame.Color("black"))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    for cell in grid_cells:
        cell.draw()
    current_cell.visited = True
    current_cell.draw_current_cell()

    next_cell = current_cell.check_neighbors()
    if next_cell:
        next_cell.visited = True
        stack.append(current_cell)
        remove_walls(current_cell, next_cell)
        current_cell = next_cell
    elif stack:
        current_cell = stack.pop()

    pygame.display.flip()
    clock.tick(40)

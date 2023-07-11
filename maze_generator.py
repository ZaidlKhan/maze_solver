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


class Maze:
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

        def check_cell(self, x, y):
            if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
                return False
            return maze.grid_cells[find_index(x, y)]

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

    def __init__(self, width):
        self.width = width
        self.height = width
        self.res = self.width, self.height
        self.cols = self.width // TILE
        self.rows = self.width // TILE
        self.sc = pygame.display.set_mode(self.res)
        self.grid_cells = [Maze.Cell(col, row) for row in range(self.rows) for col in range(self.cols)]
        self.current_cell = self.grid_cells[0]
        self.stack = []
        self.start = None
        self.end = None

    def remove_walls(self, current, next):
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

    def draw(self):
        sc.fill(pygame.Color("black"))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // TILE
                row = y // TILE
                clicked_cell = self.grid_cells[find_index(col, row)]

                if not self.start:
                    self.start = clicked_cell
                    self.start.visited = True
                elif not self.end:
                    self.end = clicked_cell
                    self.end.visited = True

        for cell in self.grid_cells:
            cell.draw()
        self.current_cell.visited = True
        self.current_cell.draw_current_cell()

        next_cell = self.current_cell.check_neighbors()
        if next_cell:
            next_cell.visited = True
            self.stack.append(self.current_cell)
            self.remove_walls(self.current_cell, next_cell)
            self.current_cell = next_cell
        elif self.stack:
            self.current_cell = self.stack.pop()

        if self.start:
            self.start.draw_current_cell()
        if self.end:
            self.end.draw_current_cell()

        pygame.display.flip()
        clock.tick(40)

maze = Maze(WIDTH)

while True:
    maze.draw()



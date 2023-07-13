import pygame
from random import choice
import maze_solver

pygame.init()


class MazeController:
    def __init__(self, width):
        self.width = width
        self.height = width
        self.tile = 20
        self.cols, self.rows = self.width // self.tile, self.height // self.tile
        self.res = self.width, self.height
        self.screen = pygame.display.set_mode(self.res)
        self.clock = pygame.time.Clock()
        self.maze = Maze(self)
        self.start_point = None
        self.end_point = None

    def run(self):
        while not self.maze.is_done():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
            self.maze.draw()
            pygame.display.flip()
            self.clock.tick(350)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    col = x // self.tile
                    row = y // self.tile
                    if not self.end_point and self.start_point:
                        self.select_cell(col, row)
                        self.end_point = (col, row)
                        self.maze.end_point = self.end_point
                    if not self.start_point and not self.end_point:
                        self.select_cell(col, row)
                        self.start_point = (col, row)
                        self.maze.start_point = self.start_point
                    if self.start_point and self.end_point:
                        solver = maze_solver.MazeSolver(self.maze, self)
                        path = solver.solve()
                        self.draw_solution(path)
            pygame.display.flip()
            self.clock.tick(350)

    def draw_solution(self, path):
        tile = self.tile
        for cell in path:
            x, y = cell
            pygame.draw.rect(self.screen, pygame.Color('lightblue'), (tile*x + 7, tile*y + 7, tile - 14, tile - 14))
            pygame.display.flip()
            self.clock.tick(30)

    def select_cell(self, col, row):
        cell = self.maze.grid_cells[self.find_index(col, row)]
        cell.selected = True
        cell.draw()
        pygame.display.flip()

    def find_index(self, x, y):
        return x + y * self.cols

    def check_cell(self, x, y):
        if x < 0 or x > self.cols - 1 or y < 0 or y > self.rows - 1:
            return False
        return self.maze.grid_cells[self.find_index(x, y)]


class Maze:
    def __init__(self, controller):
        self.controller = controller
        self.grid_cells = [Maze.Cell(col, row, controller, controller.screen, controller.tile)
                           for row in range(controller.rows) for col in range(controller.cols)]
        self.current_cell = self.grid_cells[0]
        self.stack = []
        self.start_point = None
        self.end_point = None
        self.generated = False

    def is_done(self):
        done = all(cell.visited for cell in self.grid_cells) and not self.stack
        self.generated = done
        return done

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
        self.controller.screen.fill(pygame.Color("black"))
        for cell in self.grid_cells:
            cell.draw()
        self.current_cell.visited = True
        next_cell = self.current_cell.check_neighbors()
        if next_cell:
            next_cell.visited = True
            self.stack.append(self.current_cell)
            self.remove_walls(self.current_cell, next_cell)
            self.current_cell = next_cell
        elif self.stack:
            self.current_cell = self.stack.pop()
        if self.is_done():
            self.current_cell.draw_current_cell()
        pygame.display.flip()
        self.controller.clock.tick(250)

    class Cell:
        def __init__(self, x, y, controller, sc, tile):
            self.x = x
            self.y = y
            self.controller = controller
            self.walls = {"top": True, "right": True, "bottom": True, "left": True}
            self.visited = False
            self.graph_visited = False
            self.color = None
            self.selected = False
            self.sc = sc
            self.tile = tile

        def draw_current_cell(self):
            tile = self.controller.tile
            sc = self.controller.screen
            x = self.x * tile
            y = self.y * tile
            pygame.draw.rect(sc, pygame.Color("darkgreen"), (x + 2, y + 2, tile - 2, tile - 2))

        def draw(self):
            x, y = self.x * self.controller.tile, self.y * self.controller.tile
            if self.visited:
                pygame.draw.rect(self.controller.screen, pygame.Color("darkgreen"),
                                 (x, y, self.controller.tile, self.controller.tile))
            if self.walls["top"]:
                pygame.draw.line(self.controller.screen, pygame.Color("white"), (x, y), (x + self.controller.tile, y),
                                 2)
            if self.walls["right"]:
                pygame.draw.line(self.controller.screen, pygame.Color("white"), (x + self.controller.tile, y),
                                 (x + self.controller.tile, y + self.controller.tile), 2)
            if self.walls["bottom"]:
                pygame.draw.line(self.controller.screen, pygame.Color("white"),
                                 (x + self.controller.tile, y + self.controller.tile), (x, y + self.controller.tile), 2)
            if self.walls["left"]:
                pygame.draw.line(self.controller.screen, pygame.Color("white"), (x, y + self.controller.tile), (x, y),
                                 2)
            if self.selected:
                color = pygame.Color("darkgreen") if not self.selected else pygame.Color("red")
                pygame.draw.rect(self.sc, color, (x + 2, y + 2, self.tile - 2, self.tile - 2))

        def check_neighbors(self):
            neighbors = []
            top = self.controller.check_cell(self.x, self.y - 1)
            right = self.controller.check_cell(self.x + 1, self.y)
            bottom = self.controller.check_cell(self.x, self.y + 1)
            left = self.controller.check_cell(self.x - 1, self.y)
            if top and not top.visited:
                neighbors.append(top)
            if right and not right.visited:
                neighbors.append(right)
            if bottom and not bottom.visited:
                neighbors.append(bottom)
            if left and not left.visited:
                neighbors.append(left)
            return choice(neighbors) if neighbors else False

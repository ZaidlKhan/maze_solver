class MazeSolver:
    def __init__(self, maze, controller):
        self.controller = controller
        self.maze = maze
        self.start = maze.start_point
        self.end = maze.end_point
        self.parent_map = {}
        self.path = []

    def solve(self):
        from collections import deque
        start_cell = self.maze.grid_cells[self.controller.find_index(*self.start)]
        queue = deque([start_cell])
        self.parent_map = {start_cell: None}

        while queue:
            current_cell = queue.popleft()

            if (current_cell.x, current_cell.y) == self.end:
                self.path = self.backtrack(current_cell)
                return self.path

            neighbors = self.get_neighbors(current_cell)

            for neighbor in neighbors:
                if neighbor not in self.parent_map:
                    queue.append(neighbor)
                    self.parent_map[neighbor] = current_cell

        return []

    def get_neighbors(self, current_cell):
        x = current_cell.x
        y = current_cell.y
        neighbors = []
        top = self.controller.check_cell(x, y - 1)
        right = self.controller.check_cell(x + 1, y)
        bottom = self.controller.check_cell(x, y + 1)
        left = self.controller.check_cell(x - 1, y)
        if top and not top.graph_visited and not current_cell.walls['top']:
            neighbors.append(top)
        if right and not right.graph_visited and not current_cell.walls['right']:
            neighbors.append(right)
        if bottom and not bottom.graph_visited and not current_cell.walls['bottom']:
            neighbors.append(bottom)
        if left and not left.graph_visited and not current_cell.walls['left']:
            neighbors.append(left)

        return neighbors

    def backtrack(self, end_cell):
        path = []
        while end_cell is not None:
            path.append(end_cell)
            end_cell = self.parent_map[end_cell]
        path.reverse()
        return [(cell.x, cell.y) for cell in path]
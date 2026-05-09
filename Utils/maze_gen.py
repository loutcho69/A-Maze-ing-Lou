import random
from .data import Dir


class MazeGenerator:
    opp = {Dir.N: Dir.S, Dir.S: Dir.N, Dir.E: Dir.W, Dir.W: Dir.E}
    DX = {Dir.E: 1, Dir.W: -1, Dir.N: 0, Dir.S: 0}
    DY = {Dir.E: 0, Dir.W: 0, Dir.N: -1, Dir.S: 1} 
    def __init__(self, width, height, entry, exit, perfect):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.path_solve = []
        self.is_path = False
        self.maze = self.create_maze()

    def create_maze(self):
        maze = [[15 for _ in range (self.width)]for _ in range(self.height)]
        is_visited = [[False for _ in range (self.width)] for _ in range(self.height)]
        x, y = self.entry

        def itinary(x, y, path) -> list:
            is_visited[y][x] = True
            path.append((x, y))
            if (x, y) == self.exit:
                self.path_solve = path.copy()
            direction = [Dir.N, Dir.E, Dir.S, Dir.W]
            random.shuffle(direction)
            for dirs in direction:
                next_x = x + self.DX[dirs]
                next_y = y + self.DY[dirs]
                if self.width > next_x >= 0 and self.height > next_y >= 0:
                    if not is_visited[next_y][next_x]:
                        maze[y][x] -= dirs.value
                        maze[next_y][next_x] -= self.opp[dirs].value
                        itinary(next_x, next_y, path)
            path.pop()
        itinary(x, y, [])
        return maze
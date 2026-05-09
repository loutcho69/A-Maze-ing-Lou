import random
from collections import deque
from .data import Dir
from .patterns import Pattern


class MazeGenerator:
    OPP = {Dir.N: Dir.S, Dir.S: Dir.N, Dir.E: Dir.W, Dir.W: Dir.E}
    DX = {Dir.E: 1, Dir.W: -1, Dir.N: 0, Dir.S: 0}
    DY = {Dir.E: 0, Dir.W: 0, Dir.N: -1, Dir.S: 1}
    ALL_DIRS = (Dir.N, Dir.E, Dir.S, Dir.W)

    def __init__(self, width, height, entry, exit, perfect, pattern=None):
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.pattern = pattern
        self.pattern_cells = self._compute_pattern_cells()
        self.path_solve = []
        self.is_path = False
        self.maze = self.create_maze()
        if not perfect:
            self._add_cycles(self.maze)
            self.path_solve = self._solve(self.maze)

    # --- pattern placement ---

    def _compute_pattern_cells(self):
        if self.pattern is None:
            return set()
        pw, ph = self.pattern.width, self.pattern.height
        if pw + 2 > self.width or ph + 2 > self.height:
            raise ValueError(
                f"Pattern '{self.pattern.name}' ({pw}x{ph}) doesn't fit in "
                f"maze ({self.width}x{self.height}). "
                f"Need at least {pw + 2}x{ph + 2}."
            )
        ox = (self.width - pw) // 2
        oy = (self.height - ph) // 2
        cells = {(ox + lx, oy + ly)
                 for (lx, ly) in self.pattern.closed_cells()}
        cells |= self._find_trapped_holes(ox, oy, cells)
        if self.entry in cells or self.exit in cells:
            raise ValueError(
                f"Pattern '{self.pattern.name}' overlaps entry or exit"
            )
        return cells

    def _find_trapped_holes(self, ox, oy, closed):
        pw, ph = self.pattern.width, self.pattern.height
        bbox = {(ox + lx, oy + ly)
                for ly in range(ph) for lx in range(pw)}
        empty = bbox - closed
        stack = [(x, y) for (x, y) in empty
                 if x in (ox, ox + pw - 1) or y in (oy, oy + ph - 1)]
        seen = set()
        while stack:
            x, y = stack.pop()
            if (x, y) in seen:
                continue
            seen.add((x, y))
            for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
                n = (x + dx, y + dy)
                if n in empty and n not in seen:
                    stack.append(n)
        return empty - seen

    # --- DFS Generation ---

    def create_maze(self):
        maze = [[15] * self.width for _ in range(self.height)]
        visited = [[False] * self.width for _ in range(self.height)]
        for (px, py) in self.pattern_cells:
            visited[py][px] = True

        def carve(x, y, path):
            visited[y][x] = True
            path.append((x, y))
            if (x, y) == self.exit:
                self.path_solve = path.copy()
            dirs = list(self.ALL_DIRS)
            random.shuffle(dirs)
            for d in dirs:
                nx, ny = x + self.DX[d], y + self.DY[d]
                if 0 <= nx < self.width and 0 <= ny < self.height \
                        and not visited[ny][nx]:
                    maze[y][x] -= d.value
                    maze[ny][nx] -= self.OPP[d].value
                    carve(nx, ny, path)
            path.pop()

        ex, ey = self.entry
        carve(ex, ey, [])
        if self.pattern_cells:
            self._reconnect(maze)
        return maze

    def _reconnect(self, maze):
        non_pat = {(x, y) for y in range(self.height)
                   for x in range(self.width)
                   if (x, y) not in self.pattern_cells}
        seen, components = set(), []
        for start in non_pat:
            if start in seen:
                continue
            comp, stack = set(), [start]
            while stack:
                x, y = stack.pop()
                if (x, y) in comp:
                    continue
                comp.add((x, y))
                c = maze[y][x]
                for d in self.ALL_DIRS:
                    if not (c & d.value):
                        nx, ny = x + self.DX[d], y + self.DY[d]
                        if (nx, ny) in non_pat and (nx, ny) not in comp:
                            stack.append((nx, ny))
            seen |= comp
            components.append(comp)
        if len(components) <= 1:
            return
        merged = next(c for c in components if self.entry in c).copy()
        for comp in components:
            if comp & merged:
                continue
            self._merge(maze, comp, merged)
            merged |= comp

    def _merge(self, maze, comp, merged):
        for (x, y) in comp:
            c = maze[y][x]
            for d in self.ALL_DIRS:
                if not (c & d.value):
                    continue
                nx, ny = x + self.DX[d], y + self.DY[d]
                if (0 <= nx < self.width and 0 <= ny < self.height
                        and (nx, ny) in merged
                        and (nx, ny) not in self.pattern_cells):
                    maze[y][x] -= d.value
                    maze[ny][nx] -= self.OPP[d].value
                    return

    # --- Non-Perfect Maze ---

    def _add_cycles(self, maze):
        candidates = []
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.pattern_cells:
                    continue
                c = maze[y][x]
                if (c & Dir.E.value) and x + 1 < self.width \
                        and (x + 1, y) not in self.pattern_cells:
                    candidates.append((x, y, Dir.E))
                if (c & Dir.S.value) and y + 1 < self.height \
                        and (x, y + 1) not in self.pattern_cells:
                    candidates.append((x, y, Dir.S))
        random.shuffle(candidates)
        target = len(candidates) * 15 // 100
        knocked = 0
        for (x, y, d) in candidates:
            if knocked >= target:
                break
            nx, ny = x + self.DX[d], y + self.DY[d]
            maze[y][x] -= d.value
            maze[ny][nx] -= self.OPP[d].value
            if self._creates_3x3(maze, x, y, nx, ny):
                maze[y][x] += d.value
                maze[ny][nx] += self.OPP[d].value
            else:
                knocked += 1

    def _creates_3x3(self, maze, ax, ay, bx, by):
        for cx, cy in self._nearby_3x3_centers(ax, ay, bx, by):
            if self._is_3x3_open(maze, cx, cy):
                return True
        return False

    def _nearby_3x3_centers(self, ax, ay, bx, by):
        seen = set()
        for (x, y) in ((ax, ay), (bx, by)):
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    cx, cy = x + dx, y + dy
                    if (cx, cy) in seen:
                        continue
                    if 1 <= cx <= self.width - 2 \
                            and 1 <= cy <= self.height - 2:
                        seen.add((cx, cy))
                        yield (cx, cy)

    def _is_3x3_open(self, maze, cx, cy):
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if (cx + dx, cy + dy) in self.pattern_cells:
                    return False
        for col in (-1, 0, 1):
            for row in (-1, 0):
                if maze[cy + row][cx + col] & Dir.S.value:
                    return False
        for row in (-1, 0, 1):
            for col in (-1, 0):
                if maze[cy + row][cx + col] & Dir.E.value:
                    return False
        return True

    def _solve(self, maze):
        parent = {self.entry: None}
        queue = deque([self.entry])
        while queue:
            x, y = queue.popleft()
            if (x, y) == self.exit:
                break
            c = maze[y][x]
            for d in self.ALL_DIRS:
                if c & d.value:
                    continue
                nx, ny = x + self.DX[d], y + self.DY[d]
                if not (0 <= nx < self.width and 0 <= ny < self.height):
                    continue
                if (nx, ny) in self.pattern_cells or (nx, ny) in parent:
                    continue
                parent[(nx, ny)] = (x, y)
                queue.append((nx, ny))
        if self.exit not in parent:
            return []
        path, cur = [], self.exit
        while cur is not None:
            path.append(cur)
            cur = parent[cur]
        return list(reversed(path))

    # --- Output File ---

    def _path_directions(self):
        letters = []
        moves = {(0, -1): 'N', (1, 0): 'E', (0, 1): 'S', (-1, 0): 'W'}
        for i in range(len(self.path_solve) - 1):
            x1, y1 = self.path_solve[i]
            x2, y2 = self.path_solve[i + 1]
            letters.append(moves.get((x2 - x1, y2 - y1), ''))
        return ''.join(letters)

    def to_output(self):
        rows = [''.join(f'{self.maze[y][x]:X}' for x in range(self.width))
                for y in range(self.height)]
        return '\n'.join(rows + [
            '',
            f'{self.entry[0]},{self.entry[1]}',
            f'{self.exit[0]},{self.exit[1]}',
            self._path_directions(),
        ]) + '\n'

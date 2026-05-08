import random
from collections import deque
from .data import Dir
from .patterns import Pattern


class MazeGenerator:
    opp = {Dir.N: Dir.S, Dir.S: Dir.N, Dir.E: Dir.W, Dir.W: Dir.E}
    DX = {Dir.E: 1, Dir.W: -1, Dir.N: 0, Dir.S: 0}
    DY = {Dir.E: 0, Dir.W: 0, Dir.N: -1, Dir.S: 1}

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
        # Non-perfect mode: open extra walls to create cycles, then
        # recompute the shortest path (the one captured during the DFS
        # is no longer guaranteed to be shortest once cycles exist).
        if not self.perfect:
            self._add_cycles(self.maze)
            self.path_solve = self._solve(self.maze)

    def create_maze(self):
        maze = [[15 for _ in range (self.width)]for _ in range(self.height)]
        is_visited = [[False for _ in range (self.width)] for _ in range(self.height)]
        # Mark pattern cells as already visited so the DFS skips them.
        for (px, py) in self.pattern_cells:
            is_visited[py][px] = True
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
        # If the pattern isolated some regions, reconnect them.
        if self.pattern_cells:
            self._ensure_connectivity(maze)
        return maze

    # ------------------------------------------------------------------ #
    # Helpers added for pattern support
    # ------------------------------------------------------------------ #
    def _compute_pattern_cells(self):
        """Place the pattern (if any) at the maze center.

        Returns the set of (x, y) maze cells that must stay closed.
        Raises ValueError if the pattern doesn't fit, or covers entry/exit.
        """
        if self.pattern is None:
            return set()
        pw, ph = self.pattern.width, self.pattern.height
        if pw + 2 > self.width or ph + 2 > self.height:
            raise ValueError(
                f"Pattern '{self.pattern.name}' ({pw}x{ph}) does not fit "
                f"in maze ({self.width}x{self.height}). "
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
        """Empty cells inside the pattern bbox unreachable from outside."""
        pw, ph = self.pattern.width, self.pattern.height
        bbox = {(ox + lx, oy + ly)
                for ly in range(ph) for lx in range(pw)}
        empty_in_bbox = bbox - closed
        from_outside = {
            (x, y) for (x, y) in empty_in_bbox
            if x == ox or x == ox + pw - 1
            or y == oy or y == oy + ph - 1
        }
        reachable = set()
        stack = list(from_outside)
        while stack:
            x, y = stack.pop()
            if (x, y) in reachable:
                continue
            reachable.add((x, y))
            for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
                n = (x + dx, y + dy)
                if n in empty_in_bbox and n not in reachable:
                    stack.append(n)
        return empty_in_bbox - reachable

    def _ensure_connectivity(self, maze):
        """Connect any region isolated by the embedded pattern."""
        non_pattern = {
            (x, y) for y in range(self.height) for x in range(self.width)
            if (x, y) not in self.pattern_cells
        }
        seen = set()
        components = []
        for start in non_pattern:
            if start in seen:
                continue
            comp = set()
            stack = [start]
            while stack:
                x, y = stack.pop()
                if (x, y) in comp:
                    continue
                comp.add((x, y))
                c = maze[y][x]
                for d in (Dir.N, Dir.E, Dir.S, Dir.W):
                    if not (c & d.value):
                        nx, ny = x + self.DX[d], y + self.DY[d]
                        if (nx, ny) in non_pattern and (nx, ny) not in comp:
                            stack.append((nx, ny))
            seen |= comp
            components.append(comp)
        if len(components) <= 1:
            return
        main = next(c for c in components if self.entry in c)
        merged = set(main)
        for comp in components:
            if comp is main:
                continue
            self._merge_component(maze, comp, merged)
            merged |= comp

    def _merge_component(self, maze, comp, merged):
        for (x, y) in comp:
            c = maze[y][x]
            for d in (Dir.N, Dir.E, Dir.S, Dir.W):
                if c & d.value:
                    nx, ny = x + self.DX[d], y + self.DY[d]
                    if (0 <= nx < self.width
                            and 0 <= ny < self.height
                            and (nx, ny) in merged
                            and (nx, ny) not in self.pattern_cells):
                        maze[y][x] -= d.value
                        maze[ny][nx] -= self.opp[d].value
                        return

    # ------------------------------------------------------------------ #
    # Helpers added for non-perfect mode
    # ------------------------------------------------------------------ #
    def _add_cycles(self, maze):
        """Knock down ~15% of removable interior walls to create cycles.

        Constraints:
        - never touch a wall of a pattern cell (they must stay closed)
        - never create a 3x3 fully-open area (subject rule IV.4)
        """
        candidates = []
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.pattern_cells:
                    continue
                c = maze[y][x]
                if (c & Dir.E.value) and x + 1 < self.width:
                    if (x + 1, y) not in self.pattern_cells:
                        candidates.append((x, y, Dir.E))
                if (c & Dir.S.value) and y + 1 < self.height:
                    if (x, y + 1) not in self.pattern_cells:
                        candidates.append((x, y, Dir.S))
        random.shuffle(candidates)
        target = len(candidates) * 15 // 100
        knocked = 0
        for (x, y, d) in candidates:
            if knocked >= target:
                break
            nx, ny = x + self.DX[d], y + self.DY[d]
            maze[y][x] -= d.value
            maze[ny][nx] -= self.opp[d].value
            if self._creates_open_3x3(maze, x, y, nx, ny):
                maze[y][x] += d.value
                maze[ny][nx] += self.opp[d].value
            else:
                knocked += 1

    def _creates_open_3x3(self, maze, ax, ay, bx, by):
        """Check whether removing a wall created a 3x3 open area near
        the modified cells."""
        candidates = set()
        for (x, y) in ((ax, ay), (bx, by)):
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    cx, cy = x + dx, y + dy
                    if (1 <= cx <= self.width - 2
                            and 1 <= cy <= self.height - 2):
                        candidates.add((cx, cy))
        for (cx, cy) in candidates:
            if self._is_open_3x3(maze, cx, cy):
                return True
        return False

    def _is_open_3x3(self, maze, cx, cy):
        """True if the 3x3 area centered at (cx, cy) is fully open."""
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
        """BFS from entry to exit. Returns the shortest path (list of
        cells). Used in non-perfect mode where the DFS-captured path
        is no longer guaranteed shortest."""
        parent = {self.entry: None}
        queue = deque([self.entry])
        while queue:
            x, y = queue.popleft()
            if (x, y) == self.exit:
                break
            c = maze[y][x]
            for d in (Dir.N, Dir.E, Dir.S, Dir.W):
                if c & d.value:
                    continue
                nx, ny = x + self.DX[d], y + self.DY[d]
                if not (0 <= nx < self.width and 0 <= ny < self.height):
                    continue
                if (nx, ny) in self.pattern_cells:
                    continue
                if (nx, ny) in parent:
                    continue
                parent[(nx, ny)] = (x, y)
                queue.append((nx, ny))
        if self.exit not in parent:
            return []
        path = []
        cur = self.exit
        while cur is not None:
            path.append(cur)
            cur = parent[cur]
        path.reverse()
        return path

    # ------------------------------------------------------------------ #
    # Output file format (subject IV.5)
    # ------------------------------------------------------------------ #
    def _path_to_directions(self):
        """Convert path_solve (list of cells) into a string of N/E/S/W
        letters describing the moves taken from entry to exit.

        For each consecutive pair of cells in the path, determine the
        cardinal direction from the first to the second.
        """
        letters = []
        for i in range(len(self.path_solve) - 1):
            x1, y1 = self.path_solve[i]
            x2, y2 = self.path_solve[i + 1]
            dx = x2 - x1
            dy = y2 - y1
            if dx == 0 and dy == -1:
                letters.append('N')
            elif dx == 1 and dy == 0:
                letters.append('E')
            elif dx == 0 and dy == 1:
                letters.append('S')
            elif dx == -1 and dy == 0:
                letters.append('W')
            # If two consecutive cells aren't adjacent, the path is
            # malformed; we silently skip (shouldn't happen with BFS).
        return ''.join(letters)

    def to_output(self):
        """Format the maze for the output file as specified in IV.5.

        - One hex digit per cell, encoded as bit 0=N, 1=E, 2=S, 3=W
          (bit set = wall closed). Our internal cell values use the
          exact same encoding, so we just hex() each value.
        - Cells stored row by row, one row per line.
        - Blank line.
        - Entry coordinates "x,y".
        - Exit coordinates "x,y".
        - Shortest path as a string of N/E/S/W letters.
        - Every line ends with '\\n'.
        """
        lines = []
        for y in range(self.height):
            row = ''.join(f'{self.maze[y][x]:X}' for x in range(self.width))
            lines.append(row)
        lines.append('')  # blank line separator
        lines.append(f'{self.entry[0]},{self.entry[1]}')
        lines.append(f'{self.exit[0]},{self.exit[1]}')
        lines.append(self._path_to_directions())
        # Trailing newline on every line, including the last.
        return '\n'.join(lines) + '\n'

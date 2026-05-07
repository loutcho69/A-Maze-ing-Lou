import random
from .data import Dir
from .patterns import Pattern


class PatternTooLargeError(Exception):
    """Raised when the requested pattern does not fit inside the maze."""
    pass


class PatternOverlapsEntryExitError(Exception):
    """Raised when the centered pattern would cover entry or exit cell."""
    pass


class MazeGenerator:
    """Generate a 2D maze using randomized DFS (recursive backtracker).

    Each cell is encoded as a 4-bit integer where each bit represents a
    closed wall: bit 0 = N, bit 1 = E, bit 2 = S, bit 3 = W.
    A cell starts at 15 (all walls closed). When a wall is removed during
    generation, the corresponding bit is cleared on both adjacent cells.

    A Pattern can be embedded at the maze center. Pattern cells are kept
    fully closed (value 15) and the DFS routes around them.
    """

    opp = {Dir.N: Dir.S, Dir.S: Dir.N, Dir.E: Dir.W, Dir.W: Dir.E}
    DX = {Dir.E: 1, Dir.W: -1, Dir.N: 0, Dir.S: 0}
    DY = {Dir.E: 0, Dir.W: 0, Dir.N: -1, Dir.S: 1}

    def __init__(
        self,
        width: int,
        height: int,
        entry: tuple[int, int],
        exit: tuple[int, int],
        perfect: bool,
        pattern: Pattern | None = None,
        seed: int | None = None,
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.pattern = pattern
        # Local RNG: seeded for reproducibility, or unseeded for random.
        # Using a local Random instance instead of the global random
        # module avoids polluting global state.
        self._rng = random.Random(seed)
        self.path_solve: list[tuple[int, int]] = []
        self.is_path = False
        # Cells (in maze coordinates) that belong to the pattern.
        self.pattern_cells: set[tuple[int, int]] = self._compute_pattern_cells()
        self.maze = self.create_maze()

    # ------------------------------------------------------------------ #
    # Pattern placement
    # ------------------------------------------------------------------ #
    def _compute_pattern_cells(self) -> set[tuple[int, int]]:
        """Compute the set of maze cells covered by the centered pattern.

        Returns an empty set if no pattern is set.

        Raises:
            PatternTooLargeError: if pattern + 1-cell margin does not fit.
            PatternOverlapsEntryExitError: if entry or exit falls inside.
        """
        if self.pattern is None:
            return set()

        pw, ph = self.pattern.width, self.pattern.height
        # Need at least one cell of margin on every side so the DFS
        # can route around the pattern without isolating cells.
        if pw + 2 > self.width or ph + 2 > self.height:
            raise PatternTooLargeError(
                f"Pattern '{self.pattern.name}' "
                f"({pw}x{ph}) does not fit in maze "
                f"({self.width}x{self.height}). "
                f"Need at least {pw + 2}x{ph + 2}."
            )

        # Top-left corner of the pattern, centered.
        ox = (self.width - pw) // 2
        oy = (self.height - ph) // 2

        cells = {
            (ox + lx, oy + ly)
            for (lx, ly) in self.pattern.closed_cells()
        }

        # Cells that are 0 in the pattern grid but completely surrounded
        # by closed cells inside the pattern bounding box would otherwise
        # be unreachable. Include them in the closed set.
        cells |= self._find_trapped_holes(ox, oy, cells)

        if self.entry in cells or self.exit in cells:
            raise PatternOverlapsEntryExitError(
                f"Pattern '{self.pattern.name}' overlaps "
                f"entry {self.entry} or exit {self.exit}."
            )

        return cells

    def _find_trapped_holes(
        self,
        ox: int,
        oy: int,
        closed: set[tuple[int, int]],
    ) -> set[tuple[int, int]]:
        """Find empty cells inside the pattern bounding box that are
        unreachable from outside the pattern (because they are fully
        enclosed by closed cells).

        We do a flood fill from the bounding-box border, only on cells
        that are 0 in the pattern. Anything inside the bbox that is 0
        but not reached is a trapped hole.
        """
        assert self.pattern is not None
        pw, ph = self.pattern.width, self.pattern.height
        # All cells inside the bounding box (in maze coordinates).
        bbox = {
            (ox + lx, oy + ly)
            for ly in range(ph)
            for lx in range(pw)
        }
        empty_in_bbox = bbox - closed

        # Starting points: empty cells on the bbox border.
        from_outside: set[tuple[int, int]] = set()
        for (x, y) in empty_in_bbox:
            if x == ox or x == ox + pw - 1 or y == oy or y == oy + ph - 1:
                from_outside.add((x, y))

        # Flood fill among empty cells inside the bbox.
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

    # ------------------------------------------------------------------ #
    # Maze generation
    # ------------------------------------------------------------------ #
    def create_maze(self) -> list[list[int]]:
        """Run the randomized DFS and return the maze grid.

        After the DFS, isolated regions (caused by the pattern) are
        reconnected, and the shortest path from entry to exit is
        computed via BFS.
        """
        maze = [[15 for _ in range(self.width)] for _ in range(self.height)]
        is_visited = [
            [False for _ in range(self.width)] for _ in range(self.height)
        ]
        # Mark pattern cells as already visited so the DFS skips them
        # and never breaks any of their walls.
        for (px, py) in self.pattern_cells:
            is_visited[py][px] = True

        x, y = self.entry

        def itinary(x: int, y: int) -> None:
            is_visited[y][x] = True
            direction = [Dir.N, Dir.E, Dir.S, Dir.W]
            self._rng.shuffle(direction)
            for dirs in direction:
                next_x = x + self.DX[dirs]
                next_y = y + self.DY[dirs]
                if self.width > next_x >= 0 and self.height > next_y >= 0:
                    if not is_visited[next_y][next_x]:
                        maze[y][x] -= dirs.value
                        maze[next_y][next_x] -= self.opp[dirs].value
                        itinary(next_x, next_y)

        itinary(x, y)
        self._ensure_connectivity(maze)
        if not self.perfect:
            self._carve_extra_passages(maze)
        self.path_solve = self._compute_shortest_path(maze)
        return maze

    # ------------------------------------------------------------------ #
    # Connectivity repair (needed when a pattern blocks the DFS)
    # ------------------------------------------------------------------ #
    def _ensure_connectivity(self, maze: list[list[int]]) -> None:
        """Connect any region isolated by the embedded pattern.

        The DFS may leave entire regions unreachable when it is forced
        to route around a large pattern. This pass finds each connected
        component (excluding pattern cells) and breaks one wall to merge
        it with the main component containing the entry.
        """
        if not self.pattern_cells:
            return

        non_pattern = {
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if (x, y) not in self.pattern_cells
        }

        # Find connected components by walking through open passages.
        seen: set[tuple[int, int]] = set()
        components: list[set[tuple[int, int]]] = []
        for start in non_pattern:
            if start in seen:
                continue
            comp: set[tuple[int, int]] = set()
            stack = [start]
            while stack:
                x, y = stack.pop()
                if (x, y) in comp:
                    continue
                comp.add((x, y))
                c = maze[y][x]
                for d in (Dir.N, Dir.E, Dir.S, Dir.W):
                    if not (c & d.value):  # wall is open
                        nx = x + self.DX[d]
                        ny = y + self.DY[d]
                        if (nx, ny) in non_pattern and (nx, ny) not in comp:
                            stack.append((nx, ny))
            seen |= comp
            components.append(comp)

        if len(components) <= 1:
            return

        # Identify the main component (the one containing the entry).
        main = next(c for c in components if self.entry in c)
        others = [c for c in components if c is not main]

        # For each isolated component, find a wall to break that touches
        # the main component (or any already-merged component).
        merged = set(main)
        for comp in others:
            self._merge_component(maze, comp, merged)
            merged |= comp

    def _merge_component(
        self,
        maze: list[list[int]],
        comp: set[tuple[int, int]],
        merged: set[tuple[int, int]],
    ) -> None:
        """Break one wall to connect `comp` to the `merged` set."""
        for (x, y) in comp:
            c = maze[y][x]
            for d in (Dir.N, Dir.E, Dir.S, Dir.W):
                if c & d.value:  # wall is closed
                    nx = x + self.DX[d]
                    ny = y + self.DY[d]
                    if (
                        0 <= nx < self.width
                        and 0 <= ny < self.height
                        and (nx, ny) in merged
                        and (nx, ny) not in self.pattern_cells
                    ):
                        maze[y][x] -= d.value
                        maze[ny][nx] -= self.opp[d].value
                        return

    # ------------------------------------------------------------------ #
    # Non-perfect mode: carve extra passages while avoiding 3x3 open areas
    # ------------------------------------------------------------------ #
    def _carve_extra_passages(self, maze: list[list[int]]) -> None:
        """Open additional walls to create cycles (non-perfect maze).

        For each interior wall between two non-pattern cells, with a
        certain probability, remove the wall — but only if doing so
        does not produce a 3x3 fully open area.

        The probability is tuned to give a noticeable difference from
        the perfect maze without flooding the maze with open spaces.
        """
        # Build the list of interior walls. Each wall is identified by
        # the cell it belongs to and a direction (we only consider E and S
        # to avoid counting each wall twice).
        candidates: list[tuple[int, int, Dir]] = []
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.pattern_cells:
                    continue
                c = maze[y][x]
                # East wall (between (x,y) and (x+1,y))
                if (c & Dir.E.value) and x + 1 < self.width:
                    if (x + 1, y) not in self.pattern_cells:
                        candidates.append((x, y, Dir.E))
                # South wall (between (x,y) and (x,y+1))
                if (c & Dir.S.value) and y + 1 < self.height:
                    if (x, y + 1) not in self.pattern_cells:
                        candidates.append((x, y, Dir.S))

        self._rng.shuffle(candidates)
        # ~20% of removable walls are knocked down. Tuned by feel:
        # high enough to make the maze visibly non-perfect, low enough
        # to keep it interesting and avoid trivial paths.
        target = len(candidates) // 5

        knocked = 0
        for (x, y, d) in candidates:
            if knocked >= target:
                break
            nx = x + self.DX[d]
            ny = y + self.DY[d]
            # Tentatively open the wall and see if it creates a 3x3 area.
            maze[y][x] -= d.value
            maze[ny][nx] -= self.opp[d].value
            if self._creates_open_3x3(maze, x, y, nx, ny):
                # Revert the change.
                maze[y][x] += d.value
                maze[ny][nx] += self.opp[d].value
            else:
                knocked += 1

    def _creates_open_3x3(
        self,
        maze: list[list[int]],
        ax: int, ay: int,
        bx: int, by: int,
    ) -> bool:
        """Check whether removing the wall between (ax,ay) and (bx,by)
        creates any fully-open 3x3 area in the maze.

        A 3x3 area centered at (cx, cy) is fully open iff all 12 internal
        walls between its 9 cells are open. Only check 3x3 boxes that
        actually contain at least one of the two affected cells.
        """
        # The two cells whose neighborhood may have changed.
        affected = ((ax, ay), (bx, by))
        # All 3x3 box centers (cx, cy) such that the 3x3 box covers
        # at least one affected cell. The box covers cells from
        # (cx-1, cy-1) to (cx+1, cy+1).
        candidates = set()
        for (x, y) in affected:
            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    cx, cy = x + dx, y + dy
                    # Bounds: a 3x3 box requires 1 <= cx <= W-2.
                    if 1 <= cx <= self.width - 2 \
                            and 1 <= cy <= self.height - 2:
                        candidates.add((cx, cy))

        for (cx, cy) in candidates:
            if self._is_open_3x3(maze, cx, cy):
                return True
        return False

    def _is_open_3x3(
        self,
        maze: list[list[int]],
        cx: int,
        cy: int,
    ) -> bool:
        """True if the 3x3 area centered at (cx, cy) is fully open
        (all 12 internal walls between its 9 cells are open)."""
        # The 9 cells of the box.
        # Any pattern cell in the box disqualifies it (pattern cells
        # have all walls closed by definition, so they cannot be part
        # of an open area).
        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if (cx + dx, cy + dy) in self.pattern_cells:
                    return False

        # 6 horizontal internal walls: between rows.
        # For each (col in {-1,0,1}, row pair), check south wall of upper.
        for col in (-1, 0, 1):
            for row in (-1, 0):
                upper_y = cy + row
                upper_x = cx + col
                if maze[upper_y][upper_x] & Dir.S.value:
                    return False

        # 6 vertical internal walls: between columns.
        for row in (-1, 0, 1):
            for col in (-1, 0):
                left_x = cx + col
                left_y = cy + row
                if maze[left_y][left_x] & Dir.E.value:
                    return False

        return True

    # ------------------------------------------------------------------ #
    # Shortest path (BFS)
    # ------------------------------------------------------------------ #
    def _compute_shortest_path(
        self,
        maze: list[list[int]],
    ) -> list[tuple[int, int]]:
        """Compute the shortest path from entry to exit using BFS.

        BFS on an unweighted grid graph guarantees the shortest path
        in number of cells. Walks only through open passages, never
        through pattern cells.

        Returns:
            The list of cells from entry to exit, inclusive. Empty if
            the exit is unreachable (should not happen after
            connectivity repair).
        """
        from collections import deque

        # parent[(x, y)] = previous cell on the shortest path
        parent: dict[tuple[int, int], tuple[int, int] | None] = {
            self.entry: None
        }
        queue: deque[tuple[int, int]] = deque([self.entry])

        while queue:
            x, y = queue.popleft()
            if (x, y) == self.exit:
                break
            c = maze[y][x]
            for d in (Dir.N, Dir.E, Dir.S, Dir.W):
                if c & d.value:  # wall is closed
                    continue
                nx = x + self.DX[d]
                ny = y + self.DY[d]
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

        # Reconstruct the path by walking backwards from exit to entry.
        path: list[tuple[int, int]] = []
        cur: tuple[int, int] | None = self.exit
        while cur is not None:
            path.append(cur)
            cur = parent[cur]
        path.reverse()
        return path


def maze_gen(
    setting,
    pattern: Pattern | None = None,
    seed: int | None = None,
):
    """Build a MazeGenerator from a parsed settings object.

    Args:
        setting: Parsed config (must have WIDTH, HEIGHT, ENTRY, EXIT, PERFECT,
            and optionally SEED).
        pattern: Optional Pattern to embed at the center of the maze.
        seed: Optional override for the seed. If None, falls back to
            setting.SEED. If both are None, the maze is fully random.

    Returns:
        A MazeGenerator instance, or None on failure (after printing the error).
    """
    if seed is None:
        seed = getattr(setting, 'SEED', None)
    try:
        maze = MazeGenerator(
            setting.WIDTH,
            setting.HEIGHT,
            setting.ENTRY,
            setting.EXIT,
            setting.PERFECT,
            pattern=pattern,
            seed=seed,
        )
    except (PatternTooLargeError, PatternOverlapsEntryExitError) as err:
        print(f"Pattern error: {err}")
        return None
    except Exception as err:
        print(f"Missing or invalid value in config: {err}")
        return None
    return maze

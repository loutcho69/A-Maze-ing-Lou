from .data import Dir


# Dark grey block used for inner-cell empty space.
DARK = '\033[38;5;235m█\033[0m'
# Light shade used when displaying the solution path.
PATH_CHAR = '░'
# Entry marker (green) and exit marker (red).
ENTRY_CHAR = '\033[32m█\033[0m'
EXIT_CHAR = '\033[31m█\033[0m'


def print_title() -> None:
    """Print the ASCII title and the interactive menu."""
    amazing_art = r"""
  █████╗ ███╗   ███╗  █████╗ ███████╗ ██╗███╗   ██╗  ██████╗
 ██╔══██╗████╗ ████║ ██╔══██╗╚══███╔╝ ██║████╗  ██║ ██╔════╝
 ███████║██╔████╔██║ ███████║  ███╔╝  ██║██╔██╗ ██║ ██║  ███╗
 ██╔══██║██║╚██╔╝██║ ██╔══██║ ███╔╝   ██║██║╚██╗██║ ██║   ██║
 ██║  ██║██║ ╚═╝ ██║ ██║  ██║███████╗ ██║██║ ╚████║ ╚██████╔╝
 ╚═╝  ╚═╝╚═╝     ╚═╝ ╚═╝  ╚═╝╚══════╝ ╚═╝╚═╝  ╚═══╝  ╚═════╝
"""
    print(f"\n{amazing_art}")
    print("                   A _ M A Z E _ I N G\n")
    print('1. Generate a new maze', end='   ')
    print('2. Show/hide path from entry to exit')
    print('3. Rotate maze colors', end='    ')
    print('4. Change pattern')
    print('5. Change pattern color', end='  ')
    print('6. Quit\n')


def _is_pattern(maze, x: int, y: int) -> bool:
    """True if (x, y) is inside the embedded pattern."""
    if not (0 <= x < maze.width and 0 <= y < maze.height):
        return False
    return (x, y) in maze.pattern_cells


def _wall_color(maze, a: tuple[int, int], b: tuple[int, int],
                wall_color: str, pattern_color: str) -> str:
    """Pick the color for a wall between two cells.

    A wall is colored as pattern if at least one of the two cells
    belongs to the pattern. Cells outside the maze count as non-pattern.
    """
    if _is_pattern(maze, *a) or _is_pattern(maze, *b):
        return pattern_color
    return wall_color


def _cell_inside(maze, x: int, y: int, pattern_color: str) -> str:
    """Render the inside of a cell (entry/exit/path/empty/pattern)."""
    if (x, y) == maze.entry:
        return ENTRY_CHAR
    if (x, y) == maze.exit:
        return EXIT_CHAR
    if _is_pattern(maze, x, y):
        return pattern_color
    if (x, y) in maze.path_solve and maze.is_path:
        return PATH_CHAR
    return DARK


def _path_edges(maze) -> set[frozenset[tuple[int, int]]]:
    """Build the set of consecutive cell-pairs along the solution path.

    Each pair is stored as a frozenset so that order does not matter
    when looking up an edge between two cells.
    """
    if not maze.is_path:
        return set()
    edges: set[frozenset[tuple[int, int]]] = set()
    p = maze.path_solve
    for i in range(len(p) - 1):
        edges.add(frozenset((p[i], p[i + 1])))
    return edges


def print_maze(maze, color: str, pattern_color: str | None = None) -> None:
    """Render the maze to stdout using ANSI block characters.

    Args:
        maze: a MazeGenerator instance.
        color: ANSI block character used for normal walls.
        pattern_color: optional ANSI block char used for pattern cells
            and their walls. Defaults to the same as `color`.
    """
    if pattern_color is None:
        pattern_color = color

    # An open passage between two cells is highlighted as path only
    # when those two cells are consecutive in the solution path.
    edges = _path_edges(maze)

    line_bottom = ''
    for y in range(maze.height):
        line0 = ''  # top line of the row (north walls + nw corners)
        line1 = ''  # bottom line of the row (west walls + cell interiors)

        for x in range(maze.width):
            c = maze.maze[y][x]
            n_closed = bool(c & Dir.N.value)
            w_closed = bool(c & Dir.W.value)

            # --- line0, first char: north-west corner ---
            if n_closed or w_closed:
                # The corner exists. Pick pattern color if any of the
                # four cells touching this corner is part of the pattern.
                neighbors = [(x, y), (x - 1, y), (x, y - 1), (x - 1, y - 1)]
                if any(_is_pattern(maze, nx, ny) for (nx, ny) in neighbors):
                    line0 += pattern_color
                else:
                    line0 += color
            else:
                # No N nor W wall: this corner is empty space. It only
                # belongs to the path if both diagonal neighbors are on
                # the path AND adjacent in the path -- but a corner
                # never sits on a single edge of the path, so we just
                # render dark space here.
                line0 += DARK

            # --- line0, second char: north wall of this cell ---
            if n_closed:
                line0 += _wall_color(maze, (x, y), (x, y - 1),
                                     color, pattern_color)
            else:
                # N wall is open: it's part of the path only if the
                # edge between (x, y) and (x, y-1) is on the path.
                if frozenset(((x, y), (x, y - 1))) in edges:
                    line0 += PATH_CHAR
                else:
                    line0 += DARK

            # --- line1, first char: west wall of this cell ---
            if w_closed:
                line1 += _wall_color(maze, (x, y), (x - 1, y),
                                     color, pattern_color)
            else:
                # W wall is open: same logic, check the edge.
                if frozenset(((x, y), (x - 1, y))) in edges:
                    line1 += PATH_CHAR
                else:
                    line1 += DARK

            # --- line1, second char: cell interior ---
            line1 += _cell_inside(maze, x, y, pattern_color)

            # --- right border (east wall of last column) ---
            if x == maze.width - 1:
                # Top-right corner.
                if any(_is_pattern(maze, nx, ny)
                       for (nx, ny) in [(x, y), (x, y - 1)]):
                    line0 += pattern_color
                else:
                    line0 += color
                # East wall of the cell.
                if _is_pattern(maze, x, y):
                    line1 += pattern_color
                else:
                    line1 += color

            # --- bottom border (south wall of last row) ---
            if y == maze.height - 1:
                if _is_pattern(maze, x, y):
                    line_bottom += pattern_color * 2
                else:
                    line_bottom += color * 2

        print(line0)
        print(line1)

    # Bottom border closing corner (right edge).
    line_bottom += color
    print(line_bottom)
    print_title()

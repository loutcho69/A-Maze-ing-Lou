from .data import Dir

# ANSI block characters for cell rendering.
ENTRY = '\033[32m█\033[0m'   # green
EXIT = '\033[31m█\033[0m'    # red
DARK = '\033[38;5;235m█\033[0m'
PATH = '░'

_TITLE = r"""
  █████╗ ███╗   ███╗  █████╗ ███████╗ ██╗███╗   ██╗  ██████╗
 ██╔══██╗████╗ ████║ ██╔══██╗╚══███╔╝ ██║████╗  ██║ ██╔════╝
 ███████║██╔████╔██║ ███████║  ███╔╝  ██║██╔██╗ ██║ ██║  ███╗
 ██╔══██║██║╚██╔╝██║ ██╔══██║ ███╔╝   ██║██║╚██╗██║ ██║   ██║
 ██║  ██║██║ ╚═╝ ██║ ██║  ██║███████╗ ██║██║ ╚████║ ╚██████╔╝
 ╚═╝  ╚═╝╚═╝     ╚═╝ ╚═╝  ╚═╝╚══════╝ ╚═╝╚═╝  ╚═══╝  ╚═════╝
"""


def print_title():
    print(f"\n{_TITLE}")
    print("                   A _ M A Z E _ I N G\n")
    print('1. Generate a new maze', end='   ')
    print('2. Show/hide path from entry to exit')
    print('3. Rotate maze colors', end='    ')
    print('4. Change pattern')
    print('5. Change pattern color', end='  ')
    print('6. Quit\n')


def _cell(x, y, maze, pat_color):
    """Char to render at the bottom-right of cell (x, y)."""
    if (x, y) == maze.entry: return ENTRY
    if (x, y) == maze.exit: return EXIT
    if (x, y) in maze.pattern_cells: return pat_color
    if (x, y) in maze.path_solve and maze.is_path: return PATH
    return DARK


def _on_path(x, y, maze):
    """Char for an open passage at (x, y): path mark or dark."""
    if (x, y) in maze.path_solve and maze.is_path:
        return PATH
    return DARK


def _wcol(maze, color, pat_color, *cells):
    """Pick pat_color if any of cells is in the pattern, else color."""
    for (cx, cy) in cells:
        if 0 <= cx < maze.width and 0 <= cy < maze.height \
                and (cx, cy) in maze.pattern_cells:
            return pat_color
    return color


def print_maze(maze, color, pattern_color=None):
    """Render the maze. pattern_color defaults to color (so without a
    pattern, rendering is identical to the original code)."""
    if pattern_color is None:
        pattern_color = color

    line_bottom = ''
    for y in range(maze.height):
        line0 = ''
        line1 = ''
        for x in range(maze.width):
            c = maze.maze[y][x]
            # NW corner color: among the 4 cells touching it.
            nw = _wcol(maze, color, pattern_color,
                       (x, y), (x - 1, y), (x, y - 1), (x - 1, y - 1))
            ncol = _wcol(maze, color, pattern_color, (x, y), (x, y - 1))
            wcol = _wcol(maze, color, pattern_color, (x, y), (x - 1, y))
            cell = _cell(x, y, maze, pattern_color)

            n_closed = c & Dir.N.value
            w_closed = c & Dir.W.value

            # line0: NW corner + (N wall or open passage above)
            line0 += nw
            line0 += ncol if n_closed else _on_path(x, y - 1, maze)

            # line1: (W wall or open passage left) + cell content
            line1 += wcol if w_closed else _on_path(x - 1, y, maze)
            line1 += cell

            # Right border on the last column.
            if x == maze.width - 1:
                line0 += _wcol(maze, color, pattern_color,
                               (x, y), (x, y - 1))
                line1 += _wcol(maze, color, pattern_color, (x, y))
            # Bottom border on the last row.
            if y == maze.height - 1:
                bcol = pattern_color \
                    if (x, y) in getattr(maze, 'pattern_cells', set()) \
                    else color
                line_bottom += bcol * 2
        print(line0)
        print(line1)
    line_bottom += color
    print(line_bottom)

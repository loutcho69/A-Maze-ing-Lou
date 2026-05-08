from .data import Dir


def print_title():
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


def check_entry(x, y, maze):
    if (x, y) == maze.entry:
        return '\033[32m█\033[0m'
    elif (x, y) == maze.exit:
        return '\033[31m█\033[0m'
    elif (x, y) in maze.path_solve and maze.is_path:
        return '░'
    return '\033[38;5;235m█\033[0m'


def check_path(x, y, maze):
    if (x, y) in maze.path_solve and maze.is_path:
        return '░'
    return '\033[38;5;235m█\033[0m'


def _is_pattern(maze, x, y):
    """True if (x, y) is in the maze and belongs to the pattern."""
    if not (0 <= x < maze.width and 0 <= y < maze.height):
        return False
    return (x, y) in maze.pattern_cells


def _wall_color(maze, color, pattern_color, *cells):
    """Return pattern_color if any of the given cells is in the pattern,
    else the regular wall color. cells is a list of (x, y) tuples."""
    for (x, y) in cells:
        if _is_pattern(maze, x, y):
            return pattern_color
    return color


def _cell_inside(x, y, maze, pattern_color):
    """Same as check_entry but renders pattern cells in pattern_color."""
    if (x, y) == maze.entry:
        return '\033[32m█\033[0m'
    elif (x, y) == maze.exit:
        return '\033[31m█\033[0m'
    elif _is_pattern(maze, x, y):
        return pattern_color
    elif (x, y) in maze.path_solve and maze.is_path:
        return '░'
    return '\033[38;5;235m█\033[0m'


def print_maze(maze, color, pattern_color=None) -> None:
    """Render the maze. pattern_color is optional and defaults to color
    (so without a pattern, rendering is identical to the original)."""
    if pattern_color is None:
        pattern_color = color
    has_pattern = bool(getattr(maze, 'pattern_cells', None))

    line_bottom = ''
    for y in range(maze.height):
        line0 = ''
        line1 = ''
        for x in range(maze.width):
            c = maze.maze[y][x]
            # Pick wall colors for this cell. When no pattern, the
            # color logic below collapses to the original behaviour
            # because pattern_color == color.
            if has_pattern:
                # NW corner: any of the 4 cells touching the corner.
                nw_col = _wall_color(
                    maze, color, pattern_color,
                    (x, y), (x - 1, y), (x, y - 1), (x - 1, y - 1)
                )
                # N wall: between (x,y) and (x, y-1).
                n_col = _wall_color(
                    maze, color, pattern_color, (x, y), (x, y - 1)
                )
                # W wall: between (x,y) and (x-1, y).
                w_col = _wall_color(
                    maze, color, pattern_color, (x, y), (x - 1, y)
                )
                cell_char = _cell_inside(x, y, maze, pattern_color)
            else:
                nw_col = color
                n_col = color
                w_col = color
                cell_char = check_entry(x, y, maze)

            if (c & Dir.N.value) and (c & Dir.W.value):
                line0 += f'{nw_col}{n_col}'
                line1 += f'{w_col}'
                line1 += cell_char
            elif (c & Dir.N.value) and not (c & Dir.W.value):
                line0 += f'{nw_col}{n_col}'
                if (x - 1, y) in maze.path_solve:
                    line1 += check_path(x, y, maze)
                else:
                    line1 += '\033[38;5;235m█\033[0m'
                line1 += cell_char
            elif (c & Dir.W.value) and not (c & Dir.N.value):
                line0 += f'{nw_col}'
                if (x, y - 1) in maze.path_solve:
                    line0 += check_path(x, y, maze)
                else:
                    line0 += '\033[38;5;235m█\033[0m'
                line1 += f'{w_col}' + cell_char
            elif not (c & Dir.N.value) and not (c & Dir.W.value):
                line0 += f'{nw_col}'
                if (x, y - 1) in maze.path_solve:
                    line0 += check_path(x, y, maze)
                else:
                    line0 += '\033[38;5;235m█\033[0m'
                if (x - 1, y) in maze.path_solve:
                    line1 += check_path(x, y, maze)
                else:
                    line1 += '\033[38;5;235m█\033[0m'
                line1 += cell_char

            if x == maze.width - 1:
                # Right border: top corner + east wall.
                if has_pattern:
                    ne_col = _wall_color(
                        maze, color, pattern_color, (x, y), (x, y - 1)
                    )
                    e_col = _wall_color(
                        maze, color, pattern_color, (x, y)
                    )
                else:
                    ne_col = color
                    e_col = color
                line0 += f'{ne_col}'
                line1 += f'{e_col}'
            if y == maze.height - 1:
                if has_pattern and _is_pattern(maze, x, y):
                    line_bottom += f'{pattern_color}{pattern_color}'
                else:
                    line_bottom += f'{color}{color}'
        print(f"{line0}")
        print(f"{line1}")
    line_bottom += f'{color}'
    print(f"{line_bottom}")

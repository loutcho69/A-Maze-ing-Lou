from typing import Any
from .data import Dir


# mypy R8: -> None for procedures that don't return
def print_title() -> None:
    amazing_art = r"""
  █████╗ ███╗   ███╗  █████╗ ███████╗ ██╗███╗   ██╗  ██████╗
 ██╔══██╗████╗ ████║ ██╔══██╗╚══███╔╝ ██║████╗  ██║ ██╔════╝
 ███████║██╔████╔██║ ███████║  ███╔╝  ██║██╔██╗ ██║ ██║  ███╗
 ██╔══██║██║╚██╔╝██║ ██╔══██║ ███╔╝   ██║██║╚██╗██║ ██║   ██║
 ██║  ██║██║ ╚═╝ ██║ ██║  ██║███████╗ ██║██║ ╚████║ ╚██████╔╝
 ╚═╝  ╚═╝╚═╝     ╚═╝ ╚═╝  ╚═╝╚══════╝ ╚═╝╚═╝  ╚═══╝  ╚═════╝
"""
    print(f"\n{amazing_art}")


def print_menu() -> None:
    print("                   A _ M A Z E _ I N G\n")
    print('1. Generate a new maze', end='   ')
    print('2. Show/hide path from entry to exit')
    print('3. Rotate maze colors', end='    ')
    print('4. Generate with other pattern')
    print('5. Rotate pattern color', end='  ')
    print('6. Quit\n')


# mypy R8: 'maze' typed as Any to avoid circular import with MazeGenerator
def check_entry(x: int, y: int, maze: Any) -> str:
    if (x, y) == maze.entry:
        return '\033[32m█\033[0m'
    elif (x, y) == maze.exit:
        return '\033[31m█\033[0m'
    elif (x, y) in maze.path_solve and maze.is_path:
        return '░'
    return '\033[38;5;235m█\033[0m'


def check_path(x: int, y: int, maze: Any) -> str:
    if (x, y) in maze.path_solve and maze.is_path:
        return '░'
    return '\033[38;5;235m█\033[0m'


# mypy R8: returns the pattern color or None when not a pattern cell
def check_pattern(x: int, y: int, maze: Any, color: str) -> str | None:
    if (x, y) in maze.pattern_cells:
        return color
    return None


def print_maze(maze: Any, color: str, color_pattern: str) -> None:
    line_bottom = ''
    for y in range(maze.height):
        line0 = ''
        line1 = ''
        for x in range(maze.width):
            pattern = check_pattern(x, y, maze, color_pattern)
            if pattern:
                line0 += pattern + pattern
                line1 += pattern + pattern
                continue
            c = maze.maze[y][x]
            if (c & Dir.N.value) and (c & Dir.W.value):
                line0 += f'{color}{color}'
                line1 += f'{color}'
                line1 += check_entry(x, y, maze)
            elif (c & Dir.N.value) and not (c & Dir.W.value):
                line0 += f'{color}{color}'
                if (x - 1, y) in maze.path_solve:
                    line1 += check_path(x, y, maze)
                else:
                    line1 += '\033[38;5;235m█\033[0m'
                line1 += check_entry(x, y, maze)
            elif (c & Dir.W.value) and not (c & Dir.N.value):
                line0 += f'{color}'
                if (x, y - 1) in maze.path_solve:
                    line0 += check_path(x, y, maze)
                else:
                    line0 += '\033[38;5;235m█\033[0m'
                line1 += f'{color}' + check_entry(x, y, maze)
            elif not (c & Dir.N.value) and not (c & Dir.W.value):
                line0 += f'{color}'
                if (x, y - 1) in maze.path_solve:
                    line0 += check_path(x, y, maze)
                else:
                    line0 += '\033[38;5;235m█\033[0m'
                if (x - 1, y) in maze.path_solve:
                    line1 += check_path(x, y, maze)
                else:
                    line1 += '\033[38;5;235m█\033[0m'
                line1 += check_entry(x, y, maze)
            if x == maze.width - 1:
                line0 += f'{color}'
                line1 += f'{color}'
            if y == maze.height - 1:
                line_bottom += f'{color}{color}'
        print(f"{line0}")
        print(f"{line1}")
    line_bottom += f'{color}'
    print(f"{line_bottom}")

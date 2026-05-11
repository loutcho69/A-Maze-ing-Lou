"""
Terminal rendering utilities for A-Maze-ing.

This module handles:
- ASCII title and menu display
- Maze rendering in terminal with ANSI colors
- Display of entry, exit, pattern, and shortest path
"""
from typing import Any
from .data import Dir


def print_title() -> None:
    """Print the ASCII art title of the application."""
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
    """Display the interactive menu options for the user."""
    print("                   A _ M A Z E _ I N G\n")
    print('1. Generate a new maze', end='   ')
    print('2. Show/hide path from entry to exit')
    print('3. Rotate maze colors', end='    ')
    print('4. Generate with other pattern')
    print('5. Rotate pattern color', end='  ')
    print('6. Quit\n')


def check_entry(x: int, y: int, maze: Any) -> str:
    """Return the correct character for entry, exit, or path cells.

    Priority:
    - Entry cell (green)
    - Exit cell (red)
    - Path cell (if path display is enabled)
    - Default wall cell

    Args:
        x: X coordinate.
        y: Y coordinate.
        maze: Maze object containing entry, exit, and path data.

    Returns:
        str: ANSI colored character representing the cell.
    """
    if (x, y) == maze.entry:
        return '\033[32m█\033[0m'
    elif (x, y) == maze.exit:
        return '\033[31m█\033[0m'
    elif (x, y) in maze.path_solve and maze.is_path:
        return '░'
    return '\033[38;5;235m█\033[0m'


def check_path(x: int, y: int, maze: Any) -> str:
    """Return the character representing a path cell if applicable.

    Args:
        x: X coordinate.
        y: Y coordinate.
        maze: Maze object containing path information.

    Returns:
        str: Path character or wall character.
    """
    if (x, y) in maze.path_solve and maze.is_path:
        return '░'
    return '\033[38;5;235m█\033[0m'


def check_pattern(x: int, y: int, maze: Any, color: str) -> str | None:
    """Return pattern color if the cell belongs to a pattern.

    Args:
        x: X coordinate.
        y: Y coordinate.
        maze: Maze object containing pattern cells.
        color: Color used for pattern rendering.

    Returns:
        Optional[str]: Pattern color if cell is part of pattern, else None.
    """
    if (x, y) in maze.pattern_cells:
        return color
    return None


def print_maze(maze: Any, color: str, color_pattern: str) -> None:
    """Render the maze in the terminal using ANSI colors.

    The maze is printed line by line, taking into account:
    - walls encoded in each cell
    - entry and exit positions
    - optional shortest path display
    - optional embedded pattern rendering

    Args:
        maze: Maze object containing grid and metadata.
        color: Primary color used for maze walls.
        color_pattern: Color used for embedded pattern cells.

    Returns:
        None
    """
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

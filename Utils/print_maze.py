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
    print('4. Quit\n')


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


def print_maze(maze, color) -> None:
    line_bottom = ''
    for y in range(maze.height):
        line0 = ''
        line1 = ''
        for x in range(maze.width):
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
    print_title()

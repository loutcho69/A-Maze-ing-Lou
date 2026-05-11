"""
A-Maze-ing main application.

Handles:
- configuration parsing
- maze generation (with optional pattern)
- interactive terminal menu
- rendering and output file writing
"""
import sys
import random
from mazegen.print_maze import print_maze, print_title, print_menu
from mazegen.maze_gen import MazeGenerator
from mazegen.data import Color
from mazegen.patterns import FORTY_TWO, PACMAN, INVADER, Pattern
from parsing import set_arg, MazeSetting
from output import write_output


def maze_gen(setting: MazeSetting, pattern: Pattern | None) -> MazeGenerator:
    """Generate a maze from settings and an optional pattern.

    This function wraps MazeGenerator creation and handles errors:
    - If a pattern causes a ValueError, generation is retried without pattern.
    - If generation still fails, the program exits.

    Args:
        setting: Validated configuration object.
        pattern: Optional pattern to embed in the maze.

    Returns:
        MazeGenerator: The generated maze instance.

    Exits:
        Program exits if maze generation is not possible.
    """
    try:
        maze = MazeGenerator(setting.WIDTH,
                             setting.HEIGHT,
                             setting.ENTRY,
                             setting.EXIT,
                             setting.PERFECT,
                             pattern,
                             setting.SEED)
    except ValueError as err:
        print(err)
        if pattern is None:
            exit()
        return maze_gen(setting, None)
    except Exception:
        print("Missing value in 'config.txt'")
        exit()
    return maze


if __name__ == "__main__":
    """Entry point of the program.

    Flow:
    - Parse configuration file
    - Validate settings
    - Initialize seed if provided
    - Generate initial maze
    - Start interactive menu loop
    """
    try:
        if len(sys.argv) == 2:
            setting = set_arg(sys.argv[1])
        else:
            raise Exception("Enter setting file name")
        if setting is None:
            raise Exception("No argument find")
    except Exception as e:
        print(e)
        exit()
    if setting.SEED is not None:
        random.seed(setting.SEED)
    maze = maze_gen(setting, FORTY_TWO)
    write_output(maze, setting.OUTPUT_FILE)
    print()
    print_maze(maze, Color.WHITE.value, Color.CYAN.value)
    print_title()
    print_menu()
    color = 1
    color_pattern = 1
    pattern = 1
    while True:
        try:
            cmd = int(input('Choice? (1-6): '))
            if cmd == 1:
                maze = maze_gen(setting, maze.pattern)
                write_output(maze, setting.OUTPUT_FILE)
                print()
                print_maze(maze, list(Color)[color - 1].value,
                           list(Color)[color_pattern + 4].value)
                print_title()
                print_menu()
            elif cmd == 2:
                if maze.is_path:
                    maze.is_path = False
                else:
                    maze.is_path = True
                print()
                print_maze(maze, list(Color)[color - 1].value,
                           list(Color)[color_pattern + 4].value)
                print_title()
                print_menu()
            elif cmd == 3:
                print('\nChoose a color:')
                print('1. White\n2. Purple\n3. Blue\n4. Red\n5. Orange\n')
                # Bug #1 fix: keep current 'color' until validation passes,
                # so a bad input doesn't corrupt it for the next commands
                color_tmp = color
                color = int(input())
                if color < 1 or color > 5:
                    color = color_tmp
                    raise ValueError
                print_maze(maze, list(Color)[color - 1].value,
                           list(Color)[color_pattern + 4].value)
                print_title()
                print_menu()
            elif cmd == 4:
                print('\nChoose a pattern:')
                print('1. 42\n2. Pacman\n3. Invader\n')
                # Bug #1 (sym): keep 'pattern' until validated
                pattern_tmp = pattern
                pattern = int(input())
                if pattern < 1 or pattern > 3:
                    pattern = pattern_tmp
                    raise ValueError
                if pattern == 1:
                    maze = maze_gen(setting, FORTY_TWO)
                elif pattern == 2:
                    maze = maze_gen(setting, PACMAN)
                else:
                    maze = maze_gen(setting, INVADER)
                write_output(maze, setting.OUTPUT_FILE)
                print_maze(maze, list(Color)[color - 1].value,
                           list(Color)[color_pattern + 4].value)
                print_title()
                print_menu()
            elif cmd == 5:
                print('\nChoose a pattern color:')
                print('1. Cyan\n2. Green\n3. Yellow\n')
                color_tmp = color_pattern
                color_pattern = int(input())
                if color_pattern < 1 or color_pattern > 3:
                    color_pattern = color_tmp
                    raise ValueError
                print_maze(maze, list(Color)[color - 1].value,
                           list(Color)[color_pattern + 4].value)
                print_title()
                print_menu()
            elif cmd == 6:
                exit()
            else:
                raise ValueError
        except ValueError:
            print("Please enter a correct value\n")
            print_menu()
        except (KeyboardInterrupt, EOFError):
            exit()

import sys
import random
from mazegen.print_maze import print_maze, print_title
from mazegen.maze_gen import MazeGenerator
from mazegen.data import Color
from mazegen.patterns import list_patterns, FORTY_TWO
from parsing import set_arg


def maze_gen(setting, pattern=None):
    try:
        maze = MazeGenerator(setting.WIDTH,
                             setting.HEIGHT,
                             setting.ENTRY,
                             setting.EXIT,
                             setting.PERFECT,
                             pattern=pattern)
    except ValueError as err:
        # Pattern doesn't fit (or other validation error from generator).
        print(f"Pattern error: {err}")
        return None
    except Exception as err:
        print(f"Missing value in 'config.txt'")
        exit()
    return maze


def write_output_file(maze, filename):
    """Write the maze to the output file in the format specified by
    the subject (IV.5). Errors are reported but don't crash the
    program (the user can still interact with the maze).
    """
    try:
        with open(filename, 'w') as f:
            f.write(maze.to_output())
    except OSError as err:
        print(f"Could not write to '{filename}': {err}")


if __name__ == "__main__":
    # Subject IV.2: program is invoked as `python3 a_maze_ing.py config.txt`.
    # The config filename is the only argument. Default to 'config.txt'
    # if none is given, so people who just run `python3 a_maze_ing.py`
    # still get a working program.
    if len(sys.argv) > 2:
        print("Usage: python3 a_maze_ing.py [config.txt]")
        exit(1)
    config_file = sys.argv[1] if len(sys.argv) == 2 else 'config.txt'

    setting = set_arg(config_file)
    if setting is None:
        # set_arg already printed a clear error message. Exit cleanly.
        exit(1)

    # Apply the seed if one is set in the config (subject IV.4).
    if setting.SEED is not None:
        random.seed(setting.SEED)

    pattern = FORTY_TWO  # default pattern
    color = 1            # default wall color: White
    pat_color = 4        # default pattern color: Red

    maze = maze_gen(setting, pattern=pattern)
    if maze is None:
        # The default pattern doesn't fit. Since we always want a
        # pattern, refuse to start instead of falling back to none.
        print("The default pattern doesn't fit in this maze size.")
        print("Tip: increase WIDTH and HEIGHT in config.txt.")
        exit(1)
    write_output_file(maze, setting.OUTPUT_FILE)
    print()
    print_maze(maze, list(Color)[color - 1].value,
               list(Color)[pat_color - 1].value)
    print_title()

    while True:
        try:
            cmd = int(input('Choice? (1-6): '))
            if cmd == 1:
                new_maze = maze_gen(setting, pattern=pattern)
                if new_maze is None:
                    print("Generation failed; keeping previous maze.")
                    continue
                maze = new_maze
                write_output_file(maze, setting.OUTPUT_FILE)
                print()
                print_maze(maze, list(Color)[color - 1].value,
                           list(Color)[pat_color - 1].value)
                print_title()
            elif cmd == 2:
                if maze.is_path:
                    maze.is_path = False
                else:
                    maze.is_path = True
                print()
                print_maze(maze, list(Color)[color - 1].value,
                           list(Color)[pat_color - 1].value)
                print_title()
            elif cmd == 3:
                print('\nChoose a color:')
                print('1. White\n2. Purple\n3. Blue\n4. Red\n5. Orange\n')
                color = int(input())
                if color < 1 or color > 5:
                    raise ValueError
                print_maze(maze, list(Color)[color - 1].value,
                           list(Color)[pat_color - 1].value)
                print_title()
            elif cmd == 4:
                patterns = list_patterns()
                print('\nChoose a pattern:')
                for i, p in enumerate(patterns, 1):
                    marker = ' (current)' if p is pattern else ''
                    print(f'{i}. {p.name}{marker}')
                print()
                choice = int(input())
                if choice < 1 or choice > len(patterns):
                    raise ValueError
                new_pattern = patterns[choice - 1]
                if new_pattern is pattern:
                    continue
                new_maze = maze_gen(setting, pattern=new_pattern)
                if new_maze is None:
                    print("Pattern doesn't fit; keeping previous maze.")
                    continue
                pattern = new_pattern
                maze = new_maze
                write_output_file(maze, setting.OUTPUT_FILE)
                print_maze(maze, list(Color)[color - 1].value,
                           list(Color)[pat_color - 1].value)
                print_title()
            elif cmd == 5:
                print('\nChoose a pattern color:')
                print('1. White\n2. Purple\n3. Blue\n4. Red\n5. Orange\n')
                pat_color = int(input())
                if pat_color < 1 or pat_color > 5:
                    raise ValueError
                print_maze(maze, list(Color)[color - 1].value,
                           list(Color)[pat_color - 1].value)
                print_title()
            elif cmd == 6:
                exit()
            else:
                raise ValueError
        except ValueError as e:
            print("Please enter a correct value")

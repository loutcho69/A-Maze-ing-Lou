import sys
import random
from mazegen import (
    MazeGenerator, print_maze, print_title,
    list_patterns, FORTY_TWO,
)
from mazegen.data import Color
from parsing import set_arg

COLORS = list(Color)
COLOR_NAMES = ['White', 'Purple', 'Blue', 'Red', 'Orange']


def build_maze(setting, pattern):
    try:
        return MazeGenerator(setting.WIDTH, setting.HEIGHT,
                             setting.ENTRY, setting.EXIT,
                             setting.PERFECT, pattern=pattern)
    except ValueError as err:
        print(f"Pattern error: {err}")
        return None


def write_output(maze, filename):
    try:
        with open(filename, 'w') as f:
            f.write(maze.to_output())
    except OSError as err:
        print(f"Could not write to '{filename}': {err}")


def display(maze, ci, pi):
    print()
    print_maze(maze, COLORS[ci - 1].value, COLORS[pi - 1].value)
    print_title()


def pick(prompt, items, current=None):
    """Print a numbered menu and return the chosen index (1-based)."""
    print(f'\n{prompt}')
    for i, label in enumerate(items, 1):
        marker = ' (current)' if label == current else ''
        print(f'{i}. {label}{marker}')
    print()
    n = int(input())
    if not (1 <= n <= len(items)):
        raise ValueError
    return n


def main():
    if len(sys.argv) > 2:
        print("Usage: python3 a_maze_ing.py [config.txt]")
        sys.exit(1)
    cfg_file = sys.argv[1] if len(sys.argv) == 2 else 'config.txt'

    setting = set_arg(cfg_file)
    if setting is None:
        sys.exit(1)
    if setting.SEED is not None:
        random.seed(setting.SEED)

    pattern = FORTY_TWO
    ci, pi = 1, 4  # wall color index, pattern color index

    maze = build_maze(setting, pattern)
    if maze is None:
        print("The default pattern doesn't fit in this maze size.")
        print("Tip: increase WIDTH and HEIGHT in config.txt.")
        sys.exit(1)
    write_output(maze, setting.OUTPUT_FILE)
    display(maze, ci, pi)

    patterns = list_patterns()
    while True:
        try:
            cmd = int(input('Choice? (1-6): '))
            if cmd == 1:
                new = build_maze(setting, pattern)
                if new is None:
                    print("Generation failed; keeping previous maze.")
                    continue
                maze = new
                write_output(maze, setting.OUTPUT_FILE)
                display(maze, ci, pi)
            elif cmd == 2:
                maze.is_path = not maze.is_path
                display(maze, ci, pi)
            elif cmd == 3:
                ci = pick('Choose a wall color:', COLOR_NAMES)
                display(maze, ci, pi)
            elif cmd == 4:
                idx = pick('Choose a pattern:',
                           [p.name for p in patterns], pattern.name)
                new_pat = patterns[idx - 1]
                if new_pat is pattern:
                    continue
                new = build_maze(setting, new_pat)
                if new is None:
                    print("Pattern doesn't fit; keeping previous maze.")
                    continue
                pattern, maze = new_pat, new
                write_output(maze, setting.OUTPUT_FILE)
                display(maze, ci, pi)
            elif cmd == 5:
                pi = pick('Choose a pattern color:', COLOR_NAMES)
                display(maze, ci, pi)
            elif cmd == 6:
                sys.exit(0)
            else:
                raise ValueError
        except ValueError:
            print("Please enter a correct value")


if __name__ == "__main__":
    main()

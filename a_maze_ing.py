from mazegen.print_maze import print_maze, print_title, print_menu
from mazegen.maze_gen import MazeGenerator
from mazegen.data import Color
from mazegen.patterns import FORTY_TWO, PACMAN, INVADER
from parsing import set_arg


def maze_gen(setting, pattern):
    try:
        maze = MazeGenerator(setting.WIDTH,
                            setting.HEIGHT,
                            setting.ENTRY,
                            setting.EXIT,
                            setting.PERFECT,
                            pattern)
    except Exception as err:
        print(f"Missing value in 'config.txt'")
        exit()
    return maze

if __name__ == "__main__":
    setting = set_arg('config.txt')
    maze = maze_gen(setting, FORTY_TWO)
    print()
    print_maze(maze, Color.WHITE.value, Color.CYAN.value)
    print_title()
    print_menu()
    color = 1
    color_pattern = 1
    while True:
        try:
            cmd = int(input('Choice? (1-6): '))
            if cmd == 1:
                maze = maze_gen(setting, maze.pattern)
                print()
                print_maze(maze, list(Color)[color - 1].value, list(Color)[color_pattern + 4].value)
                print_title()
                print_menu()
            elif cmd == 2:
                if maze.is_path:
                    maze.is_path = False
                else:
                    maze.is_path = True
                print()
                print_maze(maze, list(Color)[color - 1].value, list(Color)[color_pattern + 4].value)
                print_title()
                print_menu()
            elif cmd == 3:
                print('\nChoose a color:')
                print('1. White\n2. Purple\n3. Blue\n4. Red\n5. Orange\n')
                color = int(input())
                if color < 1 or color > 5:
                    raise ValueError
                print_maze(maze, list(Color)[color - 1].value, list(Color)[color_pattern + 4].value)
                print_title()
                print_menu()
            elif cmd == 4:
                print('\nChoose a pattern:')
                print('1. 42\n2. Pacman\n3. Invader\n')
                pattern = int(input())
                if pattern < 1 or pattern > 3:
                    raise ValueError
                if pattern == 1:
                    maze = maze_gen(setting, FORTY_TWO)
                elif pattern == 2:
                    maze = maze_gen(setting, PACMAN)
                else:
                    maze = maze_gen(setting, INVADER)
                print_maze(maze, list(Color)[color - 1].value, list(Color)[color_pattern + 4].value)
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
                print_maze(maze, list(Color)[color - 1].value, list(Color)[color_pattern + 4].value)
                print_title()
                print_menu()
            elif cmd == 6:
                exit()
            else:
                raise ValueError
        except ValueError as e:
            print("Please enter a correct value\n")
            print_menu()
        except (KeyboardInterrupt, EOFError) as e:
            exit()

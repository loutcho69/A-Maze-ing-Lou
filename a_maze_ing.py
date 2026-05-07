from Utils.print_maze import print_maze
from Utils.maze_gen import maze_gen
from Utils.data import Color
from Utils.parsing import set_arg
from Utils.patterns import list_patterns, FORTY_TWO


def choose_pattern(current):
    """Prompt the user to pick a pattern (or none).

    Returns the chosen Pattern, or None for "no pattern".
    Returns `current` unchanged on invalid input.
    """
    patterns = list_patterns()
    print('\nChoose a pattern:')
    for i, p in enumerate(patterns, 1):
        marker = ' (current)' if p is current else ''
        print(f'{i}. {p.name}{marker}')
    none_idx = len(patterns) + 1
    none_marker = ' (current)' if current is None else ''
    print(f'{none_idx}. none{none_marker}\n')
    try:
        choice = int(input())
    except ValueError:
        print('Invalid input, pattern unchanged.')
        return current
    if 1 <= choice <= len(patterns):
        return patterns[choice - 1]
    if choice == none_idx:
        return None
    print('Invalid choice, pattern unchanged.')
    return current


def choose_pattern_color(current_idx):
    """Prompt the user to pick a pattern color.

    Returns the new color index (1-based into list(Color)).
    Returns `current_idx` unchanged on invalid input.
    """
    colors = list(Color)
    print('\nChoose a pattern color:')
    for i, c in enumerate(colors, 1):
        marker = ' (current)' if i == current_idx else ''
        print(f'{i}. {c.name.capitalize()}{marker}')
    print()
    try:
        choice = int(input())
    except ValueError:
        print('Invalid input, color unchanged.')
        return current_idx
    if 1 <= choice <= len(colors):
        return choice
    print('Invalid choice, color unchanged.')
    return current_idx


def render(maze, wall_color_idx, pattern_color_idx):
    """Render the maze with the currently selected colors."""
    colors = list(Color)
    wall = colors[wall_color_idx - 1].value
    pat = colors[pattern_color_idx - 1].value
    print()
    print_maze(maze, wall, pat)


if __name__ == "__main__":
    setting = set_arg('config.txt')
    if setting is None:
        exit(1)

    # Default state: 42 pattern, white walls, red pattern color.
    pattern = FORTY_TWO
    wall_color = 1   # white
    pat_color = 4    # red
    # When SEED is set in the config, each "regenerate" bumps this
    # offset so the user actually sees a new maze. When SEED is unset,
    # generation is fully random and the offset is unused.
    seed_offset = 0

    def current_seed():
        if setting.SEED is None:
            return None
        return setting.SEED + seed_offset

    maze = maze_gen(setting, pattern=pattern, seed=current_seed())
    if maze is None:
        # Pattern doesn't fit the configured maze size. The subject
        # explicitly allows omitting the pattern in this case, provided
        # we tell the user.
        print(
            "No pattern fits this maze size. "
            "Starting without a pattern."
        )
        print(
            "Tip: increase WIDTH and HEIGHT in config.txt "
            "to use patterns."
        )
        pattern = None
        maze = maze_gen(setting, pattern=None, seed=current_seed())
        if maze is None:
            exit(1)

    render(maze, wall_color, pat_color)

    while True:
        try:
            cmd = int(input('Choice? (1-6): '))
        except ValueError:
            print("Please enter a correct value")
            continue

        if cmd == 1:
            seed_offset += 1
            new_maze = maze_gen(setting, pattern=pattern, seed=current_seed())
            if new_maze is None:
                print("Generation failed; keeping previous maze.")
                seed_offset -= 1  # revert the bump on failure
                continue
            maze = new_maze
            render(maze, wall_color, pat_color)

        elif cmd == 2:
            maze.is_path = not maze.is_path
            render(maze, wall_color, pat_color)

        elif cmd == 3:
            print('\nChoose a wall color:')
            for i, c in enumerate(Color, 1):
                marker = ' (current)' if i == wall_color else ''
                print(f'{i}. {c.name.capitalize()}{marker}')
            print()
            try:
                choice = int(input())
                if 1 <= choice <= len(Color):
                    wall_color = choice
                else:
                    print("Invalid choice.")
                    continue
            except ValueError:
                print("Please enter a correct value")
                continue
            render(maze, wall_color, pat_color)

        elif cmd == 4:
            new_pattern = choose_pattern(pattern)
            if new_pattern is pattern:
                continue
            # Try to regenerate; keep previous on failure.
            seed_offset += 1
            new_maze = maze_gen(
                setting, pattern=new_pattern, seed=current_seed()
            )
            if new_maze is None:
                print("Pattern doesn't fit; keeping previous maze and pattern.")
                seed_offset -= 1
                continue
            pattern = new_pattern
            maze = new_maze
            render(maze, wall_color, pat_color)

        elif cmd == 5:
            pat_color = choose_pattern_color(pat_color)
            render(maze, wall_color, pat_color)

        elif cmd == 6:
            exit(0)

        else:
            print("Please enter a correct value")

def check_entry(x, y, path):
    if (x, y) == entry:
        return '\033[32m█\033[0m'
    elif (x, y) == exit:
        return '\033[31m█\033[0m'
    elif (x, y) in path:
        return '\033[35m█\033[0m'
    return ' '
    
def check_path(x, y, path):
    if (x, y) in path:
        return '\033[35m█\033[0m'
    return ' '


def print_maze(maze) -> None:
    line_bottom = ''
    for y in range(self.height):
        line0 = ''
        line1 = ''
        for x in range(maze.width):
            c = maze.maze[y][x]
            if (c & N) and (c & W):
                line0 += '██'
                line1 += '█'
                line1 += check_entry(x, y, path)
            elif (c & N) and not (c & W):
                line0 += '██'
                if (x - 1, y) in maze.path:
                    line1 += check_path(x, y, maze.path)
                else:
                    line1 += ' '
                line1 += check_entry(x, y, maze.path)
            elif (c & W) and not (c & N):
                line0 += '█'
                if (x, y - 1) in maze.path:
                    line0 += check_path(x, y, maze.path)
                else:
                    line0 += ' '
                line1 += '█' + check_entry(x, y, maze.path)
            elif not (c & N) and not (c & W):
                line0 += '█'
                if (x, y - 1) in maze.path:
                    line0 += check_path(x, y, maze.path)
                else:
                    line0 += ' ' 
                if (x - 1, y) in maze.path:
                    line1 += check_path(x, y, maze.path)
                else:
                    line1 += ' '
                line1 += check_entry(x, y, maze.path)
            if x == maze.width - 1:
                line0 += '█'
                line1 += '█'
            if y == maze.height - 1:
                line_bottom += '██'
        print(line0)
        print(line1)
    line_bottom += '█'
    print(line_bottom)
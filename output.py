from typing import Any


# mypy R8: annotations required (no-untyped-def)
# 'Any' avoids importing MazeGenerator (would create a circular import)
def write_output(maze: Any, filename: str) -> None:
    try:
        with open(filename, "w") as file:
            file.write(maze.to_output())
    except OSError as err:
        print(f"Cannot write output file '{filename}': {err.strerror or err}")

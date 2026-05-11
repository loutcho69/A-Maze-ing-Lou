"""
Output writer for A-Maze-ing.

This module is responsible for writing a generated maze
to a file in the required output format.

It converts the internal maze representation into a
textual representation via the `to_output()` method.
"""
from typing import Any


def write_output(maze: Any, filename: str) -> None:
    """Write a generated maze to a file in the required output format.

    The maze object must expose a `to_output()` method returning a string
    representation of the maze (grid + entry/exit + path).

    Args:
        maze: Maze object providing a `to_output()` method.
        filename: Path to the file where the maze will be written.

    Returns:
        None

    Raises:
        OSError: If the file cannot be created or written to.

    Notes:
        The file is overwritten if it already exists.
    """
    try:
        with open(filename, "w") as file:
            file.write(maze.to_output())

    except OSError as err:
        print(
            f"Cannot write output file '{filename}': "
            f"{err.strerror or err}"
        )

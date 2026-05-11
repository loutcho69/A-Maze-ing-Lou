"""
Pattern definitions for A-Maze-ing.

This module provides:
- A Pattern dataclass representing a binary grid
- Predefined embedded patterns (42, Pacman, Invader)

A pattern defines cells that must remain closed during maze generation.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Pattern:
    """Immutable representation of a maze embedded pattern.

    A pattern is defined by a binary grid where:
    - 1 represents a blocked (closed) cell
    - 0 represents a free cell

    Attributes:
        name: Name of the pattern.
        grid: 2D tuple representing the pattern layout.
    """
    name: str
    grid: tuple[tuple[int, ...], ...]

    @property
    def height(self) -> int:
        """Return the number of rows in the pattern grid."""
        return len(self.grid)

    @property
    def width(self) -> int:
        """Return the number of columns in the pattern grid.

        Returns 0 if the grid is empty.
        """
        return len(self.grid[0]) if self.grid else 0

    def closed_cells(self) -> set[tuple[int, int]]:
        """Return the set of coordinates of blocked cells.

        Returns:
            set[tuple[int, int]]: Coordinates (x, y) of all cells
            marked as 1 in the pattern grid.
        """
        return {(x, y) for y, row in enumerate(self.grid)
                for x, v in enumerate(row) if v == 1}


FORTY_TWO = Pattern("42", (
    (1, 0, 0, 1, 0, 1, 1, 1, 0),
    (1, 0, 0, 1, 0, 0, 0, 0, 1),
    (1, 0, 0, 1, 0, 0, 0, 0, 1),
    (1, 1, 1, 1, 0, 0, 0, 1, 0),
    (0, 0, 0, 1, 0, 0, 1, 0, 0),
    (0, 0, 0, 1, 0, 1, 0, 0, 0),
    (0, 0, 0, 1, 0, 1, 1, 1, 1),
))

PACMAN = Pattern("pacman", (
    (0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0),
    (0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0),
    (0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0),
    (0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0),
    (1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0),
    (1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0),
    (1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0),
    (0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0),
    (0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0),
    (0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0),
    (0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0),
))

INVADER = Pattern("invader", (
    (0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0),
    (0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0),
    (0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0),
    (0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0),
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    (0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0),
    (0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0),
    (0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0),
))

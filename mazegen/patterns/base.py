from dataclasses import dataclass


@dataclass(frozen=True)
class Pattern:
    """Represent a pattern made of closed cells inside the maze.

    The pattern is a 2D grid of 0/1 where 1 means the cell must be
    fully closed (all 4 walls intact).

    Attributes:
        name: Display name of the pattern (e.g. "42").
        grid: 2D tuple of 0/1, indexed grid[y][x].
    """

    name: str
    grid: tuple[tuple[int, ...], ...]

    @property
    def height(self) -> int:
        return len(self.grid)

    @property
    def width(self) -> int:
        return len(self.grid[0]) if self.grid else 0

    def closed_cells(self) -> set[tuple[int, int]]:
        """Return the set of (x, y) offsets that are 1 in the grid."""
        return {
            (x, y)
            for y, row in enumerate(self.grid)
            for x, val in enumerate(row)
            if val == 1
        }

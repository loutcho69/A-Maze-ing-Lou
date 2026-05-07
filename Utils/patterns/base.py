from dataclasses import dataclass


@dataclass(frozen=True)
class Pattern:
    """Represent a pattern made of closed cells inside the maze.

    The pattern is a 2D grid of 0/1 where 1 means the cell must be
    fully closed (all 4 walls intact).

    Attributes:
        name: Display name of the pattern (e.g. "42", "footballer").
        grid: 2D tuple of 0/1, indexed grid[y][x].
    """

    name: str
    grid: tuple[tuple[int, ...], ...]

    @property
    def height(self) -> int:
        """Pattern height in cells."""
        return len(self.grid)

    @property
    def width(self) -> int:
        """Pattern width in cells."""
        return len(self.grid[0]) if self.grid else 0

    def closed_cells(self) -> set[tuple[int, int]]:
        """Return the set of (x, y) offsets that are closed cells.

        Coordinates are local to the pattern (0,0 = top-left of pattern).
        """
        return {
            (x, y)
            for y, row in enumerate(self.grid)
            for x, val in enumerate(row)
            if val == 1
        }

    def scale(self, factor: int) -> "Pattern":
        """Return a copy of this pattern enlarged by an integer factor.

        Each pixel of the original grid is replaced by a factor x factor
        block of identical pixels. So a 9x7 pattern at factor=2 becomes
        an 18x14 pattern. factor=1 returns an identical copy.

        Note: at factor >= 3, blocks of empty cells in the original
        produce 3x3 (or larger) open areas, which violate the maze
        rules. This method does not enforce that constraint -- callers
        must restrict factor to {1, 2} or post-process the output.
        """
        if factor < 1:
            raise ValueError(f"scale factor must be >= 1, got {factor}")
        if factor == 1:
            return Pattern(name=self.name, grid=self.grid)
        new_grid = tuple(
            tuple(val for val in row for _ in range(factor))
            for row in self.grid
            for _ in range(factor)
        )
        return Pattern(name=self.name, grid=new_grid)

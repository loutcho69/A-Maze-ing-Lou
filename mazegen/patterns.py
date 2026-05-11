from dataclasses import dataclass


@dataclass(frozen=True)
class Pattern:
    name: str
    grid: tuple[tuple[int, ...], ...]

    @property
    def height(self) -> int:
        return len(self.grid)

    @property
    def width(self) -> int:
        return len(self.grid[0]) if self.grid else 0

    def closed_cells(self) -> set[tuple[int, int]]:
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

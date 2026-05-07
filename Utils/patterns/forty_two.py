from .base import Pattern


# "42" pattern, 9 wide x 7 tall
# Designed to be readable: a "4" then a "2" with one cell of spacing.
_GRID = (
    (1, 0, 0, 1, 0, 1, 1, 1, 0),
    (1, 0, 0, 1, 0, 0, 0, 0, 1),
    (1, 0, 0, 1, 0, 0, 0, 0, 1),
    (1, 1, 1, 1, 0, 0, 0, 1, 0),
    (0, 0, 0, 1, 0, 0, 1, 0, 0),
    (0, 0, 0, 1, 0, 1, 0, 0, 0),
    (0, 0, 0, 1, 0, 1, 1, 1, 1),
)

FORTY_TWO = Pattern(name="42", grid=_GRID)

from .base import Pattern


# President-style bust: head + suit jacket with tie.
# Generic suited figure, no real person depicted.
# 9 wide x 10 tall.
_GRID = (
    (0, 0, 0, 1, 1, 1, 0, 0, 0),  # hair top
    (0, 0, 1, 1, 1, 1, 1, 0, 0),  # hair
    (0, 0, 1, 1, 1, 1, 1, 0, 0),  # head
    (0, 0, 1, 1, 1, 1, 1, 0, 0),  # face
    (0, 0, 0, 1, 1, 1, 0, 0, 0),  # neck
    (0, 1, 1, 1, 0, 1, 1, 1, 0),  # shoulders + collar gap
    (1, 1, 1, 0, 1, 0, 1, 1, 1),  # jacket + tie top
    (1, 1, 1, 0, 1, 0, 1, 1, 1),  # jacket + tie
    (1, 1, 1, 1, 1, 1, 1, 1, 1),  # jacket bottom
    (1, 1, 1, 1, 1, 1, 1, 1, 1),  # jacket bottom
)

PRESIDENT = Pattern(name="president", grid=_GRID)

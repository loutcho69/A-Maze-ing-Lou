from .base import Pattern


# Basketball player silhouette: head, body, ball at the side.
# 9 wide x 11 tall.
_GRID = (
    (0, 0, 0, 1, 1, 1, 0, 0, 0),  # head top
    (0, 0, 1, 1, 1, 1, 1, 0, 0),  # head
    (0, 0, 1, 1, 1, 1, 1, 0, 0),  # head
    (0, 0, 0, 1, 1, 1, 0, 0, 0),  # neck
    (0, 1, 1, 1, 1, 1, 1, 1, 0),  # shoulders
    (0, 1, 1, 1, 1, 1, 1, 1, 1),  # body + arm reaches ball
    (0, 1, 1, 1, 1, 1, 1, 1, 1),  # body + ball
    (0, 1, 1, 1, 1, 1, 1, 1, 0),  # body
    (0, 0, 1, 1, 0, 1, 1, 0, 0),  # legs split
    (0, 0, 1, 1, 0, 1, 1, 0, 0),  # legs
    (0, 0, 1, 1, 0, 1, 1, 0, 0),  # feet
)

BASKETBALL = Pattern(name="basketball", grid=_GRID)

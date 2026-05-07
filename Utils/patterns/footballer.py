from .base import Pattern


# Footballer silhouette: head + jersey + soccer ball at his feet.
# 9 wide x 11 tall.
_GRID = (
    (0, 0, 0, 1, 1, 1, 0, 0, 0),  # head top
    (0, 0, 1, 1, 1, 1, 1, 0, 0),  # head
    (0, 0, 1, 1, 1, 1, 1, 0, 0),  # head
    (0, 0, 0, 1, 1, 1, 0, 0, 0),  # neck
    (0, 1, 1, 1, 1, 1, 1, 1, 0),  # shoulders
    (0, 1, 1, 1, 1, 1, 1, 1, 0),  # jersey top
    (0, 1, 1, 1, 1, 1, 1, 1, 0),  # jersey
    (0, 0, 1, 1, 0, 1, 1, 0, 0),  # waist / legs split
    (0, 0, 1, 1, 0, 1, 1, 0, 0),  # legs
    (0, 0, 1, 1, 0, 1, 1, 0, 0),  # feet
    (0, 0, 0, 0, 1, 0, 0, 0, 0),  # ball
)

FOOTBALLER = Pattern(name="footballer", grid=_GRID)

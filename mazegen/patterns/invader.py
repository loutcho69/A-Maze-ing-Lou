from .base import Pattern


# Alien-invader silhouette in pixel-art style.
# 11 wide x 9 tall.
_GRID = (
    (0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0),
    (0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0),
    (0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0),
    (0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0),
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
    (0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0),
    (0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0),
    (0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0),
)

INVADER = Pattern(name="invader", grid=_GRID)

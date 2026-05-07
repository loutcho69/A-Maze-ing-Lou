from .base import Pattern


# Alien-invader silhouette in pixel-art style: two antennas at the top,
# a head-body, and short legs. The shape is kept compact and convex
# enough to keep the surrounding maze easy to generate.
# 11 wide x 9 tall.
_GRID = (
    (0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0),  # antennas
    (0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0),  # antennas leaning in
    (0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0),  # top of head
    (0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0),  # head
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),  # widest (arms out)
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),  # body
    (0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0),  # narrows (between legs not yet)
    (0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 0),  # legs split (pixels with gaps)
    (0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 0),  # feet sticking out
)

INVADER = Pattern(name="invader", grid=_GRID)

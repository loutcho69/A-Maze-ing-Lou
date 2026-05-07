from .base import Pattern


# Pacman-style: a disc with a wedge cut out (mouth) opening to the right.
# 11 wide x 11 tall. The mouth is a V-shape pointing right.
_GRID = (
    (0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0),  # top of head
    (0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0),
    (0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0),
    (0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0),  # mouth starts (top edge)
    (1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0),  # mouth widens
    (1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0),  # mouth peak (deepest)
    (1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0),  # mouth narrows
    (0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0),  # mouth ends (bottom edge)
    (0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0),
    (0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0),
    (0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0),  # bottom of head
)

PACMAN = Pattern(name="pacman", grid=_GRID)

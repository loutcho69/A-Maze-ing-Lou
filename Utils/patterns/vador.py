from .base import Pattern


# Dark helmet silhouette: rounded dome with lateral "shoulder pads"
# at the base, V-shaped chin guard. Designed to look distinctly
# different from a round head.
# 11 wide x 11 tall.
_GRID = (
    (0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0),  # dome top
    (0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0),  # dome
    (0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0),  # dome
    (0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0),  # eye line (kept solid)
    (0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0),
    (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),  # widest (helmet base)
    (1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1),  # shoulder pads / vents
    (1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1),
    (1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 1),  # shoulders flare out
    (0, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0),
    (0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0),  # chin point
)

VADOR = Pattern(name="vador", grid=_GRID)

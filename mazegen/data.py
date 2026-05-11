"""
Core enums for A-Maze-ing.

Defines:
- Dir: bit-flag representation of maze walls
- Color: ANSI colors used for terminal rendering
"""
from enum import Enum


class Dir(Enum):
    """Bitmask representation of maze directions.

    Each direction corresponds to a power of two, allowing
    walls to be encoded as bitwise values in each cell:

    - N = 1
    - E = 2
    - S = 4
    - W = 8
    """
    N = 1
    E = 2
    S = 4
    W = 8


class Color(Enum):
    """ANSI color codes used for terminal maze rendering.

    Each value represents a colored block character used to draw:
    - maze walls
    - patterns
    - UI elements

    Colors are encoded using ANSI escape sequences.
    """
    WHITE = '█'
    PURPLE = '\033[38;2;186;104;200m█\033[0m'
    BLUE = '\033[38;2;144;202;249m█\033[0m'
    RED = '\033[38;2;229;115;115m█\033[0m'
    ORANGE = '\033[38;2;255;183;77m█\033[0m'
    CYAN = '\033[38;2;77;208;225m█\033[0m'
    GREEN = '\033[38;2;129;199;132m█\033[0m'
    YELLOW = '\033[38;2;255;238;88m█\033[0m'

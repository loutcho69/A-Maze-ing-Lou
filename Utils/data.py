from enum import Enum

class Dir(Enum):
    N = 1
    E = 2
    S = 4
    W = 8

class Color(Enum):
    WHITE = '█'
    PURPLE = '\033[38;2;186;104;200m█\033[0m'
    BLUE = '\033[38;2;144;202;249m█\033[0m'
    RED = '\033[38;2;229;115;115m█\033[0m'
    ORANGE = '\033[38;2;255;183;77m█\033[0m'
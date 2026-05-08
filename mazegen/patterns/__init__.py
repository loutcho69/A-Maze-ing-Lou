from .base import Pattern
from .forty_two import FORTY_TWO
from .pacman import PACMAN
from .invader import INVADER


# Ordered registry: insertion order is used for menu numbering.
PATTERNS: dict[str, Pattern] = {
    FORTY_TWO.name: FORTY_TWO,
    PACMAN.name: PACMAN,
    INVADER.name: INVADER,
}


def list_patterns() -> list[Pattern]:
    """Return all registered patterns in insertion order."""
    return list(PATTERNS.values())


__all__ = [
    "Pattern",
    "PATTERNS",
    "list_patterns",
    "FORTY_TWO",
    "PACMAN",
    "INVADER",
]

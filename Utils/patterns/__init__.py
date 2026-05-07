from .base import Pattern
from .forty_two import FORTY_TWO
from .pacman import PACMAN
from .vador import VADOR
from .invader import INVADER


# Ordered registry: insertion order is used for menu numbering.
PATTERNS: dict[str, Pattern] = {
    FORTY_TWO.name: FORTY_TWO,
    PACMAN.name: PACMAN,
    VADOR.name: VADOR,
    INVADER.name: INVADER,
}


def get_pattern(name: str) -> Pattern | None:
    """Return the Pattern registered under that name, or None."""
    return PATTERNS.get(name)


def list_patterns() -> list[Pattern]:
    """Return all registered patterns in insertion order."""
    return list(PATTERNS.values())


__all__ = [
    "Pattern",
    "PATTERNS",
    "get_pattern",
    "list_patterns",
    "FORTY_TWO",
    "PACMAN",
    "VADOR",
    "INVADER",
]

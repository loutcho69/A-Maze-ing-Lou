from .base import Pattern
from .forty_two import FORTY_TWO
from .footballer import FOOTBALLER
from .basketball import BASKETBALL
from .president import PRESIDENT


# Ordered registry: insertion order is used for menu numbering.
PATTERNS: dict[str, Pattern] = {
    FORTY_TWO.name: FORTY_TWO,
    FOOTBALLER.name: FOOTBALLER,
    BASKETBALL.name: BASKETBALL,
    PRESIDENT.name: PRESIDENT,
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
    "FOOTBALLER",
    "BASKETBALL",
    "PRESIDENT",
]

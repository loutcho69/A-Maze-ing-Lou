"""Parse and validate the configuration file (subject IV.3)."""
from pydantic import BaseModel, Field, ValidationError, model_validator


VALID_KEYS = frozenset({
    'WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT', 'SEED',
})


class MazeSetting(BaseModel):
    WIDTH: int = Field(ge=3)
    HEIGHT: int = Field(ge=3)
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool
    SEED: int | None = None

    @model_validator(mode="after")
    def check_setting(self):
        ex, ey = self.ENTRY
        xx, xy = self.EXIT
        if not (0 <= ex < self.WIDTH and 0 <= ey < self.HEIGHT):
            raise ValueError("ENTRY is out of bounds")
        if not (0 <= xx < self.WIDTH and 0 <= xy < self.HEIGHT):
            raise ValueError("EXIT is out of bounds")
        if self.ENTRY == self.EXIT:
            raise ValueError("ENTRY and EXIT must be different")
        return self


def parse_value(value):
    value = value.strip()
    if value in ("True", "False"):
        return value == "True"
    if "," in value:
        a, b = value.split(",", 1)
        try:
            return int(a), int(b)
        except ValueError:
            return value
    try:
        return int(value)
    except ValueError:
        return value


def set_arg(filename):
    """Read filename and return a validated MazeSetting, or None on error
    (after printing a clear message)."""
    args = {}
    try:
        with open(filename) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if '=' not in line:
                    raise ValueError("Invalid line. Missing '='")
                key, value = line.split('=', 1)
                key = key.strip()
                if key not in VALID_KEYS:
                    raise ValueError(f"Unknown config key: {key}")
                args[key] = parse_value(value)
        return MazeSetting(**args)
    except FileNotFoundError:
        print(f"Config file not found: {filename}")
    except ValidationError as err:
        print(err.errors()[0]["msg"])
    except ValueError as err:
        print(err)

from typing import Any
from pydantic import BaseModel, Field, ValidationError, model_validator


class MazeSetting(BaseModel):
    WIDTH: int = Field(ge=3)
    HEIGHT: int = Field(ge=3)
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool
    SEED: int | None = None

    @model_validator(mode="after")
    def check_setting(self) -> "MazeSetting":  # mypy R8: return type
        entry_x, entry_y = self.ENTRY
        exit_x, exit_y = self.EXIT
        if not (0 <= entry_x < self.WIDTH and 0 <= entry_y < self.HEIGHT):
            raise ValueError("ENTRY is out of bounds")
        if not (0 <= exit_x < self.WIDTH and 0 <= exit_y < self.HEIGHT):
            raise ValueError("EXIT is out of bounds")
        # Subject R38: entry and exit must be different cells
        if self.ENTRY == self.EXIT:
            raise ValueError("ENTRY and EXIT must be different cells")
        return self


# mypy R8: parse_value returns either bool, int, tuple[int,int], or str
def parse_value(value: str) -> bool | int | tuple[int, int] | str:
    value = value.strip()
    if value == "True":
        return True
    if value == "False":
        return False
    if "," in value:
        a, b = value.split(",", 1)
        try:
            return int(a), int(b)
        except Exception:
            return value
    try:
        return int(value)
    except ValueError:
        return value


# mypy R8: set_arg returns the parsed setting or None on error
def set_arg(filename: str) -> "MazeSetting | None":
    args: dict[str, Any] = {}
    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if '=' not in line:
                    raise ValueError("Invalid line. Missing '='")
                key, value = line.split('=', 1)
                args[key] = parse_value(value)
            if len(args) > 7:
                raise ValueError("Too many arguments in settings.")
            return MazeSetting(**args)
    except ValidationError as err:
        print(err.errors()[0]["msg"])
    except ValueError as err:
        print(err)
    except OSError as err:
        print(f"Cannot open '{filename}': {err.strerror or err}")
    # mypy R8: explicit None return for the error branches
    return None

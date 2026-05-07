from pydantic import BaseModel, Field, ValidationError, model_validator


class MazeSetting(BaseModel):
    """Validated configuration for the maze generator.

    Mandatory keys: WIDTH, HEIGHT, ENTRY, EXIT, OUTPUT_FILE, PERFECT.
    Optional keys: SEED (integer; if absent or commented, the maze is
    fully random).
    """
    WIDTH: int = Field(ge=3)
    HEIGHT: int = Field(ge=3)
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool
    SEED: int | None = None

    @model_validator(mode="after")
    def check_setting(self) -> "MazeSetting":
        entry_x, entry_y = self.ENTRY
        exit_x, exit_y = self.EXIT
        if not (0 <= entry_x < self.WIDTH and 0 <= entry_y < self.HEIGHT):
            raise ValueError("ENTRY is out of bounds")
        if not (0 <= exit_x < self.WIDTH and 0 <= exit_y < self.HEIGHT):
            raise ValueError("EXIT is out of bounds")
        if self.ENTRY == self.EXIT:
            raise ValueError("ENTRY and EXIT must be different cells")
        return self


def parse_value(value: str):
    """Parse a config value into bool, tuple[int,int], int, or str."""
    value = value.strip()
    if value == "True":
        return True
    if value == "False":
        return False
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


def set_arg(filename: str) -> MazeSetting | None:
    """Load and validate the configuration file.

    Returns the parsed MazeSetting, or None on error (after printing
    a message). Unknown keys are reported. SEED is accepted as an
    optional key.
    """
    valid_keys = {
        'WIDTH', 'HEIGHT', 'ENTRY', 'EXIT',
        'OUTPUT_FILE', 'PERFECT', 'SEED',
    }
    args: dict = {}
    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if '=' not in line:
                    raise ValueError("Invalid line. Missing '='")
                key, value = line.split('=', 1)
                key = key.strip()
                if key not in valid_keys:
                    raise ValueError(f"Unknown config key: {key}")
                args[key] = parse_value(value)
            return MazeSetting(**args)
    except FileNotFoundError:
        print(f"Config file not found: {filename}")
        return None
    except ValidationError as err:
        print(err.errors()[0]["msg"])
        return None
    except ValueError as err:
        print(err)
        return None

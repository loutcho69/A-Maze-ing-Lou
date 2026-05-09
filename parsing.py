import io
from pydantic import BaseModel, Field, ValidationError, model_validator


class MazeSetting(BaseModel):
    WIDTH: int = Field(ge=3)
    HEIGHT: int = Field(ge=3)
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool
    
    @model_validator(mode="after")
    def check_setting(self):
        entry_x, entry_y = self.ENTRY
        exit_x, exit_y = self.EXIT
        if not (0 <= entry_x < self.WIDTH and 0 <= entry_y < self.HEIGHT):
            raise ValueError("ENTRY is out of bounds")
        if not (0 <= exit_x < self.WIDTH and 0 <= exit_y < self.HEIGHT):
            raise ValueError("EXIT is out of bounds")
        return self

def parse_value(value):
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

def set_arg(filename):
    args = {}
    valid_key = ['WIDTH', 'HEIGHT', 'ENTRY', 'EXIT', 'OUTPUT_FILE', 'PERFECT']
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
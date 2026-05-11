"""
Maze configuration parser and validator.

This module defines:
- MazeSetting: validation of maze parameters using Pydantic
- parse_value: conversion of config file values
- set_arg: parsing of configuration files into validated settings
"""
from typing import Any
from pydantic import BaseModel, Field, ValidationError, model_validator


class MazeSetting(BaseModel):
    """Store and validate maze configuration settings."""

    WIDTH: int = Field(ge=3)
    HEIGHT: int = Field(ge=3)
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    OUTPUT_FILE: str
    PERFECT: bool
    SEED: int | None = None

    @model_validator(mode="after")
    def check_setting(self) -> "MazeSetting":
        """Validate entry and exit coordinates.

        Ensures that both coordinates are inside the maze bounds
        and that the entry and exit are different cells.

        Returns:
            MazeSetting: The validated settings object.

        Raises:
            ValueError: If coordinates are invalid or identical.
        """
        entry_x, entry_y = self.ENTRY
        exit_x, exit_y = self.EXIT

        if not (0 <= entry_x < self.WIDTH and
                0 <= entry_y < self.HEIGHT):
            raise ValueError("ENTRY is out of bounds")

        if not (0 <= exit_x < self.WIDTH and
                0 <= exit_y < self.HEIGHT):
            raise ValueError("EXIT is out of bounds")

        if self.ENTRY == self.EXIT:
            raise ValueError(
                "ENTRY and EXIT must be different cells"
            )

        return self


def parse_value(value: str) -> bool | int | tuple[int, int] | str:
    """Convert a configuration value to the appropriate Python type.

    The function attempts to parse:
    - booleans ("True" / "False"),
    - integer tuples ("x,y"),
    - integers,
    - or fallback strings.

    Args:
        value: Raw value read from the configuration file.

    Returns:
        A parsed boolean, integer, coordinate tuple, or string.
    """
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


def set_arg(filename: str) -> "MazeSetting | None":
    """Read and validate a maze configuration file.

    The file must contain KEY=VALUE pairs, one per line.
    Empty lines and comments starting with '#' are ignored.

    Args:
        filename: Path to the configuration file.

    Returns:
        MazeSetting | None:
            A validated MazeSetting object on success,
            or None if an error occurs.
    """
    args: dict[str, Any] = {}

    try:
        with open(filename, "r") as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith("#"):
                    continue

                if "=" not in line:
                    raise ValueError(
                        "Invalid line. Missing '='"
                    )

                key, value = line.split("=", 1)
                args[key] = parse_value(value)

            if len(args) > 7:
                raise ValueError(
                    "Too many arguments in settings."
                )

            return MazeSetting(**args)

    except ValidationError as err:
        print(err.errors()[0]["msg"])

    except ValueError as err:
        print(err)

    except OSError as err:
        print(
            f"Cannot open '{filename}': "
            f"{err.strerror or err}"
        )

    return None

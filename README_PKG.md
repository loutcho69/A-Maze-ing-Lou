# Mazegen

## Overview

`mazegen` is a reusable Python package for generating mazes programmatically.  
It provides a `MazeGenerator` class that can be imported and used in any project.

The module allows:
- Maze generation with customizable parameters (size, perfect mode, entry, exit)
- Access to the internal maze structure
- Retrieval of a computed solution path
- Print the generated maze

---

## Installation

After building the package:

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

```bash
from mazegen.maze_gen import MazeGenerator

gen = MazeGenerator(HEIGHT, WIDTH, ENTRY, EXIT, PERFECT)
```

Show the maze:

```bash
from mazegen.data import Color
from mazegen.print_maze import print_maze

print_maze(gen, Color.'COLOR'.value)
```

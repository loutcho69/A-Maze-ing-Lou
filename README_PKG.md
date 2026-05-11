## Using the `mazegen` Generator

The maze generation logic is exposed through the `MazeGenerator` class from the `mazegen` package.

---

## Running the program with a configuration file

The main program (`a_maze_ing.py`) requires a configuration file to run correctly.

### Running with a custom configuration file

```bash
python3 a_maze_ing.py path/to/config.txt
```

---

## Example `config.txt`

```ini
WIDTH=30
HEIGHT=15
ENTRY=0,0
EXIT=29,14
OUTPUT_FILE=maze.txt
PERFECT=True
SEED=42
```

### Required configuration fields

| Key | Description |
|---|---|
| `WIDTH` | Maze width |
| `HEIGHT` | Maze height |
| `ENTRY` | Entry coordinates |
| `EXIT` | Exit coordinates |
| `OUTPUT_FILE` | Output file path |
| `PERFECT` | Perfect or imperfect maze |

### Optional configuration fields

| Key | Description |
|---|---|
| `SEED` | Random seed for reproducible mazes |

---

## Basic instantiation and usage

```python
from mazegen import MazeGenerator

maze = MazeGenerator(
    width=20,
    height=10,
    entry=(0, 0),
    exit=(19, 9),
    perfect=True,
)

print(maze.to_output())
```

This creates a perfect maze of size `20x10` with an entry at `(0, 0)` and an exit at `(19, 9)`.

---

## Passing custom parameters

The generator accepts several optional parameters to customize generation behavior.

### Example with a custom seed and pattern

```python
from mazegen import MazeGenerator
from mazegen.patterns import FORTY_TWO

maze = MazeGenerator(
    width=30,
    height=15,
    entry=(0, 0),
    exit=(29, 14),
    perfect=False,
    pattern=FORTY_TWO,
    seed=42,
)
```

### Available parameters

| Parameter | Description |
|---|---|
| `width` | Maze width in cells |
| `height` | Maze height in cells |
| `entry` | Entry coordinates `(x, y)` |
| `exit` | Exit coordinates `(x, y)` |
| `perfect` | `True` for a perfect maze, `False` to allow loops |
| `pattern` | Optional embedded pattern (`FORTY_TWO`, `PACMAN`, `INVADER`, or `None`) |
| `seed` | Optional random seed for reproducible mazes |

Using the same `seed` always produces the same maze layout.

---

## Accessing the generated maze and its solution

The generated structure is directly accessible through the instance attributes.

### Accessing the maze grid

```python
print(maze.maze)
```

`maze.maze` contains the maze as a 2D list of hexadecimal wall values.

Example:

```python
[
    ['F', '9', '3'],
    ['C', '0', '6'],
]
```

---

### Accessing the solution path

```python
print(maze.path_solve)
```

`maze.path_solve` returns the solution path as a list of `(x, y)` coordinates from the entry to the exit.

Example:

```python
[(0, 0), (1, 0), (1, 1), (2, 1)]
```

---

### Exporting the maze to file format

```python
print(maze.to_output())
```

This returns the complete formatted output containing:
- the hexadecimal maze grid,
- entry coordinates,
- exit coordinates,
- and the shortest path encoded with `N`, `E`, `S`, `W`.
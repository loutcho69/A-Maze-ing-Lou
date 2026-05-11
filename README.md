_This project has been created as part of the 42 curriculum by lucpelle, lobroue._

# A-Maze-ing

A configurable maze generator written in Python. Reads a configuration file, generates a random maze (perfect or imperfect) with a hidden "42" pattern, displays it in the terminal with color, saves it to disk in a compact hexadecimal format, and lets the user interact with it through a small text menu.

---

## Table of contents

- [Description](#description)
- [Instructions](#instructions)
- [Configuration file](#configuration-file)
- [Output file format](#output-file-format)
- [Maze generation algorithm](#maze-generation-algorithm)
- [Reusable `mazegen` module](#reusable-mazegen-module)
- [Project structure](#project-structure)
- [Resources](#resources)
- [Team management](#team-management)

---

## Description

A-Maze-ing produces mazes that satisfy a precise set of geometric rules: every cell is reachable, the outer walls are closed, no fully open 3×3 area exists anywhere on the grid, and the cells forming a "42" appear in the middle as a fully closed block. The maze can be either **perfect** — exactly one path between entry and exit — or **imperfect**, with additional passages that create loops and shorter detours.

Two views of the same maze are produced:

- A **terminal rendering** with ANSI colors, including a visual highlight for the shortest path between the entry and the exit (toggleable from the menu).
- A **hexadecimal text file** where each cell is encoded as a single hex digit representing its four walls, followed by the entry coordinates, the exit coordinates, and the shortest path expressed as a sequence of `N`, `E`, `S`, `W` letters.

The whole maze-generation logic lives in a standalone `mazegen` package that can be installed and reused in any other Python project.

---

## Instructions

### Requirements

- Python 3.10 or later
- `pydantic` (installed automatically via the Makefile or `pip`)

### Quick start

```bash
make install     # install the package and its dependencies
make run         # run the program with the default config.txt
```

### Available Makefile targets

| Target        | What it does                                                              |
| ------------- | ------------------------------------------------------------------------- |
| `install`     | Install the project and its dependencies (`pydantic`) in editable mode.   |
| `run`         | Run `a_maze_ing.py` with the default `config.txt`.                        |
| `debug`       | Run the program under `pdb`, the Python debugger.                         |
| `clean`       | Remove caches (`__pycache__`, `.mypy_cache`) and the generated maze file. |
| `lint`        | Run `flake8` and `mypy` with the flags required by the subject.           |
| `lint-strict` | Run `flake8` and `mypy --strict`.                                         |

### Running with a custom configuration

```bash
python3 a_maze_ing.py path/to/your_config.txt
```

If no argument is given, the program falls back to `./config.txt`.

### Interactive menu

Once the program is running, the following options are available:

| Key | Action                                                |
| --- | ----------------------------------------------------- |
| `1` | Generate a new maze (random or seeded).               |
| `2` | Show or hide the shortest path from entry to exit.    |
| `3` | Cycle through wall colors.                            |
| `4` | Change the central pattern (42, Pac-Man, Invader).    |
| `5` | Cycle through pattern colors.                         |
| `6` | Quit.                                                 |

The menu is reprinted after every action — successful or not — so the user always knows what to do next. `Ctrl+C` and `Ctrl+D` exit gracefully without a traceback.

---

## Configuration file

The configuration file uses a simple `KEY=VALUE` syntax, one pair per line. Lines starting with `#` are treated as comments and ignored. Both upper and lower case keys are accepted.

### Mandatory keys

| Key           | Type            | Description                                              |
| ------------- | --------------- | -------------------------------------------------------- |
| `WIDTH`       | integer ≥ 3     | Number of cells along the horizontal axis.               |
| `HEIGHT`      | integer ≥ 3     | Number of cells along the vertical axis.                 |
| `ENTRY`       | `x,y` tuple     | Coordinates of the entry cell (must be inside the maze). |
| `EXIT`        | `x,y` tuple     | Coordinates of the exit cell (must differ from `ENTRY`). |
| `OUTPUT_FILE` | string          | Path of the file where the generated maze is written.    |
| `PERFECT`     | `True` / `False`| Whether the maze has exactly one path (`True`) or extra passages forming loops (`False`). |

### Optional keys

| Key    | Type    | Description                                                       |
| ------ | ------- | ----------------------------------------------------------------- |
| `SEED` | integer | Fixes the random seed, making generation **reproducible**.        |

### Example

```ini
WIDTH=30
HEIGHT=15
ENTRY=0,0
EXIT=25,5
OUTPUT_FILE=maze.txt
PERFECT=False
# SEED=42
```

### Error handling

Validation is performed by `pydantic`, which makes every error explicit and recoverable. The program never crashes on malformed input: missing keys, invalid types, out-of-bounds coordinates, identical entry and exit, broken syntax — each one produces a clear message and a clean exit.

---

## Output file format

The first generated maze is written to the path defined by `OUTPUT_FILE`. The file is rewritten every time a new maze is generated (commands `1` and `4`). The structure is:

```
HEIGHT lines of WIDTH hexadecimal digits  (one digit per cell)
<empty line>
entry_x,entry_y
exit_x,exit_y
NESW... (shortest path from entry to exit)
```

### Cell encoding (hex digit)

Each cell's value is the sum of four bits, one per wall:

| Bit | Direction | Value |
| --- | --------- | ----- |
| 0   | North     | 1     |
| 1   | East      | 2     |
| 2   | South     | 4     |
| 3   | West      | 8     |

A bit set to `1` means the corresponding wall is **closed**. A cell with all four walls closed has value `15` (`F` in hex). A cell with no walls has value `0`. The walls between two adjacent cells are always consistent: if a cell has its east wall closed, its right neighbor has its west wall closed too.

### Shortest path

The last line contains the moves needed to walk from `ENTRY` to `EXIT`, expressed as the letters `N`, `E`, `S`, `W`. Following these moves step by step, starting from the entry cell, leads exactly to the exit cell — and this sequence matches the path highlighted on the terminal when the user toggles it on with command `2`.

---

## Maze generation algorithm

A-Maze-ing uses a **randomized depth-first search** (also known as the **recursive backtracker**) to carve passages through a fully closed grid.

### How it works

1. The grid starts fully closed: every cell has its four walls intact (value `15`).
2. The cells belonging to the embedded pattern (e.g. "42") are pre-marked as visited so the carving step never opens any of their walls.
3. Starting from the entry cell, the algorithm picks a random unvisited neighbor, removes the wall between the current cell and that neighbor, then recurses from the neighbor.
4. When all neighbors of the current cell are visited, the algorithm backtracks and continues from the previous cell. This produces a perfect maze over all non-pattern cells (a spanning tree).
5. If the pattern isolates regions of the grid from the entry, an explicit reconnection step opens exactly one wall per disconnected component to restore full connectivity.
6. When `PERFECT=False`, an additional step opens roughly 15% of the remaining interior walls to create extra passages. Every candidate wall is checked beforehand to ensure it does not produce a fully open 3×3 area, as required by the subject.

The shortest path between entry and exit is then computed:
- in **perfect mode**, it is the unique path discovered during the DFS;
- in **imperfect mode**, it is recomputed with a **BFS** (breadth-first search), since the shortcuts created by the extra passages make the DFS path no longer optimal.

### Why this algorithm

The recursive backtracker was chosen for three reasons:

- **Subject compliance** — it natively produces a perfect maze, which is exactly what `PERFECT=True` requires. No additional work is needed to guarantee the "exactly one path" property.
- **Simple integration of the "42" pattern** — by marking the pattern cells as visited from the start, the DFS naturally avoids them. There is no need for a complex post-processing pass to "cut out" the pattern after generation.
- **Bias and visual quality** — recursive backtracking tends to produce long winding corridors with relatively few short dead-ends. This gives the rendered maze a satisfying, organic look that feels harder than the same maze generated by, e.g., Kruskal's or Prim's algorithm (which produce shorter, more uniform branches).

The same approach is used for both perfect and imperfect modes — the imperfect case is just the perfect maze with a controlled number of extra passages added afterwards. This keeps the code small and the two modes consistent.

### Reproducibility

Two equivalent ways to fix the random seed are available:

- **From the configuration file**: add `SEED=42` to your `config.txt`. The program calls `random.seed(...)` at startup, and two runs of `a_maze_ing.py` then produce byte-for-byte identical output.
- **From code**, when using the `mazegen` module as a library: pass `seed=42` to the `MazeGenerator` constructor. Useful for debugging, demos, and grading.

---

## Reusable `mazegen` module

The maze-generation logic is packaged as a standalone Python module named `mazegen`, distributed as a wheel (`mazegen-1.0.0-py3-none-any.whl`) and a source tarball (`mazegen-1.0.0.tar.gz`). Both files are present at the root of the repository.

### Installing in another project

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### Rebuilding from source

```bash
pip install build
python -m build
# produces dist/mazegen-1.0.0.tar.gz and dist/mazegen-1.0.0-py3-none-any.whl
```

### Using the `MazeGenerator` class

```python
from mazegen import MazeGenerator
from mazegen.patterns import FORTY_TWO

maze = MazeGenerator(
    width=30,
    height=15,
    entry=(0, 0),
    exit=(29, 14),
    perfect=True,
    pattern=FORTY_TWO,  # optional: None for a plain maze
    seed=42,            # optional: reproducible output when set
)

print(maze.maze)        # list of rows of hexadecimal cell values
print(maze.path_solve)  # list of (x, y) tuples from entry to exit
print(maze.to_output()) # full string in the output-file format
```

### Constructor parameters

| Parameter | Type                       | Description                                         |
| --------- | -------------------------- | --------------------------------------------------- |
| `width`   | `int` (≥ 3)                | Number of columns.                                  |
| `height`  | `int` (≥ 3)                | Number of rows.                                     |
| `entry`   | `tuple[int, int]`          | Entry coordinates.                                  |
| `exit`    | `tuple[int, int]`          | Exit coordinates (must differ from entry).          |
| `perfect` | `bool`                     | `True` for a perfect maze, `False` for cycles.      |
| `pattern` | `Pattern \| None`          | Optional embedded pattern (`FORTY_TWO`, `PACMAN`, `INVADER`, or `None`). |
| `seed`    | `int \| None`              | Optional random seed; identical seeds produce identical mazes. |

The `Pattern` class lets you define your own embedded patterns:

```python
from mazegen.patterns import Pattern

my_pattern = Pattern(name="custom", grid=(
    (1, 1, 1),
    (1, 0, 1),
    (1, 1, 1),
))
```

Each `1` marks a cell that must stay fully closed during generation.

---

## Project structure

```
.
├── a_maze_ing.py                     # Entry point: CLI, menu loop, interactive rendering
├── parsing.py                        # Configuration parser (pydantic validation)
├── output.py                         # Writes the generated maze to disk
├── config.txt                        # Default configuration
├── Makefile                          # install / run / debug / clean / lint / lint-strict
├── pyproject.toml                    # Package metadata for building the wheel
├── mazegen-1.0.0-py3-none-any.whl    # Reusable module (built artifact)
├── mazegen-1.0.0.tar.gz              # Reusable module (source distribution)
└── mazegen/                          # Reusable package (source)
    ├── __init__.py                   # Public API exports
    ├── data.py                       # Dir and Color enums
    ├── maze_gen.py                   # MazeGenerator class (DFS, BFS, cycle insertion)
    ├── patterns.py                   # Pattern class + FORTY_TWO, PACMAN, INVADER
    └── print_maze.py                 # Terminal rendering with ANSI colors
```

The split is intentional:

- The **app-level files** at the root (`a_maze_ing.py`, `parsing.py`, `output.py`, `config.txt`) handle user interaction, configuration, and file I/O. They are **not** part of the redistributable package.
- The **`mazegen/` package** contains only the pure generation and rendering logic. It has zero dependency on the configuration file format or the CLI, which makes it directly reusable from any other Python script.

---

## Team & Project Management

### Roles

| Member    | Role                                                         |
|-----------|--------------------------------------------------------------|
| lucpelle  | Parser, Backtracking, Mazegen, Menu settings interaction, Terminal display |
| lobroue   | Pathfinding, Imperfect mode, 42, Readme, BFS rework, Output file, Makefile |

### Planning

Initially we estimated roughly equal time between maze generation and the visual layer. In practice the interactive menu, rendering and wall-coherence validation took longer than expected, while the parsing and backtracking algorithm came together faster once the grid structure was stabilised.

### Retrospective

What worked well:
- Splitting the project into a reusable package (`mazegen`) and a CLI layer made testing and packaging easier.
- Using pydantic early greatly reduced parsing and validation bugs.
- The DFS approach integrated naturally with the embedded pattern system.

What could be improved:
- Some rendering and wall-consistency checks were implemented late and required refactoring.
- More automated tests would have helped catch edge cases earlier.
- The menu and rendering logic could be further separated from the core generation code.

### Tools Used

- **Python 3.10+**
- **Poetry** — dependency management and packaging
- **mypy** — static type checking
- **flake8** — code style linting
- **Git** — version control

---

## Resources

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive Backtracker](https://aryanab.medium.com/maze-generation-recursive-backtracking-5981bc5cc766)
- [Pathfinding — BFS](https://www.geeksforgeeks.org/dsa/count-number-of-ways-to-reach-destination-in-a-maze-using-bfs/)

### AI Usage

- README.md structure
- Differents explanations/clarifications of notions

All generated code and documentation was reviewed, understood, and adjusted by both team members before being committed.

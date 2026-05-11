# Makefile for A-Maze-ing — see subject chapter III.2

# Subject R11: install dependencies via pip (project uses pydantic via pyproject.toml)
install:
	pip install --break-system-packages -e .

# Subject R12: run the main script with the default config
run:
	python3 a_maze_ing.py config.txt

# Subject R13: run with the pdb debugger attached
debug:
	python3 -m pdb a_maze_ing.py config.txt

# Subject R14: remove caches and generated artifacts
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -f maze.txt

# Subject R15: lint = flake8 + mypy with the exact flags from the subject
lint:
	flake8 .
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

# Subject R16: optional strict lint
lint-strict:
	flake8 .
	mypy . --strict

.PHONY: install run debug clean lint lint-strict

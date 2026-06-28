# Contributing

## Development setup

```bash
git clone https://github.com/ernestopalacios/gdrive-utils.git
cd gdrive-utils
uv sync --group dev
```

## Running tests

```bash
uv run pytest -v
```

## Linting and type checking

```bash
uv run ruff check src tests
uv run mypy src
```

## Building documentation

```bash
uv run mkdocs build
```

Preview locally:

```bash
uv run mkdocs serve
```

## CI

Pull requests trigger GitHub Actions that run tests, linting, and type checking on Python 3.10, 3.11, and 3.12.

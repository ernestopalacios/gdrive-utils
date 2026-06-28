# Installation

## Requirements

- Python 3.10 or higher
- A Google service-account JSON credentials file
- The target Google Sheet must be shared with the service-account email

## Install from Git

```bash
uv add git+https://github.com/your-org/gdrive-utils.git
```

With pip:

```bash
pip install git+https://github.com/your-org/gdrive-utils.git
```

## Install with development dependencies

If you want to contribute or run tests locally:

```bash
git clone https://github.com/your-org/gdrive-utils.git
cd gdrive-utils
uv sync --group dev
```

This installs:

- `pytest` + `pytest-cov` — testing
- `ruff` — linting
- `mypy` — type checking
- `mkdocs-material` + `mkdocstrings[python]` — documentation

# Contributing to repro-zipfile

[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch) [![linting - Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v0.json)](https://github.com/charliermarsh/ruff) [![code style - black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black) [![types - mypy](https://img.shields.io/badge/types-mypy-blue.svg)](https://github.com/python/mypy)

## Report a bug or request a feature

Please file an issue in the [issue tracker](https://github.com/drivendataorg/repro-zipfile/issues).

## Developers guide

This project uses [Hatch](https://github.com/pypa/hatch) as its project management tool.

### Directory structure

This is a monorepo containing both the repro-zipfile library package and the rpzip CLI package. The root of the repository contains files relevant to the library package, and the CLI package is in the subdirectory `cli/`.

Tests for both packages are combined in `tests/`.

### Tests

To run tests in your current environment, you should install from source with the `tests` extra to additionally install test dependencies (pytest). Then, use pytest to run the tests.

```bash
# Install with test dependencies
pip install .[tests]
# Run tests
pytest tests.py
```

To run tests on the full test matrix, you should use Hatch:

```bash
hatch run tests:test
```

To run on a specific test environment, you reference that environment's name:

```bash
hatch run tests.py3.11:test
```

To see all test environment names, run:

```bash
hatch env show tests
```

### Code Quality: Linting and Static Typechecking

All code quality dependencies are installed in the default environment.

To run linting:

```bash
hatch run lint
```

To run static typechecking:

```bash
hatch run typecheck
```

### Configuring IDEs with the Virtual Environment

The default hatch environment is configured to be located in `./venv/`. To configure your IDE to use it, point it at that environment's Python interpreter located at `./venv/bin/python`.

### Releases and publishing to PyPI

The release process of building and publishing the packages is done using GitHub Actions CI. There are two workflows:

- `release-lib` — for the repro-zipfile library package
- `release-cli` — for the rpzip CLI package

Each package should be released independently.

To trigger a release, publish a release through the GitHub web UI. Use a different tag naming scheme to determine which release workflow you trigger:

- `v*` (e.g., `v0.1.0`) to publish repro-zipfile
- `cli-v*` (e.g., `cli-v0.1.0`) to publish rpzip

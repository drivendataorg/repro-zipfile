# Contributing to repro-zipfile

[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![types - mypy](https://img.shields.io/badge/types-mypy-blue.svg)](https://github.com/python/mypy)

## Report a bug or request a feature

Please file an issue in the [issue tracker](https://github.com/drivendataorg/repro-zipfile/issues).

## Developers guide

This project uses [uv](https://github.com/astral-sh/uv) as its project management tool and [Just](https://github.com/casey/just) as a task runner.

### Directory structure

This is a monorepo containing both the repro-zipfile library package and the rpzip CLI package. The root of the repository contains files relevant to the library package, and the CLI package is in the subdirectory `cli/`.

Tests for both packages are combined in `tests/`.

### Configuring the development environment

Run:

```bash
just sync
```

This will create a virtual environment located at `.venv/`.

### Tests

To run tests for a single version of Python, use:

```bash
just test
```

To specify a version of Python, use for example:

```bash
just python=3.11 test
```

To run tests on the full test matrix, use:

```bash
just test-all
```

### Code Quality: Linting and Static Typechecking

All code quality dependencies are installed in the default environment.

To run linting:

```bash
just lint
```

To run static typechecking:

```bash
just typecheck
```

### Releases and publishing to PyPI

The release process of building and publishing the packages is done using GitHub Actions CI. There are two workflows:

- **Release Library** — for the repro-zipfile library package
- **Release CLI** — for the rpzip CLI package

Each package should be released independently.

For both packages:

1. Update the changelog
2. Ensure the static version declared in associated `pyproject.toml` is the version number of the new release
3. Run the appropriate release workflow using workflow dispatch, entering the intended versino number as an input parameter

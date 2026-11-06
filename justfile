# Keep in sync with just-version in .github/workflows/*.yml
set minimum-version := '1.55.0'

python := shell("cat .python-version")

# Print this help documentation
help:
    just --list

# Sync dev environment dependencies
sync:
    uv sync --all-extras

# Run linting (passes through args)
lint *args:
    uv run -- ruff format --check {{args}}
    uv run -- ruff check {{args}}

# Run formatting (passes through args)
format *args:
    uv run -- ruff format {{args}}
    uv run -- ruff check --fix {{args}}

# Audit GitHub Actions workflows with zizmor (passes through args)
zizmor *args:
    uvx --exclude-newer "7 days" zizmor .github/ {{args}}

# Run static typechecking with all typecheckers
[arg("python", long)]
typecheck python=python:
    just typecheck-mypy --python={{python}}
    just typecheck-pyrefly --python={{python}}
    just typecheck-ty --python={{python}}

# Run static typechecking with mypy
[arg("python", long)]
typecheck-mypy python=python:
    # Standard type checking excluding stub file and stub usage checks
    uv run --python={{python}} --isolated --all-extras --no-dev --group typecheck --group tests -- \
        mypy . --exclude '(\.pyi|typechecks\.py)$'
    # Strict type checking on stub file and stub usage checks
    uv run --python={{python}} --isolated --all-extras --no-dev --group typecheck --group tests -- \
        mypy src/repro_zipfile tests/typechecks.py --strict
    # Check stub
    uv run --python={{python}} --isolated --all-extras --no-dev --group typecheck -- \
        python -m mypy.stubtest repro_zipfile

# Run static typechecking of the stub with pyrefly (passes through args)
[arg("python", long)]
typecheck-pyrefly python=python *args:
    uv run --python={{python}} --isolated --all-extras --no-dev --group typecheck -- \
        pyrefly check --python-version={{python}} {{args}}

# Run static typechecking of the stub with ty (passes through args)
[arg("python", long)]
typecheck-ty python=python *args:
    uv run --python={{python}} --isolated --all-extras --no-dev --group typecheck -- \
        ty check --python-version={{python}} {{args}}

# Run tests (passes through args)
[arg("python", long)]
test python=python *args:
    uv run --python={{python}} --isolated --no-editable --all-extras --no-dev --group tests \
        --reinstall-package rpzip --reinstall-package repro-zipfile -- \
        python -I -m pytest {{args}}

# Run all tests with Python version matrix
test-all:
    for python in 3.10 3.11.3 3.11 3.12 3.13 3.14 3.15; do \
        just test --python=$python; \
    done

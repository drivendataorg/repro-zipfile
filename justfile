# Keep in sync with just-version in .github/workflows/*.yml
set minimum-version := '1.55.0'

python := shell("cat .python-version")

# Print this help documentation
help:
    just --list

# Sync dev environment dependencies
sync:
    uv sync --all-extras

# Run linting
lint:
    ruff format --check
    ruff check

# Run formatting
format:
    ruff format
    ruff check --fix

# Audit GitHub Actions workflows with zizmor (passes through args)
zizmor *args:
    uvx --exclude-newer "7 days" zizmor .github/ {{args}}

# Run static typechecking
typecheck:
    # Standard type checking excluding stub file
    mypy . --install-types --non-interactive --exclude '\\.pyi$'
    # Strict type checking on repro_zipfile with stub file
    mypy src/repro_zipfile --install-types --non-interactive --strict
    # Check stub
    python -m mypy.stubtest repro_zipfile
# Run tests
test *args:
    uv run --python {{python}} --no-editable --all-extras --no-dev --group test --isolated \
        --reinstall-package rpzip --reinstall-package repro-zipfile \
        python -I -m pytest {{args}}

# Run all tests with Python version matrix
test-all:
    for python in 3.10 3.11.3 3.11 3.12 3.13 3.14 3.15; do \
        just python=$python test; \
    done

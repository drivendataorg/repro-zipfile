import os
from typing import Generator
from pathlib import Path

import pytest
from pytest_cases import fixture_union


@pytest.fixture
def abs_path(tmp_path: Path) -> Path:
    """Fixture that returns a temporary directory as an absolute Path object."""
    return tmp_path


@pytest.fixture
def rel_path(tmp_path: Path) -> Generator[Path, None, None]:
    """Fixture that sets a temporary directory as the current working directory and returns a
    relative path to it."""
    orig_wd = Path.cwd()
    os.chdir(tmp_path)
    yield Path()
    os.chdir(orig_wd)


base_path = fixture_union("base_path", ["rel_path", "abs_path"])

from glob import glob
import subprocess
import sys

from typer.testing import CliRunner

from repro_zipfile import __version__ as repro_zipfile_version
from rpzip import __version__ as rpzip_version
from rpzip import app
from tests.utils import assert_archive_contents_equals, dir_tree_factory, file_factory

runner = CliRunner()


def test_zip_single_file(base_path):
    data_file = file_factory(base_path)

    rpzip_out = base_path / "rpzip.zip"
    rpzip_args = [str(rpzip_out), str(data_file)]
    rpzip_result = runner.invoke(app, rpzip_args)
    assert rpzip_result.exit_code == 0, rpzip_args

    zip_out = base_path / "zip.zip"
    zip_cmd = ["zip", str(zip_out), str(data_file)]
    zip_result = subprocess.run(zip_cmd)
    assert zip_result.returncode == 0, zip_cmd

    assert_archive_contents_equals(rpzip_out, zip_out)


def test_zip_directory(base_path):
    """Single directory, not recursive."""
    dir_tree = dir_tree_factory(base_path)

    rpzip_out = base_path / "rpzip.zip"
    rpzip_args = [str(rpzip_out), str(dir_tree)]
    rpzip_result = runner.invoke(app, rpzip_args)
    assert rpzip_result.exit_code == 0, rpzip_args

    zip_out = base_path / "zip.zip"
    zip_cmd = ["zip", str(zip_out), str(dir_tree)]
    zip_result = subprocess.run(zip_cmd)
    assert zip_result.returncode == 0, zip_cmd

    assert_archive_contents_equals(rpzip_out, zip_out)


def test_zip_directory_recursive(base_path):
    """Single input directory with recursive -r flag."""
    dir_tree = dir_tree_factory(base_path)

    rpzip_out = base_path / "rpzip.zip"
    rpzip_args = ["-r", str(rpzip_out), str(dir_tree)]
    rpzip_result = runner.invoke(app, rpzip_args)
    assert rpzip_result.exit_code == 0, rpzip_args

    zip_out = base_path / "zip.zip"
    zip_cmd = ["zip", "-r", str(zip_out), str(dir_tree)]
    zip_result = subprocess.run(zip_cmd)
    assert zip_result.returncode == 0, zip_cmd

    assert_archive_contents_equals(rpzip_out, zip_out)


def test_zip_multiple_recursive(base_path):
    """Mulitiple input files with recursive -r flag."""
    dir_tree = dir_tree_factory(base_path)

    rpzip_out = base_path / "rpzip.zip"
    rpzip_args = ["-r", str(rpzip_out)] + glob(str(dir_tree))
    rpzip_result = runner.invoke(app, rpzip_args)
    assert rpzip_result.exit_code == 0, rpzip_args

    zip_out = base_path / "zip.zip"
    zip_cmd = ["zip", "-r", str(zip_out)] + glob(str(dir_tree))
    zip_result = subprocess.run(zip_cmd)
    assert zip_result.returncode == 0, zip_cmd

    assert_archive_contents_equals(rpzip_out, zip_out)


def test_zip_no_suffix(base_path):
    data_file = file_factory(base_path)

    rpzip_out = base_path / "rpzip.zip"
    rpzip_args = [str(rpzip_out.with_suffix("")), str(data_file)]
    rpzip_result = runner.invoke(app, rpzip_args)
    assert rpzip_result.exit_code == 0, rpzip_args

    zip_out = base_path / "zip.zip"
    zip_cmd = ["zip", str(zip_out.with_suffix("")), str(data_file)]
    zip_result = subprocess.run(zip_cmd)
    assert zip_result.returncode == 0, zip_cmd

    assert_archive_contents_equals(rpzip_out, zip_out)


def test_verbosity(rel_path):
    """Adjustment of verbosity with -v and -q."""
    data_file = file_factory(rel_path)
    rpzip_out = rel_path / "rpzip.zip"

    # Base case, should be INFO level
    rpzip_args = [str(rpzip_out), str(data_file)]
    rpzip_result = runner.invoke(app, rpzip_args)
    assert rpzip_result.exit_code == 0, rpzip_args
    assert "INFO" in rpzip_result.output
    assert "DEBUG" not in rpzip_result.output

    # With -v, should be DEBUG level
    rpzip_args = [str(rpzip_out), str(data_file), "-v"]
    rpzip_result = runner.invoke(app, rpzip_args)
    assert rpzip_result.exit_code == 0, rpzip_args
    assert "INFO" in rpzip_result.output
    assert "DEBUG" in rpzip_result.output

    # With -q, should be no output
    rpzip_args = [str(rpzip_out), str(data_file), "-q"]
    rpzip_result = runner.invoke(app, rpzip_args)
    assert rpzip_result.exit_code == 0, rpzip_args
    assert rpzip_result.output.strip() == ""


def test_version():
    """With --version flag."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    output_lines = result.output.split("\n")
    assert output_lines[0].startswith("repro-zipfile ")
    assert output_lines[0].endswith(f"v{repro_zipfile_version}")
    assert output_lines[1].startswith("rpzip ")
    assert output_lines[1].endswith(f"v{rpzip_version}")


def test_python_dash_m_invocation():
    result = subprocess.run(
        [sys.executable, "-m", "rpzip", "--help"],
        capture_output=True,
        text=True,
        universal_newlines=True,
    )
    assert result.returncode == 0
    assert "Usage: python -m rpzip" in result.stdout

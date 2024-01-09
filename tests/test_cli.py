from glob import glob
import subprocess
import sys

from typer.testing import CliRunner

from repro_zipfile import __version__ as repro_zipfile_version
from repro_zipfile_cli import __version__ as repro_zipfile_cli_version
from repro_zipfile_cli import app
from tests.utils import assert_archive_contents_equals, dir_tree_factory, file_factory

runner = CliRunner()


def test_zip_single_file(base_path):
    data_file = file_factory(base_path)

    repzip_out = base_path / "repzip.zip"
    repzip_args = [str(repzip_out), str(data_file)]
    repzip_result = runner.invoke(app, repzip_args)
    assert repzip_result.exit_code == 0, repzip_args

    zip_out = base_path / "zip.zip"
    zip_cmd = ["zip", str(zip_out), str(data_file)]
    zip_result = subprocess.run(zip_cmd)
    assert zip_result.returncode == 0, zip_cmd

    assert_archive_contents_equals(repzip_out, zip_out)


def test_zip_directory(base_path):
    """Single directory, not recursive."""
    dir_tree = dir_tree_factory(base_path)

    repzip_out = base_path / "repzip.zip"
    repzip_args = [str(repzip_out), str(dir_tree)]
    repzip_result = runner.invoke(app, repzip_args)
    assert repzip_result.exit_code == 0, repzip_args

    zip_out = base_path / "zip.zip"
    zip_cmd = ["zip", str(zip_out), str(dir_tree)]
    zip_result = subprocess.run(zip_cmd)
    assert zip_result.returncode == 0, zip_cmd

    assert_archive_contents_equals(repzip_out, zip_out)


def test_zip_directory_recursive(base_path):
    """Single input directory with recursive -r flag."""
    dir_tree = dir_tree_factory(base_path)

    repzip_out = base_path / "repzip.zip"
    repzip_args = ["-r", str(repzip_out), str(dir_tree)]
    repzip_result = runner.invoke(app, repzip_args)
    assert repzip_result.exit_code == 0, repzip_args

    zip_out = base_path / "zip.zip"
    zip_cmd = ["zip", "-r", str(zip_out), str(dir_tree)]
    zip_result = subprocess.run(zip_cmd)
    assert zip_result.returncode == 0, zip_cmd

    assert_archive_contents_equals(repzip_out, zip_out)


def test_zip_multiple_recursive(base_path):
    """Mulitiple input files with recursive -r flag."""
    dir_tree = dir_tree_factory(base_path)

    repzip_out = base_path / "repzip.zip"
    repzip_args = ["-r", str(repzip_out)] + glob(str(dir_tree))
    repzip_result = runner.invoke(app, repzip_args)
    assert repzip_result.exit_code == 0, repzip_args

    zip_out = base_path / "zip.zip"
    zip_cmd = ["zip", "-r", str(zip_out)] + glob(str(dir_tree))
    zip_result = subprocess.run(zip_cmd)
    assert zip_result.returncode == 0, zip_cmd

    assert_archive_contents_equals(repzip_out, zip_out)


def test_zip_no_suffix(base_path):
    data_file = file_factory(base_path)

    repzip_out = base_path / "repzip.zip"
    repzip_args = [str(repzip_out.with_suffix("")), str(data_file)]
    repzip_result = runner.invoke(app, repzip_args)
    assert repzip_result.exit_code == 0, repzip_args

    zip_out = base_path / "zip.zip"
    zip_cmd = ["zip", str(zip_out.with_suffix("")), str(data_file)]
    zip_result = subprocess.run(zip_cmd)
    assert zip_result.returncode == 0, zip_cmd

    assert_archive_contents_equals(repzip_out, zip_out)


def test_verbosity(rel_path):
    """Adjustment of verbosity with -v and -q."""
    data_file = file_factory(rel_path)
    repzip_out = rel_path / "repzip.zip"

    # Base case, should be INFO level
    repzip_args = [str(repzip_out), str(data_file)]
    repzip_result = runner.invoke(app, repzip_args)
    assert repzip_result.exit_code == 0, repzip_args
    assert "INFO" in repzip_result.output
    assert "DEBUG" not in repzip_result.output

    # With -v, should be DEBUG level
    repzip_args = [str(repzip_out), str(data_file), "-v"]
    repzip_result = runner.invoke(app, repzip_args)
    assert repzip_result.exit_code == 0, repzip_args
    assert "INFO" in repzip_result.output
    assert "DEBUG" in repzip_result.output

    # With -q, should be no output
    repzip_args = [str(repzip_out), str(data_file), "-q"]
    repzip_result = runner.invoke(app, repzip_args)
    assert repzip_result.exit_code == 0, repzip_args
    assert repzip_result.output.strip() == ""


def test_version():
    """With --version flag."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    output_lines = result.output.split("\n")
    assert output_lines[0].startswith("repro-zipfile ")
    assert output_lines[0].endswith(f"v{repro_zipfile_version}")
    assert output_lines[1].startswith("repro-zipfile-cli ")
    assert output_lines[1].endswith(f"v{repro_zipfile_cli_version}")


def test_python_dash_m_invocation():
    result = subprocess.run(
        [sys.executable, "-m", "repro_zipfile_cli", "--help"],
        capture_output=True,
        text=True,
        universal_newlines=True,
    )
    assert result.returncode == 0
    assert "Usage: python -m repro_zipfile_cli" in result.stdout

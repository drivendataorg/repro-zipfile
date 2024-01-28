import logging
from pathlib import Path
import sys
from typing import List, Optional

try:
    from typing import Annotated
except ImportError:
    from typing_extensions import Annotated

import typer

from repro_zipfile import ReproducibleZipFile
from repro_zipfile import __version__ as repro_zipfile_version

__version__ = "0.1.0"

app = typer.Typer()


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def version_callback(value: bool):
    if value:
        print(f"repro-zipfile v{repro_zipfile_version}")
        print(f"rpzip (rpzip) v{__version__}")
        raise typer.Exit()


@app.command(context_settings={"obj": {}})
def rpzip(
    out_file: Annotated[
        str,
        typer.Argument(help="Path of output archive. '.zip' suffix will be added if not present."),
    ],
    in_list: Annotated[List[str], typer.Argument(help="Files to add to the archive.")],
    recurse_paths: Annotated[
        bool, typer.Option("--recurse-paths", "-r", help="Recurse into directories.")
    ] = False,
    quiet: Annotated[
        int,
        typer.Option(
            "--quiet",
            "-q",
            count=True,
            show_default=False,
            help="Use to decrease log verbosity.",
        ),
    ] = 0,
    verbose: Annotated[
        int,
        typer.Option(
            "--verbose",
            "-v",
            count=True,
            show_default=False,
            help="Use to increase log verbosity.",
        ),
    ] = 0,
    version: Annotated[
        Optional[bool],
        typer.Option(
            "--version",
            help="Print version number and exit.",
            callback=version_callback,
        ),
    ] = None,
):
    """A lightweight replacement for zip for most simple cases. Use it to compress and package
    files in ZIP archives, but reproducibly/deterministicly.

    Example commands:

    \b
      rpzip archive.zip some_file.txt        # Archive one file
      rpzip archive.zip file1.txt file2.txt  # Archive two files
      rpzip archive.zip some_dir/*.txt       # Archive with glob
      rpzip -r archive.zip some_dir/         # Archive directory recursively
    """
    # Set up logger
    log_level = logging.INFO + 10 * quiet - 10 * verbose
    logger.setLevel(log_level)
    log_handler = logging.StreamHandler()
    logger.addHandler(log_handler)
    prog_name = Path(sys.argv[0]).stem
    log_formatter = logging.Formatter(f"%(asctime)s | {prog_name} | %(levelname)s | %(message)s")
    log_handler.setFormatter(log_formatter)

    logger.debug("out_file: %s", out_file)
    logger.debug("in_list: %s", in_list)
    logger.debug("recurse_paths: %s", recurse_paths)

    # Set output archive path
    if not out_file.endswith(".zip"):
        out_path = Path(out_file).with_suffix(".zip").resolve()
    else:
        out_path = Path(out_file).resolve()
    logger.debug("writing to: %s", out_path)

    # Process inputs
    in_paths = set(Path(p) for p in in_list)
    if recurse_paths:
        for path in frozenset(in_paths):
            if path.is_dir():
                in_paths.update(path.glob("**/*"))

    with ReproducibleZipFile(out_path, "w") as zp:
        for path in sorted(in_paths):
            logger.info("adding: %s", path)
            zp.write(path)


if __name__ == "__main__":
    app(prog_name="python -m rpzip")

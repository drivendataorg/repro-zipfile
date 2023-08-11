"""A demo script that shows repro_zipfile's reproducible output in contrast with the standard
library module zipfile's nonreproducible output.
"""

import hashlib
from pathlib import Path
from tempfile import TemporaryDirectory
from time import sleep
from zipfile import ZipFile

from repro_zipfile import ReproducibleZipFile

example_dir = Path(__file__).parent


def create_archive(zip_class, outfile: Path):
    with zip_class(outfile, "w") as zp:
        # Use write to add a file to the archive
        zp.write(example_dir / "data.txt", arcname="data.txt")
        # Or writestr to write data to the archive
        zp.writestr("lore.txt", data="goodbye")


with TemporaryDirectory() as tempdir_name:
    tempdir = Path(tempdir_name)

    cases = [
        (ZipFile, tempdir / "zipfile-1.zip"),
        (ZipFile, tempdir / "zipfile-2.zip"),
        (ReproducibleZipFile, tempdir / "repro_zipfile-1.zip"),
        (ReproducibleZipFile, tempdir / "repro_zipfile-2.zip"),
    ]

    for case in cases:
        create_archive(*case)
        sleep(2)

    for _, outfile in cases:
        print(outfile.name, hashlib.md5(outfile.read_bytes()).hexdigest())

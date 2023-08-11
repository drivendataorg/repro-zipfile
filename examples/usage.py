"""Basic usage example of repro_zipfile.
"""

from pathlib import Path

from repro_zipfile import ReproducibleZipFile

example_dir = Path(__file__).parent

with ReproducibleZipFile(example_dir / "archive.zip", "w") as zp:
    # Use write to add a file to the archive
    zp.write(example_dir / "data.txt", arcname="data.txt")
    # Or writestr to write data to the archive
    zp.writestr("lore.txt", data="goodbye")

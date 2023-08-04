import hashlib
from pathlib import Path
from time import sleep
import uuid

from reprozip import ReproducibleZipFile


def data_factory():
    """Utility function to generate random data."""
    return str(uuid.uuid4())


def hash_file(path: Path):
    """Utility function to calculate the hash of a file's contents."""
    return hashlib.md5(path.read_bytes()).hexdigest()


def test_write_same_file_different_mtime(tmp_path):
    data = data_factory()
    data_file = tmp_path / "data.txt"

    data_file.write_text(data)
    with ReproducibleZipFile(tmp_path / "zip1.zip", "w") as zp:
        zp.write(data_file)

    sleep(2)

    data_file.write_text(data)
    with ReproducibleZipFile(tmp_path / "zip2.zip", "w") as zp:
        zp.write(data_file)

    assert hash_file(tmp_path / "zip1.zip") == hash_file(tmp_path / "zip2.zip")


def test_writestr_same_data_different_mtime(tmp_path):
    data = data_factory()

    with ReproducibleZipFile(tmp_path / "zip1.zip", "w") as zp:
        zp.writestr("data.txt", data=data)

    sleep(2)

    with ReproducibleZipFile(tmp_path / "zip2.zip", "w") as zp:
        zp.writestr("data.txt", data=data)

    assert hash_file(tmp_path / "zip1.zip") == hash_file(tmp_path / "zip2.zip")

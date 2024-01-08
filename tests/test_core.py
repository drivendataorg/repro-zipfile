import platform
from time import sleep
from zipfile import ZipFile, ZipInfo

from repro_zipfile import ReproducibleZipFile
from tests.utils import (
    assert_archive_contents_equals,
    data_factory,
    dir_tree_factory,
    file_factory,
    hash_file,
    umask,
)


def test_write_dir_tree_mtime(base_path):
    """Archiving a directory tree works with different modified time."""
    dir_tree = dir_tree_factory(base_path)

    # Create base ReproducibleZipFile archive
    repro_zipfile_arc1 = base_path / "repro_zipfile1.zip"
    with ReproducibleZipFile(repro_zipfile_arc1, "w") as zp:
        for path in sorted(dir_tree.glob("**/*")):
            zp.write(path)

    # Create regular ZipFile archive for comparison
    zipfile_arc1 = base_path / "zipfile1.zip"
    with ZipFile(zipfile_arc1, "w") as zp:
        for path in sorted(dir_tree.glob("**/*")):
            zp.write(path)

    # Sleep to update modified times, change permissions
    sleep(2)
    for path in dir_tree.glob("**/*"):
        path.touch()

    # Create second ReproducibleZipFile archive after delay
    repro_zipfile_arc2 = base_path / "repro_zipfile2.zip"
    with ReproducibleZipFile(repro_zipfile_arc2, "w") as zp:
        for path in sorted(dir_tree.glob("**/*")):
            zp.write(path)

    # Create second regular ZipFile archive for comparison after delay
    zipfile_arc2 = base_path / "zipfile2.zip"
    with ZipFile(zipfile_arc2, "w") as zp:
        for path in sorted(dir_tree.glob("**/*")):
            zp.write(path)

    # All four archives should have identical content
    assert_archive_contents_equals(repro_zipfile_arc1, zipfile_arc1)
    assert_archive_contents_equals(repro_zipfile_arc1, repro_zipfile_arc2)
    assert_archive_contents_equals(repro_zipfile_arc1, zipfile_arc2)

    # ReproducibleZipFile hashes should match; ZipFile hashes should not
    assert hash_file(repro_zipfile_arc1) == hash_file(repro_zipfile_arc2)
    assert hash_file(zipfile_arc1) != hash_file(zipfile_arc2)


def test_write_dir_tree_mode(base_path):
    """Archiving a directory tree works with different permission modes."""
    with umask(0o022):
        dir_tree = dir_tree_factory(base_path)

    # Create base ReproducibleZipFile archive
    repro_zipfile_arc1 = base_path / "repro_zipfile1.zip"
    with ReproducibleZipFile(repro_zipfile_arc1, "w") as zp:
        for path in sorted(dir_tree.glob("**/*")):
            zp.write(path)

    # Create regular ZipFile archive for comparison
    zipfile_arc1 = base_path / "zipfile1.zip"
    with ZipFile(zipfile_arc1, "w") as zp:
        for path in sorted(dir_tree.glob("**/*")):
            zp.write(path)

    # Change permissions
    with umask(0o002) as mask:
        dir_tree.chmod(mode=0o777 ^ mask)
        for path in dir_tree.glob("**/*"):
            if path.is_file():
                path.chmod(mode=0o666 ^ mask)
            else:
                path.chmod(mode=0o777 ^ mask)

    # Create second ReproducibleZipFile archive after delay
    repro_zipfile_arc2 = base_path / "repro_zipfile2.zip"
    with ReproducibleZipFile(repro_zipfile_arc2, "w") as zp:
        for path in sorted(dir_tree.glob("**/*")):
            zp.write(path)

    # Create second regular ZipFile archive for comparison after delay
    zipfile_arc2 = base_path / "zipfile2.zip"
    with ZipFile(zipfile_arc2, "w") as zp:
        for path in sorted(dir_tree.glob("**/*")):
            zp.write(path)

    # All four archives should have identical content
    assert_archive_contents_equals(repro_zipfile_arc1, zipfile_arc1)
    assert_archive_contents_equals(repro_zipfile_arc1, repro_zipfile_arc2)
    assert_archive_contents_equals(repro_zipfile_arc1, zipfile_arc2)

    # ReproducibleZipFile hashes should match; ZipFile hashes should not
    assert hash_file(repro_zipfile_arc1) == hash_file(repro_zipfile_arc2)
    if platform.system() != "Windows":
        # Windows doesn't seem to actually make them different
        assert hash_file(zipfile_arc1) != hash_file(zipfile_arc2)


def test_write_dir_tree_string_paths(rel_path):
    """Archiving a directory tree works."""
    dir_tree = dir_tree_factory(rel_path)

    # Create base ReproducibleZipFile archive
    repro_zipfile_arc1 = rel_path / "repro_zipfile1.zip"
    with ReproducibleZipFile(repro_zipfile_arc1, "w") as zp:
        for path in sorted(dir_tree.glob("**/*")):
            zp.write(str(path))

    # Create regular ZipFile archive for comparison
    zipfile_arc1 = rel_path / "zipfile1.zip"
    with ZipFile(zipfile_arc1, "w") as zp:
        for path in sorted(dir_tree.glob("**/*")):
            zp.write(str(path))

    # Update modified times
    sleep(2)
    for path in dir_tree.glob("**/*"):
        path.touch()

    # Create second ReproducibleZipFile archive after delay
    repro_zipfile_arc2 = rel_path / "repro_zipfile2.zip"
    with ReproducibleZipFile(repro_zipfile_arc2, "w") as zp:
        for path in sorted(dir_tree.glob("**/*")):
            zp.write(str(path))

    # Create second regular ZipFile archive for comparison after delay
    zipfile_arc2 = rel_path / "zipfile2.zip"
    with ZipFile(zipfile_arc2, "w") as zp:
        for path in sorted(dir_tree.glob("**/*")):
            zp.write(str(path))

    # All four archives should have identical content
    assert_archive_contents_equals(repro_zipfile_arc1, zipfile_arc1)
    assert_archive_contents_equals(repro_zipfile_arc1, repro_zipfile_arc2)
    assert_archive_contents_equals(repro_zipfile_arc1, zipfile_arc2)

    # ReproducibleZipFile hashes should match; ZipFile hashes should not
    assert hash_file(repro_zipfile_arc1) == hash_file(repro_zipfile_arc2)
    assert hash_file(zipfile_arc1) != hash_file(zipfile_arc2)


def test_write_single_file(base_path):
    """Writing the same file with different mtime produces the same hash."""
    data_file = file_factory(base_path)

    repro_zip1 = base_path / "repro_zip1.zip"
    with ReproducibleZipFile(repro_zip1, "w") as zp:
        zp.write(data_file)

    zip1 = base_path / "zip1.zip"
    with ZipFile(zip1, "w") as zp:
        zp.write(data_file)

    print(data_file.stat())
    sleep(2)
    data_file.touch()
    print(data_file.stat())

    repro_zip2 = base_path / "repro_zip2.zip"
    with ReproducibleZipFile(repro_zip2, "w") as zp:
        zp.write(data_file)

    zip2 = base_path / "zip2.zip"
    with ZipFile(zip2, "w") as zp:
        zp.write(data_file)

    # All four archives should have identical content
    assert_archive_contents_equals(repro_zip1, zip1)
    assert_archive_contents_equals(repro_zip1, repro_zip2)
    assert_archive_contents_equals(repro_zip1, zip2)

    # ReproducibleZipFile hashes should match; ZipFile hashes should not
    assert hash_file(repro_zip1) == hash_file(repro_zip2)
    assert hash_file(zip1) != hash_file(zip2)


def test_write_single_file_source_date_epoch(base_path, monkeypatch):
    """Writing the same file with different mtime with SOURCE_DATE_EPOCH set produces the
    same hash."""

    data_file = file_factory(base_path)

    arc_base = base_path / "base.zip"
    with ReproducibleZipFile(arc_base, "w") as zp:
        zp.write(data_file)

    monkeypatch.setenv("SOURCE_DATE_EPOCH", "1691732367")

    # With SOURCE_DATE_EPOCH set
    arc_sde1 = base_path / "with_sde1.zip"
    with ReproducibleZipFile(arc_sde1, "w") as zp:
        zp.write(data_file)

    sleep(2)
    data_file.touch()

    arc_sde2 = base_path / "with_sde2.zip"
    with ReproducibleZipFile(arc_sde2, "w") as zp:
        zp.write(data_file)

    # All four archives should have identical content
    assert_archive_contents_equals(arc_base, arc_sde1)
    assert_archive_contents_equals(arc_base, arc_sde2)

    # Base archive hash should match neither, two archives with SOURCE_DATE_EPOCH should match
    assert hash_file(arc_base) != hash_file(arc_sde1)
    assert hash_file(arc_sde1) == hash_file(arc_sde2)


def test_write_single_file_file_mode_env_var(rel_path, monkeypatch):
    """REPRO_ZIPFILE_FILE_MODE environment variable works."""

    with umask(0o002):
        # Expect 664
        data_file = file_factory(rel_path)

    monkeypatch.setenv("REPRO_ZIPFILE_FILE_MODE", "600")  # rw-------

    arc_path = rel_path / "archive.zip"
    with ReproducibleZipFile(arc_path, "w") as zp:
        zp.write(data_file)

    with ZipFile(arc_path, "r") as zp:
        print(zp.infolist())
        mode = (zp.getinfo(data_file.name).external_attr >> 16) & 0o777

    assert mode == 0o600, (oct(mode), oct(0o600))


def test_write_single_file_string_paths(rel_path):
    """Writing the same file with different mtime produces the same hash, using string inputs
    instead of Path."""
    data_file = file_factory(rel_path)
    file_name = data_file.name
    assert isinstance(file_name, str)

    repro_zip1 = rel_path / "repro_zip1.zip"
    with ReproducibleZipFile(repro_zip1, "w") as zp:
        zp.write(file_name)

    zip1 = rel_path / "zip1.zip"
    with ZipFile(zip1, "w") as zp:
        zp.write(file_name)

    sleep(2)
    data_file.touch()

    repro_zip2 = rel_path / "repro_zip2.zip"
    with ReproducibleZipFile(repro_zip2, "w") as zp:
        zp.write(file_name)

    zip2 = rel_path / "zip2.zip"
    with ZipFile(zip2, "w") as zp:
        zp.write(file_name)

    # All four archives should have identical content
    assert_archive_contents_equals(repro_zip1, zip1)
    assert_archive_contents_equals(repro_zip1, repro_zip2)
    assert_archive_contents_equals(repro_zip1, zip2)

    # ReproducibleZipFile hashes should match; ZipFile hashes should not
    assert hash_file(repro_zip1) == hash_file(repro_zip2)
    assert hash_file(zip1) != hash_file(zip2)


def test_write_single_file_arcname(base_path):
    """Writing a single file with explicit arcname."""
    data_file = file_factory(base_path)

    repro_zip1 = base_path / "repro_zip1.zip"
    with ReproducibleZipFile(repro_zip1, "w") as zp:
        zp.write(data_file, arcname="lore.txt")

    zip1 = base_path / "zip1.zip"
    with ZipFile(zip1, "w") as zp:
        zp.write(data_file, arcname="lore.txt")

    sleep(2)
    data_file.touch()

    repro_zip2 = base_path / "repro_zip2.zip"
    with ReproducibleZipFile(repro_zip2, "w") as zp:
        zp.write(data_file, arcname="lore.txt")

    zip2 = base_path / "zip2.zip"
    with ZipFile(zip2, "w") as zp:
        zp.write(data_file, arcname="lore.txt")

    # All four archives should have identical content
    assert_archive_contents_equals(repro_zip1, zip1)
    assert_archive_contents_equals(repro_zip1, repro_zip2)
    assert_archive_contents_equals(repro_zip1, zip2)

    # ReproducibleZipFile hashes should match; ZipFile hashes should not
    assert hash_file(repro_zip1) == hash_file(repro_zip2)
    assert hash_file(zip1) != hash_file(zip2)


def test_write_single_dir_dir_mode_env_var(rel_path, monkeypatch):
    """REPRO_ZIPFILE_DIR_MODE environment variable works."""

    with umask(0o002):
        # Expect 775
        dir_path = rel_path / data_factory()
        dir_path.mkdir()

    monkeypatch.setenv("REPRO_ZIPFILE_DIR_MODE", "700")  # rwx------

    arc_path = rel_path / "archive.zip"
    with ReproducibleZipFile(arc_path, "w") as zp:
        zp.write(dir_path)

    with ZipFile(arc_path, "r") as zp:
        print(zp.infolist())
        mode = (zp.getinfo(dir_path.name + "/").external_attr >> 16) & 0o777

    assert mode == 0o700, (oct(mode), oct(0o700))


def test_writestr(tmp_path):
    """writestr works as expected"""
    data = data_factory()

    repro_zip1 = tmp_path / "repro_zip1.zip"
    with ReproducibleZipFile(repro_zip1, "w") as zp:
        zp.writestr("data.txt", data=data)

    zip1 = tmp_path / "zip1.zip"
    with ZipFile(zip1, "w") as zp:
        zp.writestr("data.txt", data=data)

    sleep(2)

    repro_zip2 = tmp_path / "repro_zip2.zip"
    with ReproducibleZipFile(repro_zip2, "w") as zp:
        zp.writestr("data.txt", data=data)

    zip2 = tmp_path / "zip2.zip"
    with ZipFile(zip2, "w") as zp:
        zp.writestr("data.txt", data=data)

    # All four archives should have identical content
    assert_archive_contents_equals(repro_zip1, zip1)
    assert_archive_contents_equals(repro_zip1, repro_zip2)
    assert_archive_contents_equals(repro_zip1, zip2)

    # ReproducibleZipFile hashes should match; ZipFile hashes should not
    assert hash_file(repro_zip1) == hash_file(repro_zip2)
    assert hash_file(zip1) != hash_file(zip2)


def test_writestr_zip_info(rel_path):
    """writestr with ZipInfo input"""
    data = data_factory()
    data_file = rel_path / "data.txt"
    data_file.touch()

    repro_zip1 = rel_path / "repro_zip1.zip"
    with ReproducibleZipFile(repro_zip1, "w") as zp:
        zp.writestr(ZipInfo.from_file(data_file), data=data)

    zip1 = rel_path / "zip1.zip"
    with ZipFile(zip1, "w") as zp:
        zp.writestr(ZipInfo.from_file(data_file), data=data)

    sleep(2)
    data_file.touch()

    repro_zip2 = rel_path / "repro_zip2.zip"
    with ReproducibleZipFile(repro_zip2, "w") as zp:
        zp.writestr(ZipInfo.from_file(data_file), data=data)

    zip2 = rel_path / "zip2.zip"
    with ZipFile(zip2, "w") as zp:
        zp.writestr(ZipInfo.from_file(data_file), data=data)

    # All four archives should have identical content
    assert_archive_contents_equals(repro_zip1, zip1)
    assert_archive_contents_equals(repro_zip1, repro_zip2)
    assert_archive_contents_equals(repro_zip1, zip2)

    # ReproducibleZipFile hashes should match; ZipFile hashes should not
    assert hash_file(repro_zip1) == hash_file(repro_zip2)
    assert hash_file(zip1) != hash_file(zip2)


def test_writestr_source_date_epoch(tmp_path, monkeypatch):
    """Test that using writestr with the same data at different times with SOURCE_DATE_EPOCH set
    produces the same hash."""

    data = data_factory()

    arc_base = tmp_path / "base.zip"
    with ReproducibleZipFile(arc_base, "w") as zp:
        zp.writestr("data.txt", data=data)

    sleep(2)

    monkeypatch.setenv("SOURCE_DATE_EPOCH", "1691732367")

    arc_sde1 = tmp_path / "sde1.zip"
    with ReproducibleZipFile(arc_sde1, "w") as zp:
        zp.writestr("data.txt", data=data)

    arc_sde2 = tmp_path / "sde2.zip"
    with ReproducibleZipFile(arc_sde2, "w") as zp:
        zp.writestr("data.txt", data=data)

    # All three archives should have identical content
    assert_archive_contents_equals(arc_base, arc_sde1)
    assert_archive_contents_equals(arc_base, arc_sde2)

    # Base archive hash should match neither; two with SOURCE_DATE_EPOCH should match
    assert hash_file(arc_base) != hash_file(arc_sde1)
    assert hash_file(arc_sde1) == hash_file(arc_sde2)


def test_mkdir(rel_path):
    """mkdir is a Python 3.11+ method that we've backported to ReproducibleZipFile for <3.11, so
    that we can use the 3.11 implementation of write. Other tests don't cover direct use with a
    string input. Test that this is the same as writing a directory with ZipFile.
    """
    arc_repro1 = rel_path / "repro1.zip"
    with ReproducibleZipFile(arc_repro1, "w") as zp:
        zp.mkdir("dir")

    sleep(2)

    # Hashes are the same in second copy
    arc_repro2 = rel_path / "repro2.zip"
    with ReproducibleZipFile(arc_repro2, "w") as zp:
        zp.mkdir("dir")

    assert hash_file(arc_repro1) == hash_file(arc_repro2)

    # Produces same contests as regular ZipFile
    dir_path = rel_path / "dir"
    dir_path.mkdir()
    arc_zip = rel_path / "zip.zip"
    with ZipFile(arc_zip, "w") as zp:
        zp.write(dir_path)

    assert_archive_contents_equals(arc_repro1, arc_zip)

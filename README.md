# repro-zipfile

[![PyPI](https://img.shields.io/pypi/v/repro-zipfile.svg)](https://pypi.org/project/repro-zipfile/)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/repro-zipfile.svg)](https://anaconda.org/conda-forge/repro-zipfile)
[![conda-forge feedstock](https://img.shields.io/badge/conda--forge-feedstock-yellowgreen)](https://github.com/conda-forge/repro-zipfile-feedstock)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/repro-zipfile)](https://pypi.org/project/repro-zipfile/)
[![tests](https://github.com/drivendataorg/repro-zipfile/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/drivendataorg/repro-zipfile/actions/workflows/tests.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/drivendataorg/repro-zipfile/branch/main/graph/badge.svg)](https://codecov.io/gh/drivendataorg/repro-zipfile)

**A tiny, zero-dependency replacement for Python's `zipfile.ZipFile` library for creating reproducible/deterministic ZIP archives.**

"Reproducible" or "deterministic" in this context means that the binary content of the ZIP archive is identical if you add files with identical binary content in the same order. It means you can reliably check equality of the contents of two ZIP archives by simply comparing checksums of the archive using a hash function like MD5 or SHA-256.

This Python package provides a `ReproducibleZipFile` class that works exactly like [`zipfile.ZipFile`](https://docs.python.org/3/library/zipfile.html#zipfile-objects) from the Python standard library, except that certain file metadata are set to fixed values. See the ["How does repro-zipfile work?" section](#how-does-repro-zipfile-work) below for details.

You can also optionally install a command-line program, **rpzip**. See the ["rpzip command line program"](#rpzip-command-line-program) section further below.

## Installation

repro-zipfile is available from PyPI. To install, run:

```bash
pip install repro-zipfile
```

It is also available from conda-forge. To install, run:

```bash
conda install repro-zipfile -c conda-forge
```

## Usage

Simply import `ReproducibleZipFile` and use it in the same way you would use [`zipfile.ZipFile`](https://docs.python.org/3/library/zipfile.html#zipfile-objects) from the Python standard library.

```python
from repro_zipfile import ReproducibleZipFile

with ReproducibleZipFile("archive.zip", "w") as zp:
    # Use write to add a file to the archive
    zp.write("examples/data.txt", arcname="data.txt")
    # Or writestr to write data to the archive
    zp.writestr("lore.txt", data="goodbye")
```

Note that files must be written to the archive in the same order to reproduce an identical archive. Be aware that functions that like `os.listdir`, `os.glob`, `Path.iterdir`, and `Path.glob` return files in a nondeterministic order—you should call `sorted` on their returned values first.

See [`examples/usage.py`](./examples/usage.py) for an example script that you can run, and [`examples/demo_vs_zipfile.py`](./examples/demo_vs_zipfile.py) for a demonstration in contrast with the standard library's zipfile module.

For more advanced usage, such as customizing the fixed metadata values, see the subsections under ["How does repro-zipfile work?"](#how-does-repro-zipfile-work).

## rpzip command-line program

[![PyPI](https://img.shields.io/pypi/v/rpzip.svg)](https://pypi.org/project/rpzip/)

You can optionally install a lightweight command-line program, **rpzip**. This includes an additional dependency on the [typer](https://typer.tiangolo.com/) CLI framework. You can install it either directly or using the `cli` extra with repro-zipfile:

```bash
pip install rpzip
# or
pip install repro-zipfile[cli]
```

rpzip is designed to a partial drop-in replacement ubiquitous [zip](https://linux.die.net/man/1/zip) program. Use `rpzip --help` to see the documentation. Here are some usage examples:

```bash
# Archive a single file
rpzip archive.zip examples/data.txt
# Archive multiple files
rpzip archive.zip examples/data.txt README.md
# Archive multiple files with a shell glob
rpzip archive.zip examples/*.py
# Archive a directory recursively
rpzip -r archive.zip examples
```

In addition to the fixed file metadata done by repro-zipfile, rpzip will also always sort all paths being written.

## How does repro-zipfile work?

ZIP archives are not normally reproducible even when containing files with identical content because of file metadata. In particular, the usual culprits are:

1. Last-modified timestamps
2. File-system permissions (mode)

`repro_zipfile.ReproducibleZipFile` is a subclass of `zipfile.ZipFile` that overrides the `write`, `writestr`, and `mkdir` methods with versions that set the above metadata to fixed values. Note that repro-zipfile does not modify the original files—only the metadata written to the archive.

You can effectively reproduce what `ReproducibleZipFile` does with something like this:

```python
from zipfile import ZipFile

with ZipFile("archive.zip", "w") as zp:
    # Use write to add a file to the archive
    zp.write("examples/data.txt", arcname="data.txt")
    zinfo = zp.getinfo("data.txt")
    zinfo.date_time = (1980, 1, 1, 0, 0, 0)
    zinfo.external_attr = 0o644 << 16
    # Or writestr to write data to the archive
    zp.writestr("lore.txt", data="goodbye")
    zinfo = zp.getinfo("lore.txt")
    zinfo.date_time = (1980, 1, 1, 0, 0, 0)
    zinfo.external_attr = 0o644 << 16
```

It's not hard to do, but we believe `ReproducibleZipFile` is sufficiently more convenient to justify a small package!

See the next two sections for more details about the replacement metadata values and how to customize them.

### Last-modified timestamps

ZIP archives store the last-modified timestamps of files and directories. `ReproducibleZipFile` will set this to a fixed value. By default, the fixed value is 1980-01-01 00:00 UTC, which is the earliest timestamp that is supported by the ZIP format specifications.

You can customize this value with the `SOURCE_DATE_EPOCH` environment variable. If set, it will be used as the fixed value instead. This should be an integer corresponding to the [Unix epoch time](https://en.wikipedia.org/wiki/Unix_time) of the timestamp you want to set, e.g., `1704067230` for 2024-01-01 00:00:00 UTC. `SOURCE_DATE_EPOCH` is a [standard](https://reproducible-builds.org/docs/source-date-epoch/) created by the [Reproducible Builds project](https://reproducible-builds.org/) for software distributions.

### File-system permissions

ZIP archives store the file-system permissions of files and directories. The default permissions set for new files or directories often can be different across different systems or users without any intentional choices being made. (These default permissions are controlled by something called [`umask`](https://en.wikipedia.org/wiki/Umask).) `ReproducibleZipFile` will set these to fixed values. By default, the fixed values are `0o644` (`rw-r--r--`) for files and `0o755` (`rwxr-xr-x`) for directories, which matches the common default `umask` of `0o022` for root users on Unix systems. (The [`0o` prefix](https://docs.python.org/3/reference/lexical_analysis.html#integers) is how you can write an octal—i.e., base 8—integer literal in Python.)

You can customize these values using the environment variables `REPRO_ZIPFILE_FILE_MODE` and `REPRO_ZIPFILE_DIR_MODE`. They should be in three-digit octal [Unix numeric notation](https://en.wikipedia.org/wiki/File-system_permissions#Numeric_notation), e.g., `644` for `rw-r--r--`.

## Why care about reproducible ZIP archives?

ZIP archives are often useful when dealing with a set of multiple files, especially if the files are large and can be compressed. Creating reproducible ZIP archives is often useful for:

- **Building a software package.** This is a development best practice to make it easier to verify distributed software packages. See the [Reproducible Builds project](https://reproducible-builds.org/) for more explanation.
- **Working with data.** Verify that your data pipeline produced the same outputs, and avoid further reprocessing of identical data.
- **Packaging machine learning model artifacts.** Manage model artifact packages more effectively by knowing when they contain identical models.

## Related Tools and Alternatives

- https://diffoscope.org/
    - Can do a rich comparison of archive files and show what specifically differs
- https://github.com/timo-reymann/deterministic-zip
    - Command-line program written in Go that matches zip's interface but strips nondeterministic metadata when adding files
- https://github.com/bboe/deterministic_zip
    - Command-line program written in Python that creates deterministic ZIP archives
- https://salsa.debian.org/reproducible-builds/strip-nondeterminism
    - Perl library for removing nondeterministic metadata from file archives
- https://github.com/Code0x58/python-stripzip
    - Python command-line program that removes file metadata from existing ZIP archives

# repro-zipfile

[![PyPI](https://img.shields.io/pypi/v/repro-zipfile.svg)](https://pypi.org/project/repro-zipfile/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/repro-zipfile)](https://pypi.org/project/repro-zipfile/)
[![tests](https://github.com/drivendataorg/repro-zipfile/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/drivendataorg/repro-zipfile/actions/workflows/tests.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/drivendataorg/repro-zipfile/branch/main/graph/badge.svg)](https://codecov.io/gh/drivendataorg/repro-zipfile)

**A tiny, zero-dependency replacement for Python's `zipfile.ZipFile` for creating reproducible/deterministic ZIP archives.**

"Reproducible" or "deterministic" in this context means that the binary content of the ZIP archive is identical if you add files with identical binary content in the same order. This Python package provides a `ReproducibleZipFile` class that works exactly like [`zipfile.ZipFile`](https://docs.python.org/3/library/zipfile.html#zipfile-objects) from the Python standard library, except that all files written to the archive have their last-modified timestamps set to a fixed value.

## Installation

...

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

See `examples/usage.py` for an example script that you can run, and `examples/demo_vs_zipfile.py` for a demonstration in contrast with the standard library's zipfile module.

### Set timestamp value with SOURCE_DATE_EPOCH

repro_zipfile supports setting the fixed timestamp value using the `SOURCE_DATE_EPOCH` environment variable. This should be an integer corresponding to the [Unix epoch time](https://en.wikipedia.org/wiki/Unix_time) of the timestamp you want to set. `SOURCE_DATE_EPOCH` is a [standard](https://reproducible-builds.org/docs/source-date-epoch/) created by the [Reproducible Builds project](https://reproducible-builds.org/).

## How does repro-zipfile work?

`repro_zipfile.ReproducibleZipFile` is a subclass of `zipfile.ZipFile` that overrides the `write` and `writestr` methods. The overridden methods set the modified timestamp of all files written to the archive to a fixed value. By default, this value is 1980-01-01 0:00 UTC, which is the earliest timestamp that is supported by the ZIP format. You can customize this value as documented in the previous section.

You can effectively reproduce what `ReproducibleZipFile` does with something like this:

```python
from zipfile import ZipFile

with ZipFile("archive.zip", "w") as zp:
    # Use write to add a file to the archive
    zp.write("examples/data.txt", arcname="data.txt")
    zinfo = zp.getinfo("data.txt")
    zinfo.date_time = (1980, 1, 1, 0, 0, 0)
    # Or writestr to write data to the archive
    zp.writestr("lore.txt", data="goodbye")
    zinfo = zp.getinfo("lore.txt")
    zinfo.date_time = (1980, 1, 1, 0, 0, 0)
```

It's not hard to do, but we believe `ReproducibleZipFile` is sufficiently more convenient to justify a small package!

## Why care about reproducible ZIP archives?

ZIP archives are often useful when dealing with a set of multiple files, especially if the files are large and can be compressed. Creating reproducible ZIP archives is often useful for:

- **Building a software package.** This is a development best practice to make it easier to verify distributed software packages. See [reproducible-builds.org](https://reproducible-builds.org/) for more information.
- **Working with data.** Verify that your data pipeline produced the same outputs, or avoid reprocessing identical data.
- **Packaging machine learning model artifacts.** Manage trained models more effectively.

## Related Tools and Alternatives

- https://diffoscope.org/
    - Can do a rich comparison of archive files and show what specifically differs
- https://github.com/timo-reymann/deterministic-zip
    - Command-line program that matches zip's interface but strips nondeterministic metadata when adding files
- https://salsa.debian.org/reproducible-builds/strip-nondeterminism
    - Perl library for removing nondeterministic metadata from file archives
- https://github.com/Code0x58/python-stripzip
    - Python command-line program that removes file metadata from existing zip archives

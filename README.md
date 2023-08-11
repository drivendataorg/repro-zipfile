# repro-zipfile

**A replacement from Python's `zipfile.ZipFile` for creating reproducible/deterministic ZIP archives.**

"Reproducible" or "deterministic" in this context means that the binary content of the ZIP archive is identical if you add files with identical binary content in the same order.

## What does repro-zipfile do differently?

repro-zipfile sets the modified timestamp of all files written to the archive to a fixed value. By default, this value is 1980-01-01 0:00 UTC, which is the earliest timestamp that is supported by the ZIP format.

## Installation

...

## Usage

```python
from repro_zipfile import ReproducibleZipFile

with ReproducibleZipFile("archive.zip", "w") as zp:
    # Use write to add a file to the archive
    zp.write("examples/data.txt", arcname="data.txt")
    # Or writestr to write data to the archive
    zp.writestr("lore.txt", data="goodbye")
```

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

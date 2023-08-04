# reprozip

**A replacement from Python's `zipfile.ZipFile` for creating reproducible/deterministic ZIP archives.**

"Reproducible" or "deterministic" in this context means that the binary content of the ZIP archive is identical if you add files with identical binary content in the same order.

## What does reprozip do differently?

reprozip sets the modified timestamp of all files in the archive to 1980-01-01 0:00 UTC, which is the earliest timestamp that is supported by the ZIP format.

## Why care about reproducible ZIP archives?

ZIP archives are often useful when dealing with a set of multiple files, especially if the files are large and can be compressed. Creating reproducible ZIP archives is often useful for:

- **Building a software package.** This is a development best practice to make it easier to verify distributed software packages. See [reproducible-builds.org](https://reproducible-builds.org/) for more information.
- **Working with data.** Verify that your data pipeline produced the same outputs, or avoid reprocessing identical data.
- **Packaging machine learning model artifacts.** Manage trained models more effectively.

## Other related tools

- https://diffoscope.org/
- https://github.com/timo-reymann/deterministic-zip
- https://github.com/Code0x58/python-stripzip

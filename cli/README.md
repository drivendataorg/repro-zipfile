# rpzip — a CLI backed by repro-zipfile

[![PyPI](https://img.shields.io/pypi/v/rpzip.svg)](https://pypi.org/project/rpzip/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/rpzip)](https://pypi.org/project/rpzip/)
[![tests](https://github.com/drivendataorg/repro-zipfile/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/drivendataorg/repro-zipfile/actions/workflows/tests.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/drivendataorg/repro-zipfile/branch/main/graph/badge.svg)](https://codecov.io/gh/drivendataorg/repro-zipfile)

**A lightweight command-line program for creating reproducible/deterministic ZIP archives.**

"Reproducible" or "deterministic" in this context means that the binary content of the ZIP archive is identical if you add files with identical binary content in the same order. It means you can reliably check equality of the contents of two ZIP archives by simply comparing checksums of the archive using a hash function like MD5 or SHA-256.

This package provides a command-line program named **rpzip**. It is designed as a partial drop-in replacement for the ubiquitous [zip](https://linux.die.net/man/1/zip) program and implements a commonly used subset of zip's inferface.

For further documentation, see the ["rpzip command line program"](https://github.com/drivendataorg/repro-zipfile#rpzip-command-line-program) section of the repro-zipfile README.

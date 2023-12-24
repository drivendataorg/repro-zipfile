# repro-zipfile-cli

[![PyPI](https://img.shields.io/pypi/v/repro-zipfile-cli.svg)](https://pypi.org/project/repro-zipfile-cli/)
[![Supported Python versions](https://img.shields.io/pypi/pyversions/repro-zipfile-cli)](https://pypi.org/project/repro-zipfile-cli/)
[![tests](https://github.com/drivendataorg/repro-zipfile/actions/workflows/tests.yml/badge.svg?branch=main)](https://github.com/drivendataorg/repro-zipfile/actions/workflows/tests.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/drivendataorg/repro-zipfile/branch/main/graph/badge.svg)](https://codecov.io/gh/drivendataorg/repro-zipfile)

**A lightweight command-line program for creating reproducible/deterministic ZIP archives.**

"Reproducible" or "deterministic" in this context means that the binary content of the ZIP archive is identical if you add files with identical binary content in the same order. It means you can reliably check equality of the contents of two ZIP archives by simply comparing checksums of the archive using a hash function like MD5 or SHA-256.

This package provides a command-line program named **repzip** that is a drop-in replacement for a subset of the most commonly used functionality from the ubiquitous [zip](https://linux.die.net/man/1/zip) program.

For more about what repzip does, see the README for [repro-zipfile](https://github.com/drivendataorg/repro-zipfile), the backend library that repzip uses.

## Installation

repro-zipfile-cli is available from PyPI. To install, run:

```bash
pip install repro-zipfile-cli
```

You can also equivalently install it as an extra for repro-zipfile:

```bash
pip install repro-zipfile[cli]
```

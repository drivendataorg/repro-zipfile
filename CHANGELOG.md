# Changelog — repro-zipfile

## v0.3.0 (2024-01-27)

- Added a `cli` installation extra for installing the rpzip package, which includes a command-line program

## v0.2.0 (2024-01-08)

- Changed `ReproducibleZipFile` to also overwrite file-system permissions with fixed values. These default to `0o644` (`rw-r--r--`) for files and `0o755` (`rwxr-xr-x`) for directories.
- Added support for `REPRO_ZIPFILE_FILE_MODE` and `REPRO_ZIPFILE_DIR_MODE` environment variables for overriding the fixed file and directory permission values.

## v0.1.0 (2023-08-12)

Initial release! 🎉

# Changelog — rpzip

## v0.1.3 (2025-10-05)

- Added Python 3.14 as a supported version.

## v0.1.2 (2025-07-26)

- Fixed inconsistency with `zip` with output file suffixes. `rpzip` now only adds a `.zip` suffix if the output file does not have a suffix already. Previously, an existing suffix would be replaced by `.zip`. ([Issue #21](https://github.com/drivendataorg/repro-zipfile/issues/21), [PR #22](https://github.com/drivendataorg/repro-zipfile/pull/22) contributed by [@Freed-Wu](https://github.com/Freed-Wu))

## v0.1.1 (2024-02-02)

- Fixed misformatted `--version` output.

## v0.1.0 (2024-01-27)

Initial release! 🎉

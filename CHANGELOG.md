# Changelog

All notable changes to this project are documented here. The format of this document is based on [Keep a Changelog](https://keepachangelog.com). This project adheres to [Semantic Versioning](https://semver.org).

## [Unreleased]

### Added

- The generated `app.py` module now explicitly sets up provider discovery.

### Fixed

- Previously, running `bocadillo create my-package` would result in creating a Python package named `my-package`, which is not a valid Python identifier. This has been fixed: the package would now be named `my_package`.

## [v0.1.1] - 2019-14-17

### Fixed

- `bocadillo create` could not run because project templates were not included when installing Bocadillo CLI. This has been fixed!

## [v0.1.0] - 2019-14-17

### Added

Features:

- Create a package: `bocadillo create`.
- Show CLI and Bocadillo versions: `--version / -V`.

Meta:

- Setup project and package.
- Changelog.
- License.

[unreleased]: https://github.com/bocadilloproject/bocadillo-cli/compare/v0.1.1...HEAD
[v0.1.1]: https://github.com/bocadilloproject/bocadillo-cli/compare/v0.1.0...v0.1.1
[v0.1.0]: https://github.com/bocadilloproject/bocadillo-cli/compare/04dff6e...v0.1.0

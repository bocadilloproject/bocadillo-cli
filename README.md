# Bocadillo CLI

[![pypi](https://img.shields.io/pypi/v/bocadillo-cli.svg)][pypi-url]
[![travis](https://img.shields.io/travis/bocadilloproject/bocadillo-cli.svg)](https://travis-ci.org/bocadilloproject/bocadillo)
[![black](https://img.shields.io/badge/code_style-black-000000.svg)](https://github.com/ambv/black)
[![codecov](https://codecov.io/gh/bocadilloproject/bocadillo-cli/branch/master/graph/badge.svg)](https://codecov.io/gh/bocadilloproject/bocadillo-cli)
![license](https://img.shields.io/pypi/l/bocadillo-cli.svg)

[pypi-url]: https://pypi.org/project/bocadillo-cli

Bocadillo CLI provides standard development tooling for [Bocadillo].

[bocadillo]: https://github.com/bocadilloproject/bocadillo

![](media/demo.gif)

## Install

```bash
pip install bocadillo-cli
```

## Usage

### Overview

```
$ bocadillo --help
Usage: bocadillo [OPTIONS] COMMAND [ARGS]...

Options:
  -V, --version  Show the version and exit.
  --help         Show this message and exit.

Commands:
  create  Initialize a Bocadillo project.
```

### Create a project

```
$ bocadillo create --help
Usage: bocadillo create [OPTIONS] NAME

  Initialize a Bocadillo project.

Options:
  -d, --directory DIRECTORY  Directory where the project should be created.
                             Created if does not exist. Defaults to `NAME`.
  --dry                      Dry mode: does not write anything.
  --help                     Show this message and exit.
```

## Contributing

Want to contribute code or documentation? Great to hear! Our [Contributing Guidelines](https://github.com/bocadilloproject/bocadillo-cli/blob/master/CONTRIBUTING.md) are here to help.

## License

MIT

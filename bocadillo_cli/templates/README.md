# {{ name }}

This project was generated using [Bocadillo CLI](https://bocadilloproject.github.io) version {{ version }}.

[repo]: https://github.com/bocadilloproject/bocadillo-cli

## Install

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Start the uvicorn server:

```bash
uvicorn {{ name }}.asgi:app
```

To enable hot reload, add the `--reload` option.

The server will run at `http://localhost:8000`.

Happy coding!

## Getting help

To get further help on Bocadillo CLI:

- Use `$ bocadillo --help`.
- Read the [Bocadillo CLI documentation][repo].

To get help on Bocadillo, visit the [Bocadillo docs site](https://bocadilloproject.github.io).

If you like Bocadillo, feel free to show some love by [starring the repo](https://github.com/bocadilloproject/bocadillo). ❣️

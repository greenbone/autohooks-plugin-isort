![Greenbone Logo](https://www.greenbone.net/wp-content/uploads/gb_logo_resilience_horizontal.png)

# autohooks-plugin-isort

[![PyPI release](https://img.shields.io/pypi/v/autohooks-plugin-isort.svg)](https://pypi.org/project/autohooks-plugin-isort/)

An [autohooks](https://github.com/greenbone/autohooks) plugin for Python code
formatting via [isort](https://github.com/timothycrosley/isort).

## Installation

### Install using pip

You can install the latest stable release of autohooks-plugin-isort from the
Python Package Index using [pip](https://pip.pypa.io/):

    pip install autohooks-plugin-isort

Note the `pip` refers to the Python 3 package manager. In a environment where
Python 2 is also available the correct command may be `pip3`.

### Install using pipenv

It is highly encouraged to use [pipenv](https://github.com/pypa/pipenv) for
maintaining your project's dependencies. Normally autohooks-plugin-isort is
installed as a development dependency.

    pipenv install --dev autohooks-plugin-isort

## Usage

To activate the isort autohooks plugin please add the following setting to your
*pyproject.toml* file.

```toml
[tool.autohooks]
pre-commit = ["autohooks.plugins.isort"]
```

By default, autohooks plugin isort checks all files with a *.py* ending. If only
the imports of files in a sub-directory or files with different endings should
be sorted, just add the following setting:

```toml
[tool.autohooks]
pre-commit = ["autohooks.plugins.isort"]

[tool.autohooks.plugins.isort]
include = ['foo/*.py', '*.foo']
```

When using `autohooks-plugins-isort` in combination with
[autohooks-plugin-black](https://github.com/greenbone/autohooks-plugin-black),
the following configuration is recommended to ensure a consistent formatting:

```toml
[tool.isort]
multi_line_output = 3
include_trailing_comma = true
force_grid_wrap = 0
use_parentheses = true
line_length = 80
```

## Maintainer

This project is maintained by [Greenbone Networks GmbH](https://www.greenbone.net/).

## Contributing

Your contributions are highly appreciated. Please
[create a pull request](https://github.com/greenbone/autohooks-plugin-isort/pulls)
on GitHub. Bigger changes need to be discussed with the development team via the
[issues section at GitHub](https://github.com/greenbone/autohooks-plugin-isort/issues)
first.

## License

Copyright (C) 2019 [Greenbone Networks GmbH](https://www.greenbone.net/)

Licensed under the [GNU General Public License v3.0 or later](LICENSE).

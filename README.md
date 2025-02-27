# Pbs Parse

<!-- badges-begin -->
[![Tests](https://github.com/DonalChilde/pbs-parse/actions/workflows/pytest.yaml/badge.svg?branch=dev)](https://github.com/DonalChilde/pbs-parse/actions/workflows/pytest.yaml/badge.svg?branch=dev)
[![Codecov](https://codecov.io/gh/DonalChilde/pbs-parse/branch/main/graph/badge.svg)](https://codecov.io/gh/DonalChilde/pbs-parse/branch/main/graph/badge.svg)

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

[![PyPI](https://img.shields.io/pypi/v/pbs-parse.svg)][pypi status]
[![Status](https://img.shields.io/pypi/status/pbs-parse.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/pbs-parse)][pypi status]
[![License](https://img.shields.io/pypi/l/pbs-parse)][license]
[![Read the documentation at https://pbs-parse.readthedocs.io/](https://img.shields.io/readthedocs/pbs-parse/latest.svg?label=Read%20the%20Docs)][read the docs]

[pypi status]: https://pypi.org/project/pbs-parse/
[read the docs]: https://pbs-parse.readthedocs.io/

<!-- badges-end -->

Pbs-Parse extracts the text from an American Airlines pilot bid package pdf file, and converts the trips found into a json format with timezone aware dates and times for each trip.

## Requirements

Python 3.13 or better is required, as well as access to the bid package pdf files.

## Installation

The use of [python virtual environments](https://stackoverflow.com/q/41972261) is strongly recomended.

the [uv](https://docs.astral.sh/uv/) tool is an easy way to get started quickly creating virtual environments and running python programs.

```bash
# The fastest way to get started is to
# install uv for your system and...

uvx pbs-parse --help
```

You can also install _Pbs Parse_ via [pip] from [PyPI]:

```bash
# Again, using a virtual environment is strongly recommended.
pip install pbs-parse
```

## Usage

Assuming all the pdf bid package files for one month are in the same directory,

> **Note:** If using uv to run this tool, prefix the following commands with uvx

```bash
# This will extract the text from each file found,
# and save the new text file in the destination directory
# with the same file name, but with the `.txt` ending.
# Using the SOURCE_DIR as the DESTINATION_DIR will make
# the later parsing of the txt files easier.
pfmsoft-pdf2txt extract SOURCE_DIR DESTINATION_DIR
```

Create a pbs data store in a directory.

```bash
# This creates a subdirectory named NAME in the STORES_DIRECTORY,
# the parsed files will be placed there.
# The dates should be in the format 2025-01-31
# The NAME is usually the name of the bid month, eg. 2025-01 or jan25
pbs-parse store create STORES_DIRECTORY NAME EFFECTIVE_FROM EFFECTIVE_TO

# This command expects to find pdf and txt bid packages in one directory.
# These files should be for one bid period that matches the effective dates
# used to create the store.
# The STORE_DIRECTORY is the STORES_DIRECTORY/NAME used in the create command.
pbs-parse store add-all-bases STORE_DIRECTORY SOURCE_DIRECTORY

# This command will perform all the parse steps on all the bases in the
# pbs data store.
pbs-parse store do STORE_DIRECTORY _all_

# You can get stats for the trips in the pbs data store by:
pbs-parse store stats STORE_DIRECTORY

# You can export any expanded trips with errors to a debug directory.
pbs-parse store export expanded-debug STORE_DIRECTORY DEBUG_DIRECTORY
```

Please see the [documentation] for details.

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_Pbs Parse_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [DonalChilde]'s [cookiecutter-python-base] template, which was inspired by [@cjolowicz]'s [Hypermodern Python Cookiecutter] template.

[@cjolowicz]: https://github.com/cjolowicz
[DonalChilde]: https://github.com/DonalChilde
[pypi]: https://pypi.org/
[hypermodern python cookiecutter]: https://github.com/cjolowicz/cookiecutter-hypermodern-python
[cookiecutter-python-base]: https://github.com/DonalChilde/cookiecutter-python-base
[file an issue]: https://github.com/DonalChilde/pbs-parse/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/DonalChilde/pbs-parse/blob/main/LICENSE
[contributor guide]: https://github.com/DonalChilde/pbs-parse/blob/main/CONTRIBUTING
[documentation]: https://pbs-parse.readthedocs.io/en/latest/

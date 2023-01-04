![Two Pi Pies](https://raw.githubusercontent.com/rmnldwg/nerdyversary/main/two_pi_pies.jpg)

# Nerdyversary

[![MIT license](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](https://github.com/rmnldwg/nerdyversary/blob/main/LICENSE)
[![GitHub repo](https://img.shields.io/badge/rmnldwg%2Fnerdyversary-grey.svg?style=flat&logo=github)](https://github.com/rmnldwg/nerdyversary)
[![build badge](https://github.com/rmnldwg/nerdyversary/actions/workflows/build.yml/badge.svg?style=flat)](https://pypi.org/project/nerdyversary/)
[![docs badge](https://github.com/rmnldwg/nerdyversary/actions/workflows/docs.yml/badge.svg?style=flat)](https://rmnldwg.github.io/nerdyversary/)
[![tests badge](https://github.com/rmnldwg/nerdyversary/actions/workflows/tests.yml/badge.svg?style=flat)](https://rmnldwg.github.io/nerdyversary/)

Small project about finding "nerdy anniversaries". An obvious example would be that after 3.1415... years one could celebrate the $\pi$-th anniversary. The code in this repo finds nice combinations of numbers like $\pi$, $e$, $\phi$ and so on and can construct fractions for the approximation.


## Installation

### From PyPI

> ⚠️ **Note:**
> This project is currently not yet on PyPI.


### From Source

1. Clone the repository
   ```
   $ git clone https://github.com/rmnldwg/nerdyversary
   ```

1. Create a Virtual Environment (optional, but recommended)
   ```
   $ python3 -m venv .venv
   ```
   You should do this with an installation of Python 3.10 or later. And don't forget to activate the environment with
   ```
   $ source .venv/bin/activate
   ```

1. Use `pip` to install
   ```
   $ pip install -U pip setuptools setuptools-scm
   $ pip install .
   ```


## Usage

### Script

```
usage: nerdyversary [-h] [-v] [-d SPECIAL_DAY] [-s START] [-e END]
                    [--max-power MAX_POWER] [--factor-lim FACTOR_LIM]
                    [--format FORMAT]

Find beautiful nerdyversaries.

options:
  -h, --help            show this help message and exit
  -v, --version         Show the installed version and exit.
  -d SPECIAL_DAY, --special-day SPECIAL_DAY
                        Date of the special day in ISO format. (default: 2023-01-04)
  -s START, --start START
                        Date when to start with search in ISO format. (default:
                        2023-01-04)
  -e END, --end END     Date when to end the search in ISO format. (default:
                        2024-01-04)
  --max-power MAX_POWER
                        Largest exponent to consider for building the nerdyversaries.
                        (default: 5)
  --factor-lim FACTOR_LIM
                        Largest multiple of a symbol that is accepted. (default: 10)
  --format FORMAT       The output format that will be used by the `tabulate` package.
                        (default: simple)
```

The `FORMAT` argument must be one of the strings the [tabulate](https://github.com/astanin/python-tabulate#table-format) package understands.

An example: The input
```
$ nerdyversary -d 2012-12-21 -s 2023-01-01 -e 2024-01-01 --format pipe --factor-lim 4 --max-power 3
```
will yield the following table:

| Date         |   Days |   Years | Expression                     |
|:-------------|-------:|--------:|:-------------------------------|
| 6. Jan 2023  |   3668 |   10.04 | $\frac{e^{3}}{2}$              |
| 24. Feb 2023 |   3717 |   10.18 | $\frac{5 e^{3}}{\pi^{2}}$      |
| 12. Jun 2023 |   3825 |   10.47 | $4 \phi^{2}$                   |
| 19. Jun 2023 |   3832 |   10.49 | $\frac{5 \pi^{3}}{2 e^{2}}$    |
| 25. Jul 2023 |   3868 |   10.59 | $\frac{5 \phi^{3}}{2}$         |
| 5. Nov 2023  |   3971 |   10.87 | $4 e$                          |
| 12. Nov 2023 |   3978 |   10.89 | $\frac{3 \pi^{2}}{e}$          |
| 14. Dec 2023 |   4010 |   10.98 | $\frac{3 \pi^{3}}{2 \phi^{3}}$ |

The symbols here are

* the golden ratio $\phi \approx 1.618\ldots$
* the number $\pi \approx 3.1415\ldots$
* Euler's number $e \approx 2.718\ldots$

When using this package as a library, arbitrary constants may be defined as symbols.


### Library API

The API documentation is hosted [here](https://rmnldwg.github.io/nerdyversary).

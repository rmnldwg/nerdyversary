"""
.. include:: ../README.md
"""
import argparse
import datetime as dt

import numpy as np
from sympy import Expr, NumberSymbol, S, latex
from tabulate import tabulate

from ._version import version

TODAY = dt.date.today()
DAYS_PER_YEAR = 365.2425
SYMBOLS_LIST = [S.Pi, S.Exp1, S.GoldenRatio]


def search(
    special_day: str | dt.date,
    search_start: str | dt.date | None = None,
    search_end: str | dt.date | None = None,
    **construct_kwargs,
) -> set[tuple[Expr, float]]:
    """
    For every day between the date `search_start` and `search_end`, check if the time
    since the `special_day` can be written as a nerdyversary. If `search_start` is not
    given, it is assumed to be today. When `search_end` is `None`, it will be
    `search_start` plus 365 days.

    The keyword arguments `construct_kwargs` are directly passed to the
    `construct_nerdyversary` function.

    This function returns a list of `candidates`, all of whch contain the analytical
    `sympy` expression that constitutes the nerdy approximation and the difference as
    a sanity check.

    Example:
    >>> search(
    ...     special_day="2016-03-30",
    ...     search_start="2022-07-10",
    ...     search_end="2022-07-20",
    ...     factor_lim=5,
    ...     max_power=3,
    ... )
    [(datetime.date(2022, 7, 12), 2*pi), (datetime.date(2022, 7, 16), 3*pi**3*exp(-2)/2)]
    """
    if isinstance(special_day, str):
        special_day = dt.date.fromisoformat(special_day)

    if search_start is None:
        search_start = TODAY
    elif isinstance(search_start, str):
        search_start = dt.date.fromisoformat(search_start)

    if search_end is None:
        search_end = search_start + dt.timedelta(days=365)
    elif isinstance(search_end, str):
        search_end = dt.date.fromisoformat(search_end)

    candidates = {}
    min_duration = (search_start - special_day).days
    max_duration = (search_end - special_day).days

    for duration_in_days in range(min_duration, max_duration):
        expressions = construct(
            duration_in_years=(duration_in_days / DAYS_PER_YEAR),
            **construct_kwargs
        )
        date = special_day + dt.timedelta(days=duration_in_days)
        new_candidates = {(date, expr) for expr in expressions}
        candidates = {*candidates, *new_candidates}

    return sorted(candidates)


def construct(
    duration_in_years: float,
    symbols: list[NumberSymbol] | None = None,
    max_power: int = 5,
    tolerance: float = 0.5,
    factor_lim: int = 10,
):
    """
    For a given `duration_in_years`, find nice and nerdy approximations using the list
    of defined `symbols`. The `max_power` is the largest exponent that is considered
    for the `symbols`, while `factor_lim` ensures that the factors in the enumerator
    and denominator don't get too large. An approximation is considred good enough,
    when it is withing the `tolerance`, which must be given in days.

    Example:
    >>> duration_in_years = 2 * 3.1416 / 2.7183
    >>> [res for res in construct(duration_in_years)]
    [2*pi*exp(-1)]
    """
    if symbols is None:
        symbols = SYMBOLS_LIST.copy()

    for enum_pow in range(max_power + 1):
        for denom_pow in range(max_power + 1):
            # exponents of enum & denom 0 means approximation is fraction
            if enum_pow == denom_pow == 0:
                continue

            for enum_sym in symbols:
                for denom_sym in symbols:
                    # don't consider same symbol in enumerator and denominator
                    if enum_sym == denom_sym:
                        continue

                    enum_expr = enum_sym ** enum_pow
                    denom_expr = denom_sym ** denom_pow

                    ratio = float((duration_in_years * denom_expr / enum_expr).evalf())
                    enum_fac, denom_fac = round(ratio, 2).as_integer_ratio()

                    if enum_fac > factor_lim or denom_fac > factor_lim:
                        continue

                    expression = (enum_fac * enum_expr) / (denom_fac * denom_expr)
                    approx = float(expression.evalf())
                    difference = np.abs(duration_in_years - approx)

                    if difference * DAYS_PER_YEAR < tolerance:
                        yield expression


def get_fields(date: dt.date, expression: Expr) -> dict[str, str]:
    """
    Compile a `date`, and the corresponding nerdyversary `expression` into a dictionary
    that contains the fields `"Date"`, `"Days"`, `"Years"`, and `"Expression"` as a
    LaTeX formula.

    Example:
    >>> candidates = search(
    ...     special_day="2016-03-30",
    ...     search_start="2022-07-10",
    ...     search_end="2022-07-20",
    ...     factor_lim=5,
    ...     max_power=3,
    ... )
    >>> get_fields(*candidates[0])
    {'Date': '12. Jul 2022', 'Days': '2295', 'Years': '6.28', 'Expression': '$2 \\\\pi$'}

    A list of dictionaries like these for each candidate can then be used to display
    a pretty table using the [tabulate](https://github.com/astanin/python-tabulate)
    package.
    """
    duration_in_years = float(expression.evalf())
    duration_in_days = round(duration_in_years * DAYS_PER_YEAR)
    return {
        "Date"      : f"{date:%-d. %b %Y}",
        "Days"      : f"{duration_in_days:d}",
        "Years"     : f"{duration_in_years:.2f}",
        "Expression": f"${latex(expression)}$",
    }


def main():
    """Find beautiful nerdyversaries."""
    parser = argparse.ArgumentParser(
        prog="nerdyversary",
        description=main.__doc__,
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-v", "--version", action="version", version=f"nerdyversary {version}",
        help="Show the installed version and exit."
    )
    parser.add_argument(
        "-d", "--special-day", type=dt.date.fromisoformat, default=dt.date.today(),
        help="Date of the special day in ISO format.",
    )
    parser.add_argument(
        "-s", "--start", type=dt.date.fromisoformat, default=dt.date.today(),
        help="Date when to start with search in ISO format."
    )
    parser.add_argument(
        "-e", "--end", type=dt.date.fromisoformat,
        default=dt.date.today() + dt.timedelta(days=DAYS_PER_YEAR),
        help="Date when to end the search in ISO format."
    )
    parser.add_argument(
        "--max-power", type=int, default=5,
        help="Largest exponent to consider for building the nerdyversaries."
    )
    parser.add_argument(
        "--factor-lim", type=int, default=10,
        help="Largest multiple of a symbol that is accepted."
    )
    parser.add_argument(
        "--format", type=str, default="simple",
        help="The output format that will be used by the `tabulate` package."
    )
    args = parser.parse_args()

    candidates = search(
        special_day=args.special_day,
        search_start=args.start,
        search_end=args.end,
        max_power=args.max_power,
        factor_lim=args.factor_lim,
    )
    table = [get_fields(*candidate) for candidate in candidates]

    print(tabulate(table, headers="keys", tablefmt=args.format))

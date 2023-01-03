"""
.. include:: ../README.md
"""
import datetime as dt

import numpy as np
from sympy import Expr, NumberSymbol, S, latex

TODAY = dt.date.today()
DAYS_PER_YEAR = 365.2425
SYMBOLS_LIST = [S.Pi, S.Exp1, S.GoldenRatio]


def search(
    special_day: str | dt.date,
    search_start: str | dt.date | None = None,
    search_end: str | dt.date | None = None,
    **construct_kwargs,
) -> list[tuple[Expr, float]]:
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

    candidates = []
    duration_in_days = (search_start - special_day).days
    max_duration = (search_end - special_day).days

    while duration_in_days < max_duration:
        try:
            expr, _ = construct(
                duration_in_years=(duration_in_days) / DAYS_PER_YEAR,
                **construct_kwargs
            )
            date = special_day + dt.timedelta(days=duration_in_days)
            candidates.append((date, expr))
        except NoNerdyversaryError:
            pass
        finally:
            duration_in_days += 1

    return candidates


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

    Raises a `NoNerdyversaryError` if nothing is found with the given parameters.

    Example:
    >>> duration_in_years = 2 * 3.1416 / 2.7183
    >>> construct(duration_in_years)
    (2*pi*exp(-1), 1.0046673776020754e-05)
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
                        return expression, difference

    raise NoNerdyversaryError(
        "No nerdyversary found for the provided duration, tolerance and limitations."
    )


def format_md_row(
    date: dt.date,
    expression: Expr,
) -> str:
    """
    Return a row of a markdown table that contains the `date` and the `expression` of
    a nerdyversary. The header of that table looks like this:

    ```markdown
    | Date | Days | Years | Expression |
    | :--- | ---: | ----: | ---------: |
    ```

    Example:
    >>> results = search(
    ...     special_day="2016-03-30",
    ...     search_start="2022-07-10",
    ...     search_end="2022-07-20",
    ...     factor_lim=5,
    ...     max_power=3
    ... )
    >>> for res in results:
    ...     print(format_md_row(*res))
    ...
    | 12. Jul 2022 | 2295 | 6.28 | $2 \\pi$ |
    | 16. Jul 2022 | 2299 | 6.29 | $\\frac{3 \\pi^{3}}{2 e^{2}}$ |

    Together with the header row above, this would render into the following nice
    little table:

    | Date         | Days | Years | Expression                    |
    | :----------- | ---: | ----: | ----------------------------: |
    | 12. Jul 2022 | 2295 | 6.28  | $2 \\pi$                      |
    | 16. Jul 2022 | 2299 | 6.29  | $\\frac{3 \\pi^{3}}{2 e^{2}}$ |
    """
    duration_in_years = float(expression.evalf())
    duration_in_days = round(duration_in_years * DAYS_PER_YEAR)
    return (
        f"| {date:%-d. %b %Y} "
        f"| {duration_in_days:d} "
        f"| {duration_in_years:.2f} "
        f"| ${latex(expression)}$ |"
    )


class NoNerdyversaryError(Exception):
    """
    Exception that gets raised when no suitable nerdyversary can be constructed for a
    given duration.
    """

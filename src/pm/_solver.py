"""Shared cvxpy solve guards.

Private helpers: every optimizer in this repo returns weights from
`cp.Variable.value`, which is `None` when the solver doesn't reach an
optimal point (infeasible, unbounded, or solver error). Without a check,
`np.asarray(None).ravel()` yields `array([None], dtype=object)` - no
exception, and the bad value silently poisons whatever consumes it.
"""

import numpy as np

_ACCEPTABLE = ("optimal", "optimal_inaccurate")


def check_optimal(problem):
    """Solve `problem` and raise ValueError if it didn't reach an optimal
    point. Use directly (rather than `solved_weights`) when the answer
    isn't one cvxpy Variable's `.value` - e.g. `max_sharpe`'s tangency
    portfolio, which is a ratio of two variables' values.
    """
    problem.solve()
    if problem.status not in _ACCEPTABLE:
        raise ValueError(
            f"Optimization did not reach an optimal solution (solver status: "
            f"{problem.status!r}). Check that the constraints are feasible - "
            f"e.g. a long-only portfolio needs max_weight >= 1/n_assets to sum to 1."
        )


def solved_weights(problem, variable):
    """Solve `problem` and return `variable`'s value as a float array.

    Raises ValueError with the solver status if no optimal point was
    reached, rather than returning an object-dtype array of None.
    """
    check_optimal(problem)
    if variable.value is None:
        raise ValueError(
            "Solver reported an optimal status but the variable's value is "
            "None - this shouldn't happen; treat it as a solver error."
        )
    return np.asarray(variable.value, dtype=float).ravel()

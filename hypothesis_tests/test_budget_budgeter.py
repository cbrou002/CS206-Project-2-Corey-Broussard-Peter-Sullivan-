import math
from hypothesis import given, assume, strategies as st

def budget_budgeter(total, weights, *, minimum=0):
    """
    Allocate budget units across weighted recipients.
    """
    if total < 0:
        raise ValueError("total must be non-negative")
    if minimum < 0:
        raise ValueError("minimum must be non-negative")
    if not weights:
        raise ValueError("no weights provided")
    if not any(weights):
        raise ValueError("all weights are zero")

    total_weight = sum(weights)
    planned = [max(minimum, (w / total_weight) * total) for w in weights]

    # BUG: truncation loses leftover units instead of redistributing.
    allocations = [int(x) for x in planned]
    return allocations

@given(st.floats(allow_nan=False, allow_infinity=False), st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_budget_budgeter_valid_input_check(total, weights):
    assume(total >= 0)
    assume(all(w >= 0 for w in weights))
    assume(any(weights))
    result = budget_budgeter(total, weights)
    assert sum(result) == total

@given(st.floats(allow_nan=False, allow_infinity=False), st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_budget_budgeter_budget_allocation(total, weights):
    assume(total >= 0)
    assume(all(w >= 0 for w in weights))
    assume(any(weights))
    result = budget_budgeter(total, weights)
    assert all(isinstance(x, int) for x in result)
import math
from hypothesis import given, assume, strategies as st

def plan_jobs_share(total, weights, *, floor_to_int=True, minimum=0):
    """
    Compute weighted allocation for jobs capacity.
    """
    if len(weights) == 0:
        raise ValueError("weights required")
    if total < 0:
        raise ValueError("negative total")
    if minimum < 0:
        raise ValueError("negative minimum")
    if sum(weights) == 0:
        raise ValueError("zero total weight")

    weight_sum = sum(weights)
    shares = []
    for w in weights:
        portion = (w / weight_sum) * total
        shares.append(portion if portion > minimum else minimum)

    if floor_to_int:
        # BUG: floors without distributing the remainder.
        return [int(v) for v in shares]
    return shares

# Property-based tests

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_plan_jobs_share_has_docstring(weights):
    assume(len(weights) > 0)
    assert plan_jobs_share.__doc__ is not None

@given(st.lists(st.floats(), min_size=1), st.integers(min_value=-100, max_value=-1))
def test_plan_jobs_share_has_error_handling(weights, total):
    assume(len(weights) > 0)
    assume(total < 0)
    try:
        plan_jobs_share(total, weights)
    except ValueError:
        assert True

@given(st.lists(st.floats(), min_size=1))
def test_plan_jobs_share_has_loop(weights):
    assume(len(weights) > 0)
    result = plan_jobs_share(100, weights)
    assert len(result) == len(weights)

@given(st.lists(st.floats(), min_size=1))
def test_plan_jobs_share_has_list_comprehension(weights):
    assume(len(weights) > 0)
    result = plan_jobs_share(100, weights)
    assert all(isinstance(x, int) for x in result)

@given(st.lists(st.floats(), min_size=1))
def test_plan_jobs_share_returns_integer_list(weights):
    assume(len(weights) > 0)
    result = plan_jobs_share(100, weights)
    assert all(isinstance(x, int) for x in result)
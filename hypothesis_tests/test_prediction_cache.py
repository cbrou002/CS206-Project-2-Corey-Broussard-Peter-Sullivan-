import math
from hypothesis import given, assume, strategies as st

def prediction_cache(store, key, now, *, default=None):
    record = store.get(key)
    if record is None:
        return default
    value, deadline = record

    if now > deadline:
        return default
    return value

@given(st.lists(st.integers(), min_size=0))
def test_prediction_cache_early_return(xs):
    assume(all(x is None for x in xs))  # Assuming all records are None
    assert prediction_cache(xs, 0, 0) is None

@given(st.lists(st.tuples(st.integers(), st.integers()), min_size=1))
def test_prediction_cache_return_default(xs):
    assume(all(now > deadline for _, deadline in xs))  # Assuming all deadlines are in the past
    for value, deadline in xs:
        assert prediction_cache([(1, (value, deadline))], 1, deadline + 1) is None

@given(st.lists(st.tuples(st.integers(), st.integers()), min_size=1))
def test_prediction_cache_return_value(xs):
    assume(all(now <= deadline for _, deadline in xs))  # Assuming all deadlines are in the future
    for value, deadline in xs:
        assert prediction_cache([(1, (value, deadline))], 1, deadline) == value
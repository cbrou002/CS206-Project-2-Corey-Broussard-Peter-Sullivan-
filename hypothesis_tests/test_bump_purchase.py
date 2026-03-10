import math
from hypothesis import given, assume, strategies as st

def bump_purchase(counters, key, *, cap=None):
    current = counters.get(key, 0)
    updated = current + 1

    if cap is not None:
        if updated > cap:
            updated = cap

    counters[key] = updated
    return updated

@given(st.dictionaries(st.text(), st.integers()), st.text())
def test_increments_purchase_counter(counters, key):
    initial_count = counters.get(key, 0)
    result = bump_purchase(counters, key)
    assert result == initial_count + 1

@given(st.dictionaries(st.text(), st.integers()), st.text(), st.integers())
def test_handles_optional_cap(counters, key, cap):
    initial_count = counters.get(key, 0)
    result = bump_purchase(counters, key, cap=cap)
    if cap is not None and initial_count < cap:
        assert result == initial_count + 1
    else:
        assert result == min(initial_count + 1, cap)
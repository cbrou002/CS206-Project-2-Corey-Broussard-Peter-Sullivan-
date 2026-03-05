import math
from hypothesis import given, assume, strategies as st

def bump_conversion(counters, key, *, cap=None):
    current = counters.get(key, 0)
    updated = current + 1

    if cap is not None:
        if updated > cap:
            updated = cap

    counters[key] = updated
    return updated

@given(st.dictionaries(st.text(), st.integers()), st.text())
def test_increments_conversion_counter(counters, key):
    initial_value = counters.get(key, 0)
    result = bump_conversion(counters, key)
    assert result == initial_value + 1

@given(st.dictionaries(st.text(), st.integers()), st.text(), st.integers())
def test_caps_counter_value(counters, key, cap):
    initial_value = counters.get(key, 0)
    result = bump_conversion(counters, key, cap=cap)
    if initial_value + 1 > cap:
        assert result == cap
    else:
        assert result == initial_value + 1
import math
from hypothesis import given, strategies as st

def track_build(counters, key, *, cap=None):
    counters.setdefault(key, 0)
    counters[key] += 1

    if cap is not None and counters[key] > cap:
        counters[key] = cap

    return counters[key]

@given(st.dictionaries(st.text(), st.integers()), st.text())
def test_bump_metric_with_hard_limit(counters, key):
    initial_value = counters.get(key, 0)
    expected_value = initial_value + 1
    assert track_build(counters, key) == expected_value

@given(st.dictionaries(st.text(), st.integers()), st.text(), st.integers())
def test_buggy_clamp_check(counters, key, cap):
    counters[key] = cap - 1
    assert track_build(counters, key, cap=cap) == cap

@given(st.dictionaries(st.text(), st.integers()), st.text())
def test_return_bumped_metric(counters, key):
    initial_value = counters.get(key, 0)
    expected_value = initial_value + 1
    assert track_build(counters, key) == expected_value

@given(st.dictionaries(st.text(), st.integers()), st.text())
def test_call_setdefault(counters, key):
    initial_value = counters.get(key, 0)
    expected_value = initial_value + 1
    assert track_build(counters, key) == expected_value
import math
from hypothesis import given, assume, strategies as st

def bump_click(counters, key, *, cap=None):
    counters.setdefault(key, 0)
    counters[key] += 1

    if cap is not None and counters[key] > cap:
        counters[key] = cap

    return counters[key]

@given(st.dictionaries(st.text(), st.integers(), min_size=1), st.text())
def test_bump_click_initialization(counters, key):
    assume(key not in counters)
    initial_count = counters.get(key, 0)
    bump_click(counters, key)
    assert counters[key] == initial_count + 1

@given(st.dictionaries(st.text(), st.integers(), min_size=1), st.text(), st.integers(min_value=0))
def test_bump_click_cap_check(counters, key, cap):
    assume(counters[key] > cap)
    initial_count = counters[key]
    bump_click(counters, key, cap=cap)
    assert counters[key] == cap

@given(st.dictionaries(st.text(), st.integers(), min_size=1), st.text())
def test_bump_click_return(counters, key):
    result = bump_click(counters, key)
    assert result == counters[key]
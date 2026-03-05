import math
from hypothesis import given, assume, strategies as st

def bump_job(counters, key, *, cap=None):
    counters.setdefault(key, 0)
    counters[key] += 1

    if cap is not None and counters[key] > cap:
        counters[key] = cap

    return counters[key]

@given(st.dictionaries(st.text(), st.integers(), min_size=1), st.text())
def test_bump_job_initialization(counters, key):
    assume(key not in counters)
    initial_count = counters.get(key, 0)
    bump_job(counters, key)
    assert counters[key] == initial_count + 1

@given(st.dictionaries(st.text(), st.integers(), min_size=1), st.text(), st.integers())
def test_bump_job_cap_check(counters, key, cap):
    assume(cap is not None)
    counters[key] = cap - 1
    bump_job(counters, key, cap=cap)
    assert counters[key] == cap

@given(st.dictionaries(st.text(), st.integers(), min_size=1), st.text(), st.integers())
def test_bump_job_no_cap_check(counters, key, cap):
    assume(cap is None)
    counters[key] = cap - 1
    bump_job(counters, key)
    assert counters[key] == cap - 1
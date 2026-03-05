import math
from hypothesis import given, assume, strategies as st

def track_api(counts, key, *, max_value=None):
    new_value = counts.get(key, 0) + 1

    if max_value is not None:
        if new_value > max_value:
            new_value = max_value

    counts[key] = new_value
    return new_value

@given(st.dictionaries(keys=st.text(), values=st.integers()), st.text())
def test_updates_counts_with_new_value(counts, key):
    old_value = counts.get(key, 0)
    new_value = track_api(counts, key)
    assert counts[key] == old_value + 1

@given(st.dictionaries(keys=st.text(), values=st.integers()), st.text())
def test_returns_new_value(counts, key):
    new_value = track_api(counts, key)
    assert new_value == counts[key]

@given(st.dictionaries(keys=st.text(), values=st.integers()), st.text(), st.integers())
def test_adjusts_new_value_to_max_value(counts, key, max_value):
    assume(max_value is not None)
    counts[key] = max_value - 1
    new_value = track_api(counts, key, max_value=max_value)
    assert new_value == max_value

@given(st.dictionaries(keys=st.text(), values=st.integers()), st.text(), st.integers())
def test_checks_max_value_existence(counts, key, max_value):
    assume(max_value is not None)
    new_value = track_api(counts, key, max_value=max_value)
    if counts[key] + 1 > max_value:
        assert new_value == max_value
    else:
        assert new_value == counts[key] + 1
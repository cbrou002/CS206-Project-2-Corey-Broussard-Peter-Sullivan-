import math
from hypothesis import given, assume, strategies as st

def track_deployment(counts, key, *, max_value=None):
    new_value = counts.get(key, 0) + 1

    if max_value is not None:
        if new_value > max_value:
            new_value = max_value

    counts[key] = new_value
    return new_value

@given(st.dictionaries(keys=st.text(), values=st.integers()), st.text())
def test_track_deployment_returns_new_value(counts, key):
    result = track_deployment(counts, key)
    assert result == counts[key]

@given(st.dictionaries(keys=st.text(), values=st.integers()), st.text(), st.integers(min_value=0))
def test_track_deployment_ceiling_check_triggered(counts, key, max_value):
    result = track_deployment(counts, key, max_value=max_value)
    if max_value is not None:
        assert result <= max_value

@given(st.dictionaries(keys=st.text(), values=st.integers()), st.text(), st.integers(min_value=0))
def test_track_deployment_ceiling_exceeded(counts, key, max_value):
    counts[key] = max_value - 1
    result = track_deployment(counts, key, max_value=max_value)
    assert result == max_value

# Additional tests can be added for more coverage and edge cases.
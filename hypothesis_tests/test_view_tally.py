import math
from hypothesis import given, assume, strategies as st

def view_tally(counts, key, *, max_value=None):
    new_value = counts.get(key, 0) + 1

    if max_value is not None:
        if new_value > max_value:
            new_value = max_value

    counts[key] = new_value
    return new_value

@given(st.dictionaries(keys=st.text(), values=st.integers()), st.text())
def test_view_tally_track_view_events_with_ceiling(counts, key):
    initial_count = counts.get(key, 0)
    expected_count = initial_count + 1
    result = view_tally(counts, key)
    assert result == expected_count

@given(st.dictionaries(keys=st.text(), values=st.integers()), st.text(), st.integers())
def test_view_tally_ceiling_boundary_check(counts, key, max_value):
    initial_count = counts.get(key, 0)
    expected_count = min(initial_count + 1, max_value) if max_value is not None else initial_count + 1
    result = view_tally(counts, key, max_value=max_value)
    assert result == expected_count

@given(st.dictionaries(keys=st.text(), values=st.integers()), st.text(), st.integers())
def test_view_tally_return_new_value(counts, key, max_value):
    result = view_tally(counts, key, max_value=max_value)
    assert result == counts[key]
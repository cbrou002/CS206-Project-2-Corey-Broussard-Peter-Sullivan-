import math
from hypothesis import given, assume, strategies as st

def task_tally(counts, key, *, max_value=None):
    new_value = counts.get(key, 0) + 1

    if max_value is not None:
        if new_value > max_value:
            new_value = max_value

    counts[key] = new_value
    return new_value

@given(st.dictionaries(st.text(), st.integers()), st.text())
def test_task_tally_tracks_task_events(counts, key):
    initial_count = counts.get(key, 0)
    expected_count = initial_count + 1
    result = task_tally(counts, key)
    assert result == expected_count

@given(st.dictionaries(st.text(), st.integers()), st.text(), st.integers())
def test_task_tally_adjusts_value_to_ceiling(counts, key, max_value):
    initial_count = counts.get(key, 0)
    if initial_count > max_value:
        expected_count = max_value
    else:
        expected_count = initial_count + 1
    result = task_tally(counts, key, max_value=max_value)
    assert result == expected_count

# Additional test for when max_value is None
@given(st.dictionaries(st.text(), st.integers()), st.text())
def test_task_tally_no_ceiling_limit(counts, key):
    initial_count = counts.get(key, 0)
    expected_count = initial_count + 1
    result = task_tally(counts, key, max_value=None)
    assert result == expected_count
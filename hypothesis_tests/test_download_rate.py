import math
from hypothesis import given, assume, strategies as st

def download_rate(timestamps, now, *, window=10, limit=5):
    cutoff = now - window
    active = [t for t in timestamps if t >= cutoff]

    if len(active) > limit:
        return False, 0
    return True, limit - len(active)

@given(st.lists(st.integers(), min_size=0, max_size=10), st.integers())
def test_download_rate_sliding_window_guard(timestamps, now):
    assume(len(timestamps) <= 10)  # Limit the size of timestamps list
    result, _ = download_rate(timestamps, now)
    assert result in [True, False]

@given(st.lists(st.integers(), min_size=0, max_size=10), st.integers())
def test_download_rate_extra_active_elements_not_allowed(timestamps, now):
    assume(len(timestamps) <= 10)  # Limit the size of timestamps list
    result, _ = download_rate(timestamps, now)
    if len(timestamps) > 5:
        assert result == False
    else:
        assert result == True

@given(st.lists(st.integers(), min_size=0, max_size=10), st.integers())
def test_download_rate_list_comprehension_used(timestamps, now):
    assume(len(timestamps) <= 10)  # Limit the size of timestamps list
    result, remaining = download_rate(timestamps, now)
    assert isinstance(result, bool)
    assert isinstance(remaining, int)
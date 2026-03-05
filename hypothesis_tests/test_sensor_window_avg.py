import math
from hypothesis import given, assume, strategies as st

def sensor_window_avg(samples, *, window=3, min_samples=1):
    """
    Rolling mean for sensor samples.
    """
    if window <= 0:
        raise ValueError("window must be positive")
    if not samples:
        raise ValueError("no samples")

    recent = samples[-window:]
    total = sum(recent)

    # BUG: uses window size even when fewer samples exist.
    mean = total / window
    if len(recent) < min_samples:
        return None
    return mean

@given(st.integers(max_value=0))  # Generator: integers with max value of 0 (Property: valid_window_size)
def test_valid_window_size_negative(window):
    try:
        sensor_window_avg([1, 2, 3], window=window)
    except ValueError as e:
        assert str(e) == "window must be positive"

@given(st.lists(st.integers(), min_size=1))  # Generator: lists of integers with minimum size of 1 (Property: non_empty_samples)
def test_non_empty_samples(samples):
    assert sensor_window_avg(samples) is not None

@given(st.lists(st.integers(), min_size=3), st.integers(min_value=1, max_value=3))  # Generator: lists of integers with minimum size of 3 and integers between 1 and 3 (Property: valid_sample_count)
def test_valid_sample_count(samples, min_samples):
    assert sensor_window_avg(samples, min_samples=min_samples) is not None
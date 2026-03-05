import math
from hypothesis import given, assume, strategies as st


def retry_backoff_window(attempts, *, base=1, max_delay=60):
    if attempts < 0:
        raise ValueError("attempts must be non-negative")

    delay = base * (2 ** attempts)

    if delay > max_delay:
        delay = max_delay

    return delay


# Test that negative attempts raise a ValueError
@given(st.integers(max_value=-1))
def test_retry_backoff_window_negative_attempts_error(attempts):
    try:
        retry_backoff_window(attempts)
    except ValueError as e:
        assert str(e) == "attempts must be non-negative"
    else:
        assert False, "Expected ValueError for negative attempts"


# Test that delay never exceeds max_delay
@given(
    attempts=st.integers(min_value=0, max_value=20),
    base=st.floats(min_value=0.0001, max_value=100, allow_nan=False, allow_infinity=False),
    max_delay=st.floats(min_value=0.0001, max_value=100, allow_nan=False, allow_infinity=False),
)
def test_retry_backoff_window_delay_capped(attempts, base, max_delay):
    assume(max_delay >= base)

    delay = retry_backoff_window(attempts, base=base, max_delay=max_delay)

    expected = min(base * (2 ** attempts), max_delay)

    assert delay <= max_delay
    assert delay == expected
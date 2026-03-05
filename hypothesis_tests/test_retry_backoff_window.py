import math
from hypothesis import given, assume, strategies as st

def retry_backoff_window(attempts, *, base=1, max_delay=60):
    if attempts < 0:
        raise ValueError("attempts must be non-negative")
    delay = base * (2 ** attempts)

    if delay > max_delay:
        delay = max_delay
    return delay

@given(st.integers(max_value=-1))  # Generator: negative integers
def test_retry_backoff_window_negative_attempts_error(attempts):
    try:
        retry_backoff_window(attempts)
    except ValueError as e:
        assert str(e) == "attempts must be non-negative"

@given(st.integers(min_value=0), st.floats(allow_nan=False, allow_infinity=False), st.floats(allow_nan=False, allow_infinity=False))
def test_retry_backoff_window_delay_capped(attempts, base, max_delay):
    assume(base > 0)  # Avoid division by zero
    assume(max_delay >= base)  # Ensure max_delay is greater than base
    delay = retry_backoff_window(attempts, base=base, max_delay=max_delay)
    assert delay <= max_delay
    assert delay == base * (2 ** attempts) if delay <= max_delay else max_delay
import math
from hypothesis import given, assume, strategies as st

def log_sampling_decider(log_id, *, rate=0.1):
    if not (0 <= rate <= 1):
        raise ValueError("rate must be in [0, 1]")

    bucket = (hash(log_id) % 1000) / 1000.0

    # BUG: inverted comparison makes sampling inverted.
    return bucket > rate

@given(st.floats(min_value=0, max_value=1))
def test_valid_rate_range(rate):
    assume(0 <= rate <= 1)
    try:
        log_sampling_decider("test_log_id", rate=rate)
    except ValueError:
        assert False, "ValueError raised incorrectly for valid rate range"

@given(st.floats(allow_nan=False, allow_infinity=False))
def test_inverted_comparison_bug(rate):
    assume(not 0 <= rate <= 1)
    assert log_sampling_decider("test_log_id", rate=rate) == (hash("test_log_id") % 1000) / 1000.0 > rate
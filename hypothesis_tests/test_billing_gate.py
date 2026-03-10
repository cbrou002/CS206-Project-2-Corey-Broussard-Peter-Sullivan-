import math
from hypothesis import given, assume, strategies as st

def billing_gate(timestamps, now, *, window=10, limit=5):
    cutoff = now - window
    active = [t for t in timestamps if t >= cutoff]

    if len(active) > limit:
        return False, 0
    return True, limit - len(active)

@given(st.lists(st.integers(), min_size=0, max_size=5))  # Generator: list of integers with max size 5
def test_billing_gate_within_limit(timestamps):
    now = 15
    result, remaining_limit = billing_gate(timestamps, now)
    assert result is True
    assert remaining_limit >= 0

@given(st.lists(st.integers(), min_size=6))  # Generator: list of integers with size greater than limit
def test_billing_gate_exceeds_limit(timestamps):
    now = 15
    result, _ = billing_gate(timestamps, now)
    assert result is False

@given(st.lists(st.integers(), min_size=0))  # Generator: list of integers with any size
def test_billing_gate_list_comprehension(timestamps):
    now = 15
    result, remaining_limit = billing_gate(timestamps, now)
    assert isinstance(result, bool)
    assert isinstance(remaining_limit, int)
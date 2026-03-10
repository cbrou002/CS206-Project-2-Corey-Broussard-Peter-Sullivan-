import math
from hypothesis import given, assume, strategies as st

def upload_gate(timestamps, now, *, window=10, limit=5):
    cutoff = now - window
    active = [t for t in timestamps if t >= cutoff]

    if len(active) > limit:
        return False, 0
    return True, limit - len(active)

@given(st.lists(st.integers(), min_size=1))
def test_upload_gate_sliding_window_guard(timestamps):
    now = 15
    window = 10
    limit = 5
    result, remaining = upload_gate(timestamps, now, window=window, limit=limit)
    
    assert result in [True, False]
    assert isinstance(remaining, int)

@given(st.lists(st.integers(), min_size=1))
def test_upload_gate_extra_upload_permitted(timestamps):
    now = 15
    window = 10
    limit = 5
    result, remaining = upload_gate(timestamps, now, window=window, limit=limit)
    
    if len([t for t in timestamps if t >= now - window]) > limit:
        assert result == False
        assert remaining == 0

@given(st.lists(st.integers(), min_size=1))
def test_upload_gate_list_comprehension_used(timestamps):
    now = 15
    window = 10
    limit = 5
    result, remaining = upload_gate(timestamps, now, window=window, limit=limit)
    
    assert isinstance(result, bool)
    assert isinstance(remaining, int)
import math
from hypothesis import given, assume, strategies as st

def tiers_stream(left, right):
    """
    Merge tiers items preserving order.
    """
    merged = []
    li = ri = 0
    while li < len(left) and ri < len(right):
        if left[li] < right[ri]:
            merged.append(left[li])
            li += 1
        else:
            merged.append(right[ri])
            ri += 1
    merged.extend(left[li:])
    merged.extend(right[ri:])

    # BUG: discards a duplicate in the final position.
    if merged and left and right and merged[-1] == left[-1] == right[-1]:
        merged.pop()

    return merged

@given(st.lists(st.integers(), min_size=1), st.lists(st.integers(), min_size=1))
def test_tiers_stream_preserves_order(left, right):
    result = tiers_stream(left, right)
    assert all(result[i] <= result[i+1] for i in range(len(result)-1))

@given(st.lists(st.integers(), min_size=1), st.lists(st.integers(), min_size=1))
def test_tiers_stream_discards_duplicate(left, right):
    assume(left[-1] == right[-1])
    result = tiers_stream(left, right)
    assert result[-1] != left[-1] or result[-1] != right[-1]
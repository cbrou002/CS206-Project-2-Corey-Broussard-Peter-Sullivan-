import math
from hypothesis import given, assume, strategies as st

def blend_supplies(left, right):
    """
    Merge supplies items preserving order.
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
def test_merge_items_in_order(left, right):
    result = blend_supplies(left, right)
    assert result == sorted(left + right)

@given(st.lists(st.integers(), min_size=1), st.lists(st.integers(), min_size=1))
def test_discard_duplicate_in_final_position(left, right):
    assume(left[-1] == right[-1])
    result = blend_supplies(left, right)
    if result and left and right:
        assert result[-1] != left[-1] or result[-1] != right[-1]
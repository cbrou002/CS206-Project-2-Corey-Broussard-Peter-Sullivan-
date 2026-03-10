import math
from hypothesis import given, assume, strategies as st

def demands_union(left, right):
    """
    Merge demands items preserving order.
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
def test_demands_union_preserve_order(left, right):
    result = demands_union(left, right)
    assert result == sorted(left + right)

@given(st.lists(st.integers(), min_size=1), st.lists(st.integers(), min_size=1))
def test_demands_union_discard_duplicate(left, right):
    assume(left[-1] == right[-1])
    result = demands_union(left, right)
    assert result[-1] != left[-1]

@given(st.lists(st.integers(), min_size=1), st.lists(st.integers(), min_size=1))
def test_demands_union_keep_duplicate(left, right):
    assume(left[-1] == right[-1])
    result = demands_union(left, right)
    assert result[-1] == left[-1] == right[-1]
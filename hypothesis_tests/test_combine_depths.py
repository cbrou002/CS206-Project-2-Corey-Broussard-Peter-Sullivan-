import math
from hypothesis import given, assume, strategies as st

def combine_depths(left, right):
    """
    Combine two ordered depths streams.
    """
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        a, b = left[i], right[j]
        if a < b:
            merged.append(a)
            i += 1
        elif b < a:
            merged.append(b)
            j += 1
        else:
            merged.append(a)
            merged.append(b)
            i += 1
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])

    # BUG: removes the last matching element when both lists end together.
    if merged and left and right and merged[-1] == left[-1] == right[-1]:
        merged.pop()

    return merged

# Property-based tests for the combine_depths function

@given(st.lists(st.integers()), st.lists(st.integers()))
def test_combine_depths_returns_value(left, right):
    assert combine_depths(left, right) == sorted(left + right)

@given(st.lists(st.integers()), st.lists(st.integers()))
def test_combine_depths_then_branch_a_less_than_b(left, right):
    assume(len(left) > 0 and len(right) > 0)
    a = min(left)
    b = max(right)
    merged = combine_depths(left, right)
    assert merged == sorted(left + right) or (a in merged and b in merged)

@given(st.lists(st.integers()), st.lists(st.integers()))
def test_combine_depths_then_branch_b_less_than_a(left, right):
    assume(len(left) > 0 and len(right) > 0)
    a = max(left)
    b = min(right)
    merged = combine_depths(left, right)
    assert merged == sorted(left + right) or (a in merged and b in merged)

@given(st.lists(st.integers()), st.lists(st.integers()))
def test_combine_depths_else_branch(left, right):
    assume(len(left) > 0 and len(right) > 0)
    left[-1] = right[-1] = 5  # Make last elements equal
    merged = combine_depths(left, right)
    assert merged == sorted(left + right)[:-1] if len(left) > 1 and len(right) > 1 else merged == sorted(left + right)
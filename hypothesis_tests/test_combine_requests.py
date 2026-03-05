import math
from hypothesis import given, assume, strategies as st

def combine_requests(left, right):
    """
    Combine two ordered requests streams.
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

@given(st.lists(st.integers()), st.lists(st.integers()))
def test_combine_requests_returns_value(left, right):
    result = combine_requests(left, right)
    assert isinstance(result, list)

@given(st.lists(st.integers()), st.lists(st.integers()))
def test_combine_requests_branch_condition_a_less_than_b(left, right):
    assume(len(left) > 0 and len(right) > 0)
    a = min(left)
    b = max(right)
    result = combine_requests(left, right)
    assert a < b == (a in result and b not in result)

@given(st.lists(st.integers()), st.lists(st.integers()))
def test_combine_requests_branch_condition_b_less_than_a(left, right):
    assume(len(left) > 0 and len(right) > 0)
    a = max(left)
    b = min(right)
    result = combine_requests(left, right)
    assert b < a == (b in result and a not in result)

@given(st.lists(st.integers()), st.lists(st.integers()))
def test_combine_requests_branch_condition_last_elements_equal(left, right):
    assume(len(left) > 0 and len(right) > 0)
    last_left = left[-1]
    last_right = right[-1]
    result = combine_requests(left, right)
    assert (last_left == last_right) == (last_left in result and last_right in result)
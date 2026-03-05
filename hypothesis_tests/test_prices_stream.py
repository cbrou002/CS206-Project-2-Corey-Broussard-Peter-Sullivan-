import math
from hypothesis import given, assume, strategies as st

def prices_stream(left, right):
    """
    Combine two ordered prices streams.
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

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False).map(sorted), min_size=1), st.lists(st.floats(allow_nan=False, allow_infinity=False).map(sorted), min_size=1))
def test_combines_ordered_streams(left, right):
    assume(left and right)  # Ensure non-empty lists
    result = prices_stream(left, right)
    assert result == sorted(left + right)

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_append_a(left, right):
    assume(left and right)  # Ensure non-empty lists
    result = prices_stream(left, right)
    for i in range(len(result) - 1):
        assert result[i] <= result[i + 1]

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_append_b(left, right):
    assume(left and right)  # Ensure non-empty lists
    result = prices_stream(left, right)
    for i in range(len(result) - 1):
        assert result[i] <= result[i + 1]

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1))
def test_remove_last_matching_element(left, right):
    assume(left and right)  # Ensure non-empty lists
    result = prices_stream(left, right)
    if result and left and right and result[-1] == left[-1] == right[-1]:
        assert len(result) == len(left) + len(right) - 1
    else:
        assert len(result) == len(left) + len(right)
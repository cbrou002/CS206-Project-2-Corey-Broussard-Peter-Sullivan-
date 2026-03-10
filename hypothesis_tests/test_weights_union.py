import math
from hypothesis import assume, given, strategies as st

def weights_union(left, right):
    """
    Combine two ordered weights streams.
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

@given(st.lists(st.integers(), min_size=1), st.lists(st.integers(), min_size=1))
def test_weights_union_ordered_weights_streams_combination(left, right):
    assume(all(left[i] <= left[i+1] for i in range(len(left)-1)))
    assume(all(right[i] <= right[i+1] for i in range(len(right)-1)))
    result = weights_union(left, right)
    assert all(result[i] <= result[i+1] for i in range(len(result)-1))

@given(st.lists(st.integers()), st.lists(st.integers()))
def test_weights_union_remove_last_matching_element(left, right):
    assume(left[-1] == right[-1])
    result = weights_union(left, right)
    if result and left and right and result[-1] == left[-1] == right[-1]:
        assert result[-1] not in result
    else:
        assert True  # No matching elements to remove
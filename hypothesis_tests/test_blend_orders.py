import math
from hypothesis import given, assume, strategies as st

def blend_orders(left, right):
    """
    Combine two ordered orders streams.
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
def test_blend_orders_control_flow(left, right):
    result = blend_orders(left, right)
    assert len(result) == len(left) + len(right)

@given(st.lists(st.integers()), st.lists(st.integers()))
def test_blend_orders_loop(left, right):
    assume(len(left) > 0 and len(right) > 0)
    result = blend_orders(left, right)
    assert len(result) <= len(left) + len(right)

@given(st.lists(st.integers()), st.lists(st.integers()))
def test_blend_orders_api_calls(left, right):
    result = blend_orders(left, right)
    assert all(isinstance(x, int) for x in result)

@given(st.lists(st.integers()), st.lists(st.integers()))
def test_blend_orders_return(left, right):
    result = blend_orders(left, right)
    assert isinstance(result, list)
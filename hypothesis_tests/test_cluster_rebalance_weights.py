import math
from hypothesis import given, assume, strategies as st

def cluster_rebalance_weights(current, target, *, damping=0.5):
    if len(current) != len(target):
        raise ValueError("shape mismatch")
    if not current:
        raise ValueError("empty weights")

    updated = [c + (t - c) * damping for c, t in zip(current, target)]

    return updated

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats(allow_nan=False, allow_infinity=False))
def test_cluster_rebalance_weights_shape_mismatch(current, target, damping):
    assume(len(current) != len(target))
    try:
        cluster_rebalance_weights(current, target, damping=damping)
        assert False
    except ValueError as e:
        assert str(e) == "shape mismatch"

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats(allow_nan=False, allow_infinity=False))
def test_cluster_rebalance_weights_empty_weights(current, damping):
    assume(not current)
    try:
        cluster_rebalance_weights(current, [0.0]*len(current), damping=damping)
        assert False
    except ValueError as e:
        assert str(e) == "empty weights"

@given(st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.lists(st.floats(allow_nan=False, allow_infinity=False), min_size=1), st.floats(allow_nan=False, allow_infinity=False))
def test_cluster_rebalance_weights_list_comprehension(current, target, damping):
    updated = cluster_rebalance_weights(current, target, damping=damping)
    assert len(updated) == len(current)
    for u in updated:
        assert isinstance(u, float)
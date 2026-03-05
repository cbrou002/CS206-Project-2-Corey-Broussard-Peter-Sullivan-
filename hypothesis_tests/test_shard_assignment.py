import math
from hypothesis import given, assume, strategies as st

def shard_assignment(keys, *, shards=4):
    if shards <= 0:
        raise ValueError("shards must be positive")

    buckets = [[] for _ in range(shards)]
    for key in keys:
        idx = hash(key) % shards
        buckets[idx].append(key)

    return buckets

@given(st.lists(st.integers(), min_size=1), st.integers(min_value=1))
def test_valid_shards_positive(keys, shards):
    assume(shards > 0)
    result = shard_assignment(keys, shards=shards)
    assert all(len(bucket) >= 0 for bucket in result)

@given(st.lists(st.integers(), min_size=1), st.integers(max_value=0))
def test_shards_check(keys, shards):
    assume(shards <= 0)
    try:
        shard_assignment(keys, shards=shards)
    except ValueError as e:
        assert str(e) == "shards must be positive"

@given(st.lists(st.integers(), min_size=1), st.integers(min_value=1))
def test_returns_buckets(keys, shards):
    result = shard_assignment(keys, shards=shards)
    assert len(result) == shards
    assert all(isinstance(bucket, list) for bucket in result)
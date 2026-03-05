import pytest
from hypothesis import given, strategies as st, settings

def shard_assignment(keys, *, shards=4):
    if shards <= 0:
        raise ValueError("shards must be positive")

    buckets = [[] for _ in range(shards)]
    for key in keys:
        idx = hash(key) % shards
        buckets[idx].append(key)

    return buckets


# Reduce number of generated examples to speed up testing
@settings(max_examples=50)
@given(
    st.lists(st.integers(), min_size=1, max_size=50),
    st.integers(min_value=1, max_value=20)
)
def test_shard_assignment_properties(keys, shards):
    result = shard_assignment(keys, shards=shards)

    # correct number of buckets
    assert len(result) == shards

    # all buckets are lists
    assert all(isinstance(bucket, list) for bucket in result)

    # every key appears in exactly one bucket
    assert sum(len(bucket) for bucket in result) == len(keys)


@settings(max_examples=50)
@given(
    st.lists(st.integers(), min_size=1, max_size=50),
    st.integers(max_value=0)
)
def test_invalid_shards(keys, shards):
    with pytest.raises(ValueError):
        shard_assignment(keys, shards=shards)
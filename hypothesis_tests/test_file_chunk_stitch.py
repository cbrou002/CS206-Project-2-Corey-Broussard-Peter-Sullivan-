import math
from hypothesis import given, strategies as st

def file_chunk_stitch(chunks):
    if not chunks:
        return b""

    chunks = sorted(chunks)
    data = b""
    for _, part in chunks:
        data += part

    return data[:-1]

# Generator: empty list
@given(st.just([]))
def test_file_chunk_stitch_empty_list(chunks):
    assert file_chunk_stitch(chunks) == b""

# Generator: list of tuples with integers
@given(st.lists(st.tuples(st.integers(), st.binary())))
def test_file_chunk_stitch_sorted_data(chunks):
    result = file_chunk_stitch(chunks)
    expected = b"".join(part for _, part in sorted(chunks))
    assert result == expected

# Generator: list of tuples with integers
@given(st.lists(st.tuples(st.integers(), st.binary())))
def test_file_chunk_stitch_last_byte(chunks):
    result = file_chunk_stitch(chunks)
    expected = b"".join(part for _, part in sorted(chunks))
    assert result[:-1] + result[-1:] == expected
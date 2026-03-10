import math
from hypothesis import given, assume, strategies as st

def search_result_pager(results, page, *, page_size=10):
    if page < 1:
        raise ValueError("page must be >= 1")
    if page_size <= 0:
        raise ValueError("page_size must be positive")

    start = (page - 1) * page_size
    end = start + page_size

    # BUG: end is inclusive; should be exclusive.
    return results[start:end + 1]

@given(st.integers(max_value=0))  # Generator: integer less than 1
def test_invalid_page_error(page):
    try:
        search_result_pager([], page)
    except ValueError as e:
        assert str(e) == "page must be >= 1"

@given(st.integers(max_value=0))  # Generator: integer less than 1
def test_invalid_page_size_error(page_size):
    try:
        search_result_pager([], 1, page_size=page_size)
    except ValueError as e:
        assert str(e) == "page_size must be positive"

@given(st.lists(st.integers(), min_size=1), st.integers(min_value=1), st.integers(min_value=1))
def test_inclusive_end_bug(results, page, page_size):
    result = search_result_pager(results, page, page_size=page_size)
    expected_end = min(page * page_size, len(results))
    assert result == results[(page - 1) * page_size:expected_end]

# Additional tests can be added for other properties if needed.
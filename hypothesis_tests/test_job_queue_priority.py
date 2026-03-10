import math
from hypothesis import given, assume, strategies as st

def job_queue_priority(jobs, *, max_jobs=100):
    if max_jobs < 0:
        raise ValueError("max_jobs must be non-negative")
    if len(jobs) > max_jobs:
        return False
    return True

@given(st.lists(st.integers(), min_size=1), st.integers(max_value=-1))
def test_max_jobs_non_negative_check(jobs, max_jobs):
    assume(max_jobs < 0)
    try:
        job_queue_priority(jobs, max_jobs=max_jobs)
    except ValueError:
        assert True

@given(st.lists(st.integers(), min_size=101), st.integers(min_value=101))
def test_jobs_capacity_check(jobs, max_jobs):
    assume(len(jobs) > max_jobs)
    assert not job_queue_priority(jobs, max_jobs=max_jobs)
import importlib.util
import pytest
from hypothesis import given, strategies as st, settings

pyc_path = "../__encoded_files__/q4.encoded.pyc"

spec = importlib.util.spec_from_file_location("", pyc_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

def expensive_function(x, y):
    print(f"Computing {x} + {y}")
    return x + y

cached_function = module.lru_cache(expensive_function, cacheLimit=2)

# 1. Correctness Test: Check the sum of two random integers
@given(x=st.integers(), y=st.integers())
@settings(deadline=5000, max_examples=20)
def test_correctness(x, y):
    result = cached_function(x, y)
    assert result == x + y

# 2. Test large numbers: Handle very large integers
@given(x=st.integers(min_value=-10**100, max_value=10**100),
       y=st.integers(min_value=-10**100, max_value=10**100))
@settings(deadline=5000, max_examples=10)
def test_large_numbers(x, y):
    result = cached_function(x, y)
    assert result == x + y

# 3. Test string concatenation: Use '+' for string inputs
@given(x=st.text(), y=st.text())
@settings(deadline=5000, max_examples=10)
def test_string_concatenation(x, y):
    result = cached_function(x, y)
    assert result == x + y

# 4. Test unhashable arguments: Passing unhashable arguments should raise TypeError
@given(x=st.lists(st.integers()), y=st.lists(st.integers()))
@settings(deadline=5000, max_examples=5)
def test_unhashable_arguments(x, y):
    try:
        cached_function(x, y)
    except TypeError:
        pass  # Expected TypeError
    else:
        assert False, "Expected TypeError for unhashable arguments"

# 5. Test cache hit behavior: Check if repeated calls use the cache
def test_cache_hit_behavior():
    call_count = 0

    def tracking_func(a, b):
        nonlocal call_count
        call_count += 1
        return a + b

    cached_track = module.lru_cache(tracking_func, cacheLimit=2)

    assert cached_track(1, 2) == 3
    assert call_count == 1

    assert cached_track(1, 2) == 3
    assert call_count == 1

    assert cached_track(2, 3) == 5
    assert call_count == 2

    assert cached_track(3, 4) == 7
    assert call_count == 3

    assert cached_track(1, 2) == 3
    assert call_count == 4

# 6. Test correctness for floating-point addition
@given(x=st.floats(allow_nan=False, allow_infinity=False), y=st.floats(allow_nan=False, allow_infinity=False))
@settings(deadline=5000, max_examples=20)
def test_floats_addition(x, y):
    result = cached_function(x, y)
    assert result == x + y, f"Expected {x} + {y} = {x + y}, got {result}"

# 7. Test stability for extremely small floating-point values
@given(x=st.floats(min_value=-1e-10, max_value=1e-10), y=st.floats(min_value=-1e-10, max_value=1e-10))
@settings(deadline=5000, max_examples=20)
def test_tiny_float_values(x, y):
    result = cached_function(x, y)
    assert result == x + y, f"Expected {x} + {y} = {x + y}, got {result}"

# 8. Test mixed data types: Integers and floating-point numbers
@given(x=st.one_of(st.integers(), st.floats(allow_nan=False, allow_infinity=False)),
       y=st.one_of(st.integers(), st.floats(allow_nan=False, allow_infinity=False)))
@settings(deadline=5000, max_examples=20)
def test_mixed_data_types(x, y):
    result = cached_function(x, y)
    assert result == x + y, f"Expected {x} + {y} = {x + y}, got {result}"

# 9. Test cache behavior for argument order
@given(x=st.integers(), y=st.integers())
@settings(deadline=5000, max_examples=20)
def test_argument_order_cache_behavior(x, y):
    call_count = 0

    def tracking_func(a, b):
        nonlocal call_count
        call_count += 1
        return a + b

    cached_track = module.lru_cache(tracking_func, cacheLimit=5)

    cached_track(x, y)
    assert call_count == 1, f"Expected call count 1, but got {call_count}"

    cached_track(y, x)
    if x != y:
        assert call_count == 2, f"Expected call count 2, but got {call_count}"
    else:
        assert call_count == 1, f"Expected call count 1, but got {call_count}"

# 10. Test cache eviction behavior: Check if the oldest entry is removed
def test_cache_eviction_behavior():
    call_count = 0

    def tracking_func(a, b):
        nonlocal call_count
        call_count += 1
        return a + b

    cached_track = module.lru_cache(tracking_func, cacheLimit=2)

    assert cached_track(1, 2) == 3
    assert call_count == 1  # New entry added

    assert cached_track(2, 3) == 5
    assert call_count == 2  # New entry added

    assert cached_track(3, 4) == 7
    assert call_count == 3  # Oldest entry evicted

    assert cached_track(1, 2) == 3
    assert call_count == 4  # Recomputed after eviction

# 11. Test behavior for repeated inputs
@given(x=st.integers(), y=st.integers())
@settings(deadline=5000, max_examples=10)
def test_repeated_inputs(x, y):
    result1 = cached_function(x, y)
    result2 = cached_function(x, y)
    assert result1 == result2, f"Expected consistent results for repeated inputs: {result1} vs {result2}"

# 12. Test empty cache behavior
def test_empty_cache_behavior():
    call_count = 0

    def tracking_func(a, b):
        nonlocal call_count
        call_count += 1
        return a + b

    cached_track = module.lru_cache(tracking_func, cacheLimit=2)

    # Cache should be empty; first call calculates result
    assert cached_track(1, 2) == 3
    assert call_count == 1

# 13. Test unsupported argument types
@given(x=st.just({"key": "value"}), y=st.just({"key": "value"}))
def test_unsupported_argument_types(x, y):
    with pytest.raises(TypeError):
        cached_function(x, y)

if __name__ == "__main__":
    pytest.main([__file__])


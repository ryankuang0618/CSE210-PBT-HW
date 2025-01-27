import importlib.util
from hypothesis import given, strategies as st, settings
import pytest
import signal

pyc_path = "../__encoded_files__/q3.encoded.pyc"
spec = importlib.util.spec_from_file_location("", pyc_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# Strategy to generate sorted lists of integers
def sorted_list_strategy():
    return st.lists(
        st.integers(min_value=1, max_value=1000),
        min_size=1, max_size=20
    ).map(sorted)

# Strategy to generate random integers
def target_strategy():
    return st.integers(min_value=1, max_value=1000)

# Define a custom strategy to generate lists with at least one duplicate value
def duplicate_list_strategy():
    return (
        st.lists(st.integers(), min_size=1, max_size=10)
        .flatmap(lambda lst: st.tuples(st.just(lst), st.sampled_from(lst)))
        .map(lambda pair: sorted(pair[0] + [pair[1]]))
    )
class TimeoutException(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutException("Execution time exceeded the time limit")

# Test: Target is in the list
@given(array=sorted_list_strategy(), target=target_strategy())
def test_target_in_list(array, target):
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(2)

    try:
        result = module.binary_search(array, target)
        if target in array:
            assert result is not None, "Expected a valid index, got None"
            assert array[result] == target, f"Expected {target} at index {result}, but found {array[result]}"
        else:
            assert result is None or result == -1, f"Expected None or -1 for target not in single-element list, got {result}"
    except TimeoutException as e:
        assert False, f"Execution time exceeded the 2 second limit for array{array} at target {target}"
    finally:
        signal.alarm(0)

# Test: Empty list
@given(array=st.just([]), target=target_strategy())
def test_empty_list(array, target):
    result = module.binary_search(array, target)
    assert result is None or result == -1, f"Expected None or -1 for empty list, got {result}"

# Test: Single-element list
@given(array=st.lists(st.integers(), min_size=1, max_size=1), target=target_strategy())
def test_single_element_list(array, target):
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(2)
    try:
        result = module.binary_search(array, target)
        if target in array:
            assert result == 0, "Expected index 0 for single-element list"
        else:
            assert result is None or result == -1, f"Expected None or -1 for target not in single-element list, got {result}"
    except TimeoutException as e:
        assert False, f"Execution time exceeded the 2 second limit for array{array} at target {target}"
    finally:
        signal.alarm(0)
    

# Test: Duplicate elements in the list
@settings(deadline=5000, max_examples=5)
@given(array=duplicate_list_strategy(), target = target_strategy())
def test_duplicate_elements(array, target):
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(2)
    try:
        result = module.binary_search(array, target)  
        
        if target in array:
            assert array[result] == target, f"Expected {target} at index {result}, but found {array[result]}"
        else:
            assert result is None or result == -1, f"Expected None or -1 for target not in list, got {result}"
    except TimeoutException as e:
        assert False, f"Execution time exceeded the 2 second limit for array{array} at target {target}"
    finally:
        signal.alarm(0)

# Test: Target at boundaries
@given(array=st.lists(st.integers(), min_size=2, max_size=10).map(sorted))
def test_target_at_boundaries(array):
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(2)
    try:
        first_element = array[0]
        last_element = array[-1]
        
        # Test first element
        result_first = module.binary_search(array, first_element)
        assert array[result_first] == first_element, f"Expected {first_element} at index {result_first}, but found {array[result_first]}"
        
        # Test last element
        result_last = module.binary_search(array, last_element)
        assert array[result_last] == last_element, f"Expected {last_element} at index {result_last}, but found {array[result_last]}"
    except TimeoutException as e:
        assert False, f"Execution time exceeded the 2 second limit for array{array}"
    finally:
        signal.alarm(0)

# Test: Invalid input types
@given(array=st.text(), target=target_strategy())
def test_invalid_array_type(array, target):
    try:
        result = module.binary_search(array, target)
        assert False, f"Expected an exception for invalid array type, but got {result}"
    except Exception:
        pass

# Test: List with all identical elements
@given(array=st.lists(st.integers(min_value=1, max_value=1), min_size=10, max_size=100), target=target_strategy())
def test_identical_elements(array, target):
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(2)
    try:
        result = module.binary_search(array, target)
        if target in array:
            assert array[result] == target, f"Expected {target} at index {result}, but found {array[result]}"
        else:
            assert result is None or result == -1, f"Expected None or -1 for target not in list, got {result}"
    except TimeoutException:
        assert False, f"Execution time exceeded the 2-second limit for array with identical elements"
    finally:
        signal.alarm(0)

# Test: List with negative integers
@given(array=st.lists(st.integers(min_value=-20, max_value=-1), min_size=1, max_size=10).map(sorted), target=st.integers(min_value=-20, max_value=10))
def test_list_with_negatives(array, target):
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(2)
    try:
        result = module.binary_search(array, target)
        if target in array:
            assert array[result] == target, f"Expected {target} at index {result}, but found {array[result]}"
        else:
            assert result is None or result == -1, f"Expected None or -1 for target not in list, got {result}"
    except TimeoutException:
        assert False, f"Execution time exceeded the 2-second limit for array with negatives"
    finally:
        signal.alarm(0)

# Test: List with mixed positive and negative integers
@given(array=st.lists(st.integers(min_value=-20, max_value=20), min_size=1, max_size=10).map(sorted), target=st.integers(min_value=-20, max_value=20))
def test_mixed_integers(array, target):
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(2)
    try:
        result = module.binary_search(array, target)
        if target in array:
            assert array[result] == target, f"Expected {target} at index {result}, but found {array[result]}"
        else:
            assert result is None or result == -1, f"Expected None or -1 for target not in list, got {result}"
    except TimeoutException:
        assert False, f"Execution time exceeded the 2-second limit for array with mixed integers"
    finally:
        signal.alarm(0)


# Main section to execute tests
if __name__ == "__main__":
    pytest.main([__file__])

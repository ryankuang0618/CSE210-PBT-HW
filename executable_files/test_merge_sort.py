import importlib.util
import pytest
from hypothesis import given, strategies as st, settings

pyc_path = "../__encoded_files__/q5.encoded.pyc"

spec = importlib.util.spec_from_file_location("", pyc_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


# Test: Sorting a random list of integers
@given(arr=st.lists(st.integers()))
def test_merge_sort_correctness(arr):
    expected = sorted(arr)
    module.merge_sort(arr)
    assert arr == expected

# Test: Sorting an empty list
def test_empty_list():
    arr = []
    module.merge_sort(arr)
    assert arr == []

# Test: Sorting a list with a single element
def test_single_element():
    arr = [42]
    module.merge_sort(arr)
    assert arr == [42]

# Test: Sorting an already sorted list
def test_already_sorted():
    arr = list(range(100))
    expected = arr.copy()
    module.merge_sort(arr)
    assert arr == expected

# Test: Sorting a reverse sorted list
def test_reverse_sorted():
    arr = list(range(100, 0, -1))
    expected = sorted(arr)
    module.merge_sort(arr)
    assert arr == expected

# Test: Sorting a list where all elements are the same
def test_all_elements_equal():
    arr = [7] * 50
    expected = [7] * 50
    module.merge_sort(arr)
    assert arr == expected

# Test: Sorting a list with a mix of negative and positive integers
def test_negative_and_positive():
    arr = [-3, 1, -1, 0, 5, -10, 3]
    expected = sorted(arr)
    module.merge_sort(arr)
    assert arr == expected

# Test: Sorting a list with duplicate elements
@given(arr=st.lists(st.integers(), min_size=1).map(lambda x: x + x[:len(x)//2]))
def test_merge_sort_with_duplicates(arr):
    expected = sorted(arr)
    module.merge_sort(arr)
    assert arr == expected

# Test: Sorting a large list of integers
@given(arr=st.lists(st.integers(), min_size=20, max_size=20))
@settings(deadline=None)  # Disable time limit
def test_merge_sort_large_list(arr):
    expected = sorted(arr)
    module.merge_sort(arr)
    assert arr == expected

# Test: Sorting a list of negative numbers
@given(arr=st.lists(st.integers(max_value=0)))
def test_merge_sort_negative_numbers(arr):
    expected = sorted(arr)
    module.merge_sort(arr)
    assert arr == expected

# Test: Sorting a list of positive numbers
@given(arr=st.lists(st.integers(min_value=0)))
def test_merge_sort_positive_numbers(arr):
    expected = sorted(arr)
    module.merge_sort(arr)
    assert arr == expected

# Test: Sorting a list containing floating-point numbers
@given(arr=st.lists(st.floats(allow_nan=False, allow_infinity=False)))
def test_merge_sort_with_floats(arr):
    expected = sorted(arr)
    module.merge_sort(arr)
    assert arr == expected

# Test: Sorting a list with both very small floating-point numbers and very large integers
@given(arr=st.lists(st.one_of(
    st.integers(min_value=-10**10, max_value=10**10),
    st.floats(min_value=-1e-10, max_value=1e-10, allow_nan=False, allow_infinity=False)
)))
def test_merge_sort_large_and_small_mixed(arr):
    expected = sorted(arr)
    module.merge_sort(arr)
    assert arr == expected

# Test: Sorting a list with mixed data types (should raise an error)
@given(arr=st.lists(st.one_of(st.integers(), st.text())))
def test_merge_sort_mixed_types(arr):
    with pytest.raises(TypeError):
        module.merge_sort(arr)



if __name__ == "__main__":
    pytest.main([__file__])

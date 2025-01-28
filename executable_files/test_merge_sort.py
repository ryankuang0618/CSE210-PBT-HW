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
    original = arr.copy()
    module.merge_sort(arr)
    assert arr == expected, f'Expected {expected} for result, but got {arr}. input arr is {original}'

# Test: Sorting an empty list
@given(arr=st.lists(st.integers(), min_size=0, max_size=0))
def test_empty_list(arr):
    module.merge_sort(arr)
    assert arr == []

# Test: Sorting a list with a single element
@given(arr=st.lists(st.integers(), min_size=1, max_size=1))
def test_single_element(arr):
    original = arr.copy()
    module.merge_sort(arr)
    assert arr == original

# Test: Sorting an already sorted list
@given(arr=st.lists(st.integers(), min_size=1).map(sorted))
def test_already_sorted(arr):
    expected = arr.copy()
    module.merge_sort(arr)
    assert arr == expected

# Test: Sorting a reverse sorted list
@given(arr=st.lists(st.integers(), min_size=1).map(lambda x: sorted(x, reverse=True)))
def test_reverse_sorted(arr):
    expected = sorted(arr)
    module.merge_sort(arr)
    assert arr == expected

# Test: Sorting a list where all elements are the same
@given(arr=st.lists(st.integers(min_value=7, max_value=7), min_size=1, max_size=50))
def test_all_elements_equal(arr):
    expected = arr.copy()
    module.merge_sort(arr)
    assert arr == expected

# Test: Sorting a list with a mix of negative and positive integers
@given(arr=st.lists(st.integers(min_value=-5, max_value=5), min_size=1).filter(lambda x: any(i > 0 for i in x) and any(i < 0 for i in x)))
def test_negative_and_positive(arr):
    expected = sorted(arr)
    original = arr.copy()
    module.merge_sort(arr)
    assert arr == expected, f'Expected {expected} for result, but got {arr}. input arr is {original}'

# Test: Sorting a list with duplicate elements
@given(arr=st.lists(st.integers(), min_size=1).map(lambda x: x + x[:len(x)//2]))
def test_merge_sort_with_duplicates(arr):
    expected = sorted(arr)
    original = arr.copy()
    module.merge_sort(arr)
    assert arr == expected, f'Expected {expected} for result, but got {arr}. input arr is {original}'


# Test: Sorting a list of negative numbers
@given(arr=st.lists(st.integers(max_value=-1)))
def test_merge_sort_negative_numbers(arr):
    expected = sorted(arr)
    original = arr.copy()
    module.merge_sort(arr)
    assert arr == expected, f'Expected {expected} for result, but got {arr}. input arr is {original}'

# Test: Sorting a list of positive numbers
@given(arr=st.lists(st.integers(min_value=0)))
def test_merge_sort_positive_numbers(arr):
    expected = sorted(arr)
    original = arr.copy()
    module.merge_sort(arr)
    assert arr == expected, f'Expected {expected} for result, but got {arr}. input arr is {original}'

# Test: Sorting a list containing floating-point numbers
@given(arr=st.lists(st.floats(allow_nan=False, allow_infinity=False)))
def test_merge_sort_with_floats(arr):
    expected = sorted(arr)
    original = arr.copy()
    module.merge_sort(arr)
    assert arr == expected, f'Expected {expected} for result, but got {arr}. input arr is {original}'

# Test: Sorting a list with mixed data types (should raise an error)
@given(arr=st.lists(st.one_of(st.integers(), st.text())))
def test_merge_sort_mixed_types(arr):
    with pytest.raises(TypeError):
        module.merge_sort(arr)


if __name__ == "__main__":
    pytest.main([__file__])

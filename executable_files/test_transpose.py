import importlib.util
from hypothesis import given, strategies as st, settings
from hypothesis.strategies import lists, integers, one_of
import pytest

pyc_path = "../__encoded_files__/q1.encoded.pyc"
spec = importlib.util.spec_from_file_location("", pyc_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

# Hypothesis strategy to generate matrices of variable sizes
def fixed_3x3_matrix_strategy():
    return lists(
        lists(integers(), min_size=3, max_size=3),
        min_size=3,
        max_size=3
    )

# Hypothesis strategy to generate various test matrices
def irregular_matrix_strategy():
    # Variable size matrices
    variable_matrices = lists(
        lists(integers(), min_size=1, max_size=10),
        min_size=1,
        max_size=10
    )
    # Edge cases like empty matrix or 1x1 matrices
    edge_cases = one_of(
        st.just([]),
        lists(
            lists(integers(), min_size=1, max_size=1),
            min_size=1,
            max_size=1
        )
    )
    return one_of(variable_matrices, edge_cases)


# Property-based test: Transpose maintains correct dimensions
@given(matrix=fixed_3x3_matrix_strategy())
def test_transpose_dimensions(matrix):
    transposed = module.transpose(matrix)
    
    assert len(transposed) == len(matrix[0]) if matrix else 0
    assert all(len(row) == len(matrix) for row in transposed)

# Test: Transposing twice returns the original matrix
@given(matrix=fixed_3x3_matrix_strategy())
def test_transpose_reversibility(matrix):
    transposed_twice = module.transpose(module.transpose(matrix))
    assert transposed_twice == matrix

# Test: Element mapping is correct
@given(matrix=fixed_3x3_matrix_strategy())
def test_transpose_element_mapping(matrix):
    transposed = module.transpose(matrix)
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            assert transposed[j][i] == value

# Test: Transpose of a square matrix maintains symmetry
@given(matrix=fixed_3x3_matrix_strategy())
def test_transpose_square_matrix(matrix):
    transposed = module.transpose(matrix)
    if len(matrix) == len(matrix[0]):
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                assert matrix[i][j] == transposed[j][i]

# Test: Handle matrix with duplicate values
@given(matrix=fixed_3x3_matrix_strategy().map(lambda mat: [[1 for _ in row] for row in mat]))
def test_transpose_duplicate_values(matrix):
    transposed = module.transpose(matrix)
    for row in transposed:
        assert all(value == 1 for value in row)

# Test: Handle matrix with negative values
@given(matrix=lists(
    lists(integers(min_value=-1000, max_value=1000), min_size=3, max_size=3),
    min_size=3, max_size=3
))
def test_transpose_negative_values(matrix):
    transposed = module.transpose(matrix)
    for i, row in enumerate(matrix):
        for j, value in enumerate(row):
            assert transposed[j][i] == value

# Test: Large matrices
@given(matrix=lists(
    lists(integers(), min_size=20, max_size=20),
    min_size=20, max_size=20
))
def test_transpose_large_matrix(matrix):
    transposed = module.transpose(matrix)
    assert len(transposed) == len(matrix[0])
    assert all(len(row) == len(matrix) for row in transposed)

# Test: Non-uniform matrices should raise exceptions
@given(matrix=lists(
    lists(integers(), min_size=1, max_size=10),
    min_size=1, max_size=10
).filter(lambda mat: any(len(row) != len(mat[0]) for row in mat)))
def test_transpose_non_uniform_matrix(matrix):
    with pytest.raises(ValueError):
        module.transpose(matrix)

# Test: Matrix with mixed data types should raise exceptions
@given(matrix=lists(
    lists(one_of(integers(), st.text()), min_size=3, max_size=3),
    min_size=3, max_size=3
))
def test_transpose_mixed_data_types(matrix):
    with pytest.raises(TypeError):
        module.transpose(matrix)

# Test: Ensure transpose does not modify original matrix
@given(matrix=fixed_3x3_matrix_strategy())
def test_transpose_no_side_effects(matrix):
    original = [row[:] for row in matrix] 
    module.transpose(matrix)
    assert matrix == original


# Test: Handles empty and irregular matrices
@given(matrix=irregular_matrix_strategy())
def test_transpose_edge_cases(matrix):
    try:
        transposed = module.transpose(matrix)
        if not matrix:
            assert transposed == []
        if matrix and all(len(row) == len(matrix[0]) for row in matrix):
            assert len(transposed) == len(matrix[0])
            assert all(len(row) == len(matrix) for row in transposed)
    except Exception as e:
        assert False, f"Function raised an exception: {e}"

# Test: Handle empty matrix
@given(matrix=st.just([]))
def test_transpose_empty_matrix(matrix):
    transposed = module.transpose(matrix)
    assert transposed == []

# Test: Handle single row matrix
@given(matrix=st.just([[1, 2, 3]]))
def test_transpose_single_row(matrix):
    transposed = module.transpose(matrix)
    assert transposed == [[1], [2], [3]]

# Test: Handle single column matrix
@given(matrix=st.just([[1], [2], [3]]))
def test_transpose_single_column(matrix):
    transposed = module.transpose(matrix)
    assert transposed == [[1, 2, 3]]


if __name__ == "__main__":
    pytest.main([__file__])

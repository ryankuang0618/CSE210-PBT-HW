import importlib.util

# Path to the .pyc file
pyc_path = "../__encoded_files__/q1.encoded.pyc"


# Load the .pyc file
spec = importlib.util.spec_from_file_location("", pyc_path)
print(spec)
module = importlib.util.module_from_spec(spec)

# Execute the module
spec.loader.exec_module(module)

# Prepare a sample matrix to run the function
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
result = module.transpose(matrix)
print(result)

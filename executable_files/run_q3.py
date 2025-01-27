import importlib.util

# Path to the .pyc file
pyc_path = "../__encoded_files__/q3.encoded.pyc"


# Load the .pyc file
spec = importlib.util.spec_from_file_location("", pyc_path)
module = importlib.util.module_from_spec(spec)

# Execute the module
spec.loader.exec_module(module)

result = module.binary_search([1, 2, 3, 4, 5, 6, 7, 8, 9], 9)
print(result)

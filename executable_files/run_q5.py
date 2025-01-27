import importlib.util

# Path to the .pyc file
pyc_path = "../__encoded_files__/q5.encoded.pyc"


# Load the .pyc file
spec = importlib.util.spec_from_file_location("", pyc_path)
module = importlib.util.module_from_spec(spec)

# Execute the module
spec.loader.exec_module(module)

arr = [38, 27, 43, 3, 9, 82]
module.merge_sort(arr)
print("Sorted array:", arr)
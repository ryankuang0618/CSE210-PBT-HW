import importlib.util

# Path to the .pyc file
pyc_path = "../__encoded_files__/q2.encoded.pyc"


# Load the .pyc file
spec = importlib.util.spec_from_file_location("", pyc_path)
module = importlib.util.module_from_spec(spec)

# Execute the module
spec.loader.exec_module(module)

result = module.parse_date("12/31/2021")
print(result)

import importlib.util

# Path to the .pyc file
pyc_path = "../__encoded_files__/q4.encoded.pyc"


# Load the .pyc file
spec = importlib.util.spec_from_file_location("", pyc_path)
module = importlib.util.module_from_spec(spec)

# Execute the module
spec.loader.exec_module(module)

# Define the function to be cached, you cab use any function here
def expensive_function(x, y):
    print(f"Computing {x} + {y}")  # To demonstrate when the actual computation occurs
    return x + y

# Apply the lru_cache decorator
cached_function = module.lru_cache(expensive_function, cacheLimit = 2)

# Call the cached function
print(cached_function(1, 2))

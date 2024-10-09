import PathLADPlus
from python.utils import *

# Call the C function through Cython and get the temp file location
temp_file = PathLADPlus.py_run_solver("pattern.txt", "target.txt", 60, 1, 10, 0, 1)

# Print the path of the temporary file containing the output
print(f"Output saved to: {temp_file}")

# Read and print the content of the temp file
res = parse_result(temp_file)
print(res)

print("twice:")
temp_file = PathLADPlus.py_run_solver("pattern.txt", "target.txt", 60, 1, 10, 0, 1)

print(f"Output saved to: {temp_file}")
res = parse_result(temp_file)
print(res)
import os
import PathLADPlus

# Get absolute paths for the input files
pattern_file = os.path.abspath("pattern.txt")
target_file = os.path.abspath("target.txt")

# Arguments similar to what you'd pass in the command line
args = ["-p", pattern_file, "-t", target_file, "-f", "-s", "3600"]

# Call the C function through Cython
result = PathLADPlus.py_run_solver(args)
print("Result:", result)

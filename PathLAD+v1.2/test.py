import PathLADPlus

# Arguments similar to what you'd pass in the command line
args = ["-p", "pattern.txt", "-t", "target.txt", "-f", "-s", "3600", "-v"]

# Call the C function through Cython and get the temp file location
temp_file = PathLADPlus.py_run_solver(args)

# Print the path of the temporary file containing the output
print(f"Output saved to: {temp_file}")

# Read and print the content of the temp file
with open(temp_file, 'r') as f:
    print(f.read())

import PathLADPlus

# Arguments similar to what you'd pass in the command line
args = ["-p", "pattern.txt", "-t", "target.txt", "-f", "-s", "3600", "-v"]

# Call the C function through Cython and get the temp file location
temp_file = PathLADPlus.py_run_solver(args)

def parse_soultion(solution_line):
    solution_part = solution_line.split(":")[1].strip()
        
    # Now split by spaces to separate the equations
    equations = solution_part.split(" ")
    
    # Parse left and right parts of each equation
    left_list = []
    right_list = []
    
    for eq in equations:
        left, right = eq.split("=")
        left_list.append(int(left))
        right_list.append(int(right))
    
    return left_list, right_list

def parse_result(file_name):
    # Extract the line that starts with "Solution"
    with open(file_name, 'r') as file:
        file_content = file.read()
    solution_lines = []
    for line in file_content.splitlines():
        if line.startswith("Solution"):
            solution_lines.append(line)
    
    res = {
        "embeddings":[]
    }
    for line in solution_lines:
        # Split the solution part after the colon
        res["embeddings"].append(parse_soultion(line))
    return res

# Print the path of the temporary file containing the output
print(f"Output saved to: {temp_file}")

# Read and print the content of the temp file
res = parse_result(temp_file)
print(res)

# print("twice:")
# temp_file = PathLADPlus.py_run_solver(args)
# print(f"Output saved to: {temp_file}")
# res = parse_result(temp_file)
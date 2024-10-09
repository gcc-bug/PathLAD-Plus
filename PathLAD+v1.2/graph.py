from utils import *
from PathLADPlus import py_run_solver
import tempfile

# Replace '*.txt' with your actual file path
file_path = 'bench/qv_36.txt'
n = 7
m = 7
r = 2

induced = False
time = 60
only_first = False
soultion_number = 100

# Create a temporary directory
with tempfile.TemporaryDirectory() as pattern_dirs:
    os.makedirs(pattern_dirs, exist_ok=True)

    # Assume `read_file_and_create_graph` returns a list of graphs
    graphs = read_file_and_create_graph(file_path)
    
    # Create temporary files for each graph
    for i, graph in enumerate(graphs):
        temp_graph_path = os.path.join(pattern_dirs, f"graph_{i}.txt")
        export_graph(graph, temp_graph_path)  # Export each graph to a temporary file

    # Generate grid graph and store it in a temporary file
    grid_graph = generate_grid_with_Rb(n, m, r)
    with tempfile.NamedTemporaryFile(delete=False, suffix=f"_target_{n}_{m}.txt") as target_file:
        target_path = target_file.name
        export_graph(grid_graph, target_path)

    res = []

    # Iterate over temporary directory files and process each graph file
    for file in os.listdir(pattern_dirs):
        if file.endswith(".txt"):
            pattern_path = os.path.join(pattern_dirs, file)
            print(pattern_path)
            res_file = py_run_solver(pattern_path, target_path, time, only_first, soultion_number, induced, 1)
            res.append(parse_result(res_file))

    # Print the results
    print(res)
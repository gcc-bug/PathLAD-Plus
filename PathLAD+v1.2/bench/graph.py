import rustworkx as rx
import math

import subprocess
import os
import re

def parse_run_data(line):
    # Define a regular expression to capture the required values
    pattern = r"(\d+) solutions; (\d+) fail nodes; (\d+) nodes; ([\d.]+) seconds"
    
    # Use regular expression to search the line
    match = re.search(pattern, line)
    
    if match:
        # Extract and map the matched groups to a dictionary
        result = {
            "solutions": int(match.group(1)),
            "fail_nodes": int(match.group(2)),
            "nodes": int(match.group(3)),
            "time_seconds": float(match.group(4))
        }
        return result
    else:
        raise ValueError("The provided line does not match the expected format.")
    
def run_solver(args):
    command = ['../main'] + args  # Construct the full command
    result = subprocess.run(command, capture_output=True, text=True, cwd=os.getcwd())  # Ensure it runs in the current working directory
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    return result.stdout

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

def parse_result(stdout):
    # Extract the line that starts with "Solution"
    # with open(file_name, 'r') as file:
    #     file_content = file.read()
    solution_lines = []
    res = {
        "embeddings":[]
    }
    for line in stdout.splitlines():
        if line.startswith("Solution"):
            solution_lines.append(line)
        if line.startswith("Run completed"):
            data = parse_run_data(line)
            res.update(data)
            
    
    for line in solution_lines:
        # Split the solution part after the colon
        res["embeddings"].append(parse_soultion(line))
    return res

# Define a function to export the graph in the desired format
def export_graph(graph, file_name):
  with open(file_name, 'w') as file:
    # Write the number of nodes
    file.write(f"{graph.num_nodes()}\n")
    
    # Write each node's successors
    for node in range(graph.num_nodes()):
        successors = graph.neighbors(node)
        file.write(f"{len(successors)} {' '.join(map(str, successors))}\n")


def read_file_and_create_graph(file_path):
    graphs = []

    # Read the file line by line
    with open(file_path, 'r') as file:
        for line in file:
            # Remove any unwanted characters and parse the line into a list of edges
            edge_list = eval(line.strip())
            # Create a new undirected graph
            graph = rx.PyGraph()
            # Mapping to ensure nodes are added once
            node_index_map = {}

            # Add edges with nodes dynamically
            for edge in edge_list:
                for node in edge:
                    if node not in node_index_map:
                        node_index_map[node] = graph.add_node(node)

                # Now add the edge using the node indices from the mapping
                graph.add_edge(node_index_map[edge[0]], node_index_map[edge[1]], None)

            # Append the created graph to the list of graphs
            graphs.append(graph)
    return graphs

def euclidean_distance(node1, node2):
    """Calculate the Euclidean distance between two nodes."""
    return math.sqrt((node1[0] - node2[0]) ** 2 + (node1[1] - node2[1]) ** 2)

def generate_grid_with_Rb(n, m, Rb):
    """Generate an n*m grid graph with edges added between nodes within distance Rb."""
    # Create an empty graph
    G = rx.PyDiGraph()

    # Add nodes in a grid pattern
    nodes = [(i, j) for i in range(n) for j in range(m)]
    node_indices = {node: G.add_node(node) for node in nodes}

    # Add grid edges
    for i in range(n):
        for j in range(m):
            if i < n - 1:
                G.add_edge(node_indices[(i, j)], node_indices[(i + 1, j)], None)
            if j < m - 1:
                G.add_edge(node_indices[(i, j)], node_indices[(i, j + 1)], None)

    # Add additional edges for nodes within distance Rb
    for node1 in nodes:
        for node2 in nodes:
            if node1 != node2:
                distance = euclidean_distance(node1, node2)
                if distance <= Rb:
                    G.add_edge(node_indices[node1], node_indices[node2], None)
                    G.add_edge(node_indices[node2], node_indices[node1], None)

    return G

# Replace '*.txt' with your actual file path
file_path = 'cz_2q_twolocalrandom_37.txt'
pattern_folder = "pattern"
n = 8
m = 8
r = 2
only_first = False
induced = False
find_n = 10
out_time = 10
target_file = f"target_{n}_{m}.txt"

os.makedirs(pattern_folder,exist_ok=True)
graphs = read_file_and_create_graph(file_path)

for i,graph in enumerate(graphs):
    export_graph(graph,os.path.join(pattern_folder,f"graph_{i}.txt"))

grid_graph = generate_grid_with_Rb(n,m,r)
export_graph(grid_graph,target_file)

args = ["-v", "-t", target_file]
if find_n and not only_first:
    args.append("-n")
    args.append(str(find_n))
elif only_first:
    args.append("-f")
if induced:
    args.append("-i")
if out_time:
    args.append("-s")
    args.append(str(out_time))
for file in os.listdir(pattern_folder):
    if "graph" in file:
        pattern_file = os.path.join(pattern_folder,file)
        args.append("-p")
        args.append(pattern_file)
        res = parse_result(run_solver(args))
        if res.get("solutions"):
            print(f"{pattern_file} using {res["time_seconds"]} secs")
    
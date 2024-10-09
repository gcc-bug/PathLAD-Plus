import rustworkx as rx
import math
import os
from PathLADPlus import py_run_solver

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
        # print(line)
        if line.startswith("Solution"):
            solution_lines.append(line)
    
    res = {
        "embeddings":[]
    }
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
file_path = 'bench/qv_36.txt'
pattern_dirs = "pattern"
n = 7
m = 7
r = 2

induced = False
time = 60
only_first = True
soultion_number = 100

os.makedirs(pattern_dirs,exist_ok= True)
graphs = read_file_and_create_graph(file_path)
for i,graph in enumerate(graphs):
    export_graph(graph,os.path.join(pattern_dirs,f"graph_{i}.txt"))
    
grid_graph = generate_grid_with_Rb(n,m,r)
target_path = f"target_{n}_{m}.txt"
export_graph(grid_graph,target_path)

res = []
for file in os.listdir(pattern_dirs):
    if file.endswith(".txt"):
        pattern_path = os.path.join(pattern_dirs,file)
        res_file=py_run_solver(pattern_path, target_path, time, only_first, soultion_number, induced, 1)
        res.append(parse_result(res_file))
    else:
        continue
print(res)
    
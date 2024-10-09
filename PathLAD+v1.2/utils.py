import rustworkx as rx
import math
import os
import re

def parse_solution(solution_line):
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
    # Open the result file and read the contents
    with open(file_name, 'r') as file:
        file_content = file.read()

    # Initialize the result dictionary with default structure
    res = {
        "solutions": [],
        "stats": {
            "total_solutions": 0,
            "fail_nodes": 0,
            "total_nodes": 0,
            "time_seconds": 0.0
        }
    }

    # Extract solution lines and statistics from the file
    solution_lines = []
    for line in file_content.splitlines():
        if line.startswith("Solution"):
            solution_lines.append(line)
        elif line.startswith("Run completed"):
            # Extract stats like number of solutions, fail nodes, total nodes, and time
            match = re.search(r'Run completed: (\d+) solutions; (\d+) fail nodes; (\d+) nodes; ([\d\.]+) seconds', line)
            if match:
                res["stats"]["total_solutions"] = int(match.group(1))
                res["stats"]["fail_nodes"] = int(match.group(2))
                res["stats"]["total_nodes"] = int(match.group(3))
                res["stats"]["time_seconds"] = float(match.group(4))

    # Parse each solution line and add it to the result
    for line in solution_lines:
        res["solutions"].append(parse_solution(line))

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
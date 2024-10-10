import PathLADPlus
import numpy as np

def create_graph_python(nb_vertices, edges):
    """
    Create a undirectedgraph using the Tgraph struct in Python.
    :param nb_vertices: Number of vertices in the graph
    :param edges: List of tuples representing edges (i, j)
    :return: Tgraph object
    """
    # Temporary data structures to collect the information
    isLoop = [False for _ in range(nb_vertices)]
    nbAdj = [0 for _ in range(nb_vertices)]
    nbSucc = [0 for _ in range(nb_vertices)]
    nbPred = [0 for _ in range(nb_vertices)]
    adj = [[] for _ in range(nb_vertices)]
    edgeDirection = [['0'] * nb_vertices for _ in range(nb_vertices)]  # Initialize as char '0'


    # Populate the temporary data structures
    for i, j in edges:
        if i == j:
            isLoop[i] = True
        else:
            nbAdj[i] += 1
            nbAdj[j] += 1
            adj[i].append(j)
            adj[j].append(i)
            edgeDirection[i][j] = '3'

    maxDegree = max(nbAdj)

    # Now create the graph using the initialize_graph method
    graph = PathLADPlus.Tgraph()
    
    # Initialize the graph using all collected data
    graph.initialize_graph(
        nb_vertices, 
        isLoop, 
        nbAdj, 
        nbSucc, 
        nbPred, 
        adj, 
        edgeDirection,  # Ensure it's list of lists of strings (chars)
        maxDegree
    )

    return graph

# Example usage:
edges = [(0, 1), (1, 2), (2, 0)]  # Edges in the graph
graph = create_graph_python(3, edges)

# Access graph properties
print(f"Is Directed: {graph.isDirected}")
print(f"Number of Vertices: {graph.nbVertices}")
print(f"Number of Adj: {graph.nbAdj}")
print(f"Adjacency List: {graph.adj}")
print(f"Max Degree: {graph.maxDegree}")

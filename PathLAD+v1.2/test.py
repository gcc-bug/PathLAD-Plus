import PathLADPlus
import numpy as np

def create_graph_python(nb_vertices, edges):
    """
    Create a graph using the Tgraph struct in Python.
    :param nb_vertices: Number of vertices in the graph
    :param edges: List of tuples representing edges (i, j)
    :return: Tgraph object
    """
    # Temporary data structures to collect the information
    isLoop = np.zeros(nb_vertices, dtype=bool)
    nbAdj = np.zeros(nb_vertices, dtype=int)
    nbSucc = np.zeros(nb_vertices, dtype=int)
    nbPred = np.zeros(nb_vertices, dtype=int)
    adj = [[] for _ in range(nb_vertices)]
    edgeDirection = [['0'] * nb_vertices for _ in range(nb_vertices)]  # Initialize as char '0'

    maxDegree = 0
    isDirected = True

    # Populate the temporary data structures
    for i, j in edges:
        if i == j:
            isLoop[i] = True
        else:
            nbSucc[i] += 1
            nbAdj[i] += 1
            nbAdj[j] += 1
            adj[i].append(j)
            adj[j].append(i)
            edgeDirection[i][j] = '1'
            edgeDirection[j][i] = '2'

            # Update max degree
            maxDegree = max(maxDegree, nbSucc[i])

    # Now create the graph using the initialize_graph method
    graph = PathLADPlus.Tgraph()
    
    # Initialize the graph using all collected data
    graph.initialize_graph(
        nb_vertices, 
        isLoop.tolist(), 
        nbAdj.tolist(), 
        nbSucc.tolist(), 
        nbPred.tolist(), 
        adj, 
        edgeDirection,  # Ensure it's list of lists of strings (chars)
        maxDegree,
        isDirected
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

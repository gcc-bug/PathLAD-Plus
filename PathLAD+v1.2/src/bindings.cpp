#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include "global.h"

namespace py = pybind11;


PYBIND11_MODULE(PathLADPlus, m) {
    py::class_<Tgraph>(m, "Tgraph")
        .def(py::init<>())  // Default constructor
        .def_readwrite("isDirected", &Tgraph::isDirected)  // Allow setting isDirected
        .def_readwrite("nbVertices", &Tgraph::nbVertices)  // Allow setting nbVertices

        // Helper function to initialize the arrays
        .def("initialize_graph", [](Tgraph &g, int nbVertices, const std::vector<bool>& isLoop,
                                    const std::vector<int>& nbAdj, const std::vector<int>& nbSucc, 
                                    const std::vector<int>& nbPred, const std::vector<std::vector<int>>& adj, 
                                    const std::vector<std::vector<char>>& edgeDirection, int maxDegree) {
            // Set the number of vertices
            g.nbVertices = nbVertices;

            // Allocate memory for the arrays
            g.isLoop = (bool*)calloc(nbVertices, sizeof(bool));
            g.nbAdj = (int*)calloc(nbVertices, sizeof(int));
            g.nbSucc = (int*)calloc(nbVertices, sizeof(int));
            g.nbPred = (int*)calloc(nbVertices, sizeof(int));
            g.adj = (int**)calloc(nbVertices, sizeof(int*));
            g.edgeDirection = (char**)calloc(nbVertices, sizeof(char*));
            g.edgeLabel = (int**)calloc(nbVertices, sizeof(int*));
            g.vertexLabel = (int*)calloc(nbVertices, sizeof(int));

            for (int i = 0; i < nbVertices; ++i) {
                g.adj[i] = (int*)calloc(nbAdj[i], sizeof(int));
                g.edgeDirection[i] = (char*)calloc(nbVertices, sizeof(char));
                g.edgeLabel[i] = (int*)calloc(nbVertices, sizeof(int));
            }

            // Populate the fields
            for (int i = 0; i < nbVertices; ++i) {
                g.isLoop[i] = isLoop[i];
                g.nbAdj[i] = nbAdj[i];
                g.nbSucc[i] = nbSucc[i];
                g.nbPred[i] = nbPred[i];
                for (size_t j = 0; j < adj[i].size(); ++j) {
                    g.adj[i][j] = adj[i][j];
                }
                for (size_t j = 0; j < edgeDirection[i].size(); ++j) {
                    g.edgeDirection[i][j] = edgeDirection[i][j];
                }
            }

            // Set the maximum degree
            g.maxDegree = maxDegree;

            // Check if the graph is directed
            g.isDirected = false;
            for (int i = 0; i < nbVertices; ++i) {
                for (int j : adj[i]) {
                    if (g.edgeDirection[i][j] == '1' || g.edgeDirection[i][j] == '2') {
                        g.isDirected = true;
                        return;
                    }
                }
            }
        })
        .def_property("isLoop", 
            [](Tgraph &g) { return std::vector<bool>(g.isLoop, g.isLoop + g.nbVertices); },
            [](Tgraph &g, const std::vector<bool> &loops) {
                for (size_t i = 0; i < loops.size(); ++i) {
                    g.isLoop[i] = loops[i];
                }
            })
        .def_property("nbAdj", 
            [](Tgraph &g) { return std::vector<int>(g.nbAdj, g.nbAdj + g.nbVertices); },
            [](Tgraph &g, const std::vector<int> &adj) {
                for (size_t i = 0; i < adj.size(); ++i) {
                    g.nbAdj[i] = adj[i];
                }
            })
        .def_property("nbPred", 
            [](Tgraph &g) { return std::vector<int>(g.nbPred, g.nbPred + g.nbVertices); },
            [](Tgraph &g, const std::vector<int> &pred) {
                for (size_t i = 0; i < pred.size(); ++i) {
                    g.nbPred[i] = pred[i];
                }
            })
        .def_property("nbSucc", 
            [](Tgraph &g) { return std::vector<int>(g.nbSucc, g.nbSucc + g.nbVertices); },
            [](Tgraph &g, const std::vector<int> &succ) {
                for (size_t i = 0; i < succ.size(); ++i) {
                    g.nbSucc[i] = succ[i];
                }
            })
        .def_property("adj", 
            [](Tgraph &g) {
                std::vector<std::vector<int>> adj_list(g.nbVertices);
                for (int i = 0; i < g.nbVertices; ++i) {
                    adj_list[i] = std::vector<int>(g.adj[i], g.adj[i] + g.nbAdj[i]);
                }
                return adj_list;
            }, 
            [](Tgraph &g, const std::vector<std::vector<int>> &adj_list) {
                for (int i = 0; i < g.nbVertices; ++i) {
                    for (size_t j = 0; j < adj_list[i].size(); ++j) {
                        g.adj[i][j] = adj_list[i][j];
                    }
                }
            })
        .def_property("edgeDirection", 
            [](Tgraph &g) {
                std::vector<std::vector<char>> directions(g.nbVertices);
                for (int i = 0; i < g.nbVertices; ++i) {
                    directions[i] = std::vector<char>(g.edgeDirection[i], g.edgeDirection[i] + g.nbVertices);
                }
                return directions;
            }, 
            [](Tgraph &g, const std::vector<std::vector<char>> &directions) {
                for (int i = 0; i < g.nbVertices; ++i) {
                    for (int j = 0; j < g.nbVertices; ++j) {
                        g.edgeDirection[i][j] = directions[i][j];
                    }
                }
            })
        .def_property("vertexLabel", 
            [](Tgraph &g) { return std::vector<int>(g.vertexLabel, g.vertexLabel + g.nbVertices); },
            [](Tgraph &g, const std::vector<int> &labels) {
                for (size_t i = 0; i < labels.size(); ++i) {
                    g.vertexLabel[i] = labels[i];
                }
            })
        .def_readwrite("maxDegree", &Tgraph::maxDegree);  // Allow setting maxDegree
}

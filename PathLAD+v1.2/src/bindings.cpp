#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>
#include "global.h" // Your C header file with Tgraph

namespace py = pybind11;

PYBIND11_MODULE(graphmodule, m) {
    py::class_<Tgraph>(m, "Tgraph")
        .def(py::init<>())  // Default constructor
        .def_readwrite("isDirected", &Tgraph::isDirected)
        .def_property("isLoop", 
             [](Tgraph &g) { return py::array_t<bool>(g.nbVertices, g.isLoop); }, 
             [](Tgraph &g, py::array_t<bool> arr) {
                 py::buffer_info info = arr.request();
                 if (info.size != g.nbVertices)
                     throw std::runtime_error("Size mismatch");
                 std::memcpy(g.isLoop, info.ptr, sizeof(bool) * info.size);
             })
        .def_readwrite("nbVertices", &Tgraph::nbVertices)
        .def_property("nbAdj", 
             [](Tgraph &g) { return py::array_t<int>(g.nbVertices, g.nbAdj); }, 
             [](Tgraph &g, py::array_t<int> arr) {
                 py::buffer_info info = arr.request();
                 if (info.size != g.nbVertices)
                     throw std::runtime_error("Size mismatch");
                 std::memcpy(g.nbAdj, info.ptr, sizeof(int) * info.size);
             })
        .def_property("nbPred", 
             [](Tgraph &g) { return py::array_t<int>(g.nbVertices, g.nbPred); }, 
             [](Tgraph &g, py::array_t<int> arr) {
                 py::buffer_info info = arr.request();
                 if (info.size != g.nbVertices)
                     throw std::runtime_error("Size mismatch");
                 std::memcpy(g.nbPred, info.ptr, sizeof(int) * info.size);
             })
        .def_property("nbSucc", 
             [](Tgraph &g) { return py::array_t<int>(g.nbVertices, g.nbSucc); }, 
             [](Tgraph &g, py::array_t<int> arr) {
                 py::buffer_info info = arr.request();
                 if (info.size != g.nbVertices)
                     throw std::runtime_error("Size mismatch");
                 std::memcpy(g.nbSucc, info.ptr, sizeof(int) * info.size);
             })
        .def_property("adj", 
             [](Tgraph &g) {
                 std::vector<std::vector<int>> adj_vec(g.nbVertices);
                 for (int i = 0; i < g.nbVertices; ++i) {
                     adj_vec[i] = std::vector<int>(g.nbAdj[i]);
                     for (int j = 0; j < g.nbAdj[i]; ++j) {
                         adj_vec[i][j] = g.adj[i][j];
                     }
                 }
                 return adj_vec;
             }, 
             [](Tgraph &g, std::vector<std::vector<int>> adj_vec) {
                 for (int i = 0; i < g.nbVertices; ++i) {
                     for (int j = 0; j < g.nbAdj[i]; ++j) {
                         g.adj[i][j] = adj_vec[i][j];
                     }
                 }
             })
        // Repeat similar approach for edgeDirection, edgeLabel, vertexLabel, etc.
        .def_readwrite("maxDegree", &Tgraph::maxDegree);
}

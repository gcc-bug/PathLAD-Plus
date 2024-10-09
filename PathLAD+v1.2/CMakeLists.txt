cmake_minimum_required(VERSION 3.10)
project(PathLAD-Plus VERSION 1.2.1 LANGUAGES C CXX)

# Set the C standard to C99
set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)

# Set the source directory
set(SRC_DIR ${CMAKE_SOURCE_DIR}/src)
set(INCLUDE_DIR ${CMAKE_SOURCE_DIR}/include)

# Include the headers
include_directories(${INCLUDE_DIR})

# Add all source files
set(SOURCES
    ${SRC_DIR}/allDiff.c
    ${SRC_DIR}/allDiff_large.c
    ${SRC_DIR}/domainsPath.c
    ${SRC_DIR}/domainsPath_large.c
    ${SRC_DIR}/graph.c
    ${SRC_DIR}/graph_large.c
    ${SRC_DIR}/lad.c
    ${SRC_DIR}/lad_large.c
    ${SRC_DIR}/main.c
    ${SRC_DIR}/solve_large.c
    ${SRC_DIR}/compatibility.c
)

message(STATUS "PathLAD-Plus Version: ${PathLAD-Plus_VERSION}")

# Find pybind11 package
find_package(pybind11 REQUIRED)
pybind11_add_module(PathLADPlus ${SRC_DIR}/bindings.cpp)
# Link the pybind11 module
set_target_properties(PathLADPlus PROPERTIES LINKER_LANGUAGE CXX)

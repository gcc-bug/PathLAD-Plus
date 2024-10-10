add_executable(test_graph test_graph.c)
target_link_libraries(test_graph pathladplus_lib)

add_executable(test_main test_main.c)
target_link_libraries(test_main pathladplus_lib)
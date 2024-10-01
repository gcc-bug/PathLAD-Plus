from libc.stdlib cimport malloc, free
from libc.string cimport strcpy
from libc.stdio cimport FILE, fopen, freopen, stdout, fclose, fflush  # Importing fopen correctly
import os
import tempfile

# Declare the function from the C code
cdef extern from "main.h":
    int run_solver(int argc, char* argv[])

# Python wrapper for the C function
def py_run_solver(list args):
    # Prepare arguments
    cdef int argc = len(args) + 1  # Include the dummy argv[0]
    cdef char** argv = <char**>malloc((argc + 1) * sizeof(char*))

    if argv == NULL:
        raise MemoryError("Unable to allocate memory for argv")

    # Use a dummy program name as argv[0]
    program_name = b"program_name"
    argv[0] = <char*>malloc((len(program_name) + 1) * sizeof(char))
    strcpy(argv[0], program_name)

    # Copy the arguments passed from Python to argv[1], argv[2], etc.
    for i in range(len(args)):
        arg_as_bytes = args[i].encode('utf-8')  # Convert Python string to bytes
        argv[i + 1] = <char*>malloc((len(arg_as_bytes) + 1) * sizeof(char))  # Allocate memory for each argument
        if argv[i + 1] == NULL:
            raise MemoryError("Unable to allocate memory for argv[i+1]")
        strcpy(argv[i + 1], arg_as_bytes)  # Copy the bytes into the allocated memory

    argv[argc] = NULL  # Last argument must be NULL

    # Create a temporary file to save the output
    temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w+', encoding='utf-8')
    temp_filename = temp_file.name

    # Redirect stdout to the temporary file
    c_temp_file = fopen(temp_filename.encode('utf-8'), "w")
    if c_temp_file == NULL:
        raise RuntimeError("Unable to open temporary file for writing")

    # Backup the original stdout and redirect stdout to the temp file
    stdout_backup = stdout
    freopen(temp_filename.encode('utf-8'), "w", stdout)

    # Call the C function
    result = run_solver(argc, argv)

    # Flush and restore stdout
    fflush(stdout)
    freopen("/dev/tty", "w", stdout)  # Restore original stdout (for Unix-like systems)

    # Close the C file handle
    fclose(c_temp_file)

    # Free allocated memory
    for i in range(argc):
        free(argv[i])
    free(argv)

    # Return the path to the temporary file containing the log
    return temp_filename

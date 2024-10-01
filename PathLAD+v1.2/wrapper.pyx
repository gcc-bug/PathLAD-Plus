from libc.stdlib cimport malloc, free
from libc.string cimport strcpy
from libc.stdio cimport puts, fputs, stdout  # To print debug messages in C

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

    # Use the actual Python script name as argv[0]
    program_name = b"program_name"  # You can replace this with any string or use os.path.basename(__file__)
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

    # Debug print to verify the arguments passed to the C program
    # fputs(b"Arguments passed to C program:\n", stdout)
    # for i in range(argc):
    #    fputs(b"argv[", stdout)
    #    fputs(str(i).encode('utf-8'), stdout)
    #    fputs(b"]: ", stdout)
    #    fputs(argv[i], stdout)
    #    fputs(b"\n", stdout)

    # Call the C function
    result = run_solver(argc, argv)

    # Free allocated memory
    for i in range(argc):
        free(argv[i])
    free(argv)

    return result

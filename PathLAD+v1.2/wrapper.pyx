from libc.stdlib cimport malloc, free
from libc.string cimport strcpy
from libc.stdio cimport FILE, fopen, freopen, stdout, fclose, fflush  # Importing fopen correctly
import os
import tempfile

# Declare the updated C function with bint for boolean parameters
cdef extern from "main.h":
    int run_solver(int timeLimit, bint firstSol, int number_Sol, bint induced, int verbose, const char* fileNameGp, const char* fileNameGt)

# Python wrapper for the updated C function
def py_run_solver(str fileNameGp, str fileNameGt, int timeLimit=60, bint firstSol=False, int number_Sol=1, bint induced=False, int verbose=0):
    # Convert Python strings to C strings for fileNameGp and fileNameGt
    cdef char* c_fileNameGp
    cdef char* c_fileNameGt

    # Allocate memory for fileNameGp and fileNameGt
    if fileNameGp:
        c_fileNameGp = <char*>malloc((len(fileNameGp) + 1) * sizeof(char))
        strcpy(c_fileNameGp, fileNameGp.encode('utf-8'))
    else:
        c_fileNameGp = <char*>""  # Pass an empty string

    if fileNameGt:
        c_fileNameGt = <char*>malloc((len(fileNameGt) + 1) * sizeof(char))
        strcpy(c_fileNameGt, fileNameGt.encode('utf-8'))
    else:
        c_fileNameGt = <char*>""  # Pass an empty string

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

    # Call the C function with the modified arguments
    result = run_solver(timeLimit, firstSol, number_Sol, induced, verbose, c_fileNameGp, c_fileNameGt)

    # Flush and restore stdout
    fflush(stdout)
    freopen("/dev/tty", "w", stdout)  # Restore original stdout (for Unix-like systems)

    # Close the C file handle
    fclose(c_temp_file)

    # Free allocated memory for fileNameGp and fileNameGt
    if fileNameGp:
        free(c_fileNameGp)
    if fileNameGt:
        free(c_fileNameGt)

    # Return the path to the temporary file containing the log
    return temp_filename

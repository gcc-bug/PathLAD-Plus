from setuptools import setup, Extension
from Cython.Build import cythonize

ext = Extension(
    name="PathLADPlus",  # Name of the generated Python module
    sources=["wrapper.pyx",
             "main.c",
             "solve_large.c"],  # C and Cython files
    include_dirs=["."],  # Path to the C header files
    extra_compile_args=['-Wall', '-O0', '-g', '-std=c99'],  # Enable more verbose warnings
    extra_link_args=['-Wall', '-O0', '-g']
)

setup(
    ext_modules=cythonize(ext),
)

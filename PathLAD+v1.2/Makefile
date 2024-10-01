# Variables
PYTHON = python3
CYTHON_BUILD = $(PYTHON) setup.py build_ext --inplace
TEST_SCRIPT = $(PYTHON) test.py

# Default target: Build and run the test
all: build run_test

# Build the Cython extension
build:
	$(CYTHON_BUILD)

# Run the test script
run_test:
	$(TEST_SCRIPT)

# Clean the build artifacts
clean:
	rm -rf build/
	rm -f *.so
	rm -f *.c
	rm -f *.o
	rm -rf __pycache__

# Phony targets
.PHONY: all build run_test clean

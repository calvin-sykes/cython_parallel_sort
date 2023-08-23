# parallel-sort

[![Test build](https://github.com/calvin-sykes/cython_parallel_sort/actions/workflows/python-package.yml/badge.svg)](https://github.com/calvin-sykes/cython_parallel_sort/actions/workflows/python-package.yml) [![PyPI version](https://badge.fury.io/py/parallel-sort.svg)](https://badge.fury.io/py/parallel-sort)

This module provides a simple Cython interface to parallel sorting algorithms available in C++. It provides functions for in-place and out-of-place sorts, as well as indirect sorting (aka. "argsort").

By default it requires a C++17-capable compiler, and will use the standard `std::sort`routine with the parallel execution policy introduced in that standard. For older compilers without C++17 support, the [GNU Parallel Mode](https://gcc.gnu.org/onlinedocs/libstdc++/manual/parallel_mode.html) sorting routines may be used instead.

## Usage

````python
import parallel_sort
import numpy as np

x = np.random.random(size=10000)

x_sorted = parallel_sort.sort(x)

assert np.all(np.diff(x) >= 0) # x is now sorted
````

Note that these routines are "unstable" sorts, meaning that the ordering of equal elements in the original array is not guaranteed to be preserved.

## Installing

Requirements: numpy, C++17-capable g++, Cython (only for installation from source).

On Linux, installing from wheel via `pip` should "just work":

````bash
pip install parallel_sort
````

On Mac, it is important to ensure that gcc is used to compile the module rather than the default Apple-provided clang, which can be done by prefixing the install command with `CC=$(brew --prefix gcc)/bin/gcc-13` (substituting your gcc version as appropriate).

### GNU Parallel Mode option

For older compilers that do not support C++17, the module can use the GNU Parallel Mode library instead. To build without C++17, clone the repository and set `use_cxx17 = False` in `setup.py`. Then run:

````bash
pip install -e .
````

to compile and install the module.

### Note for Apple Silicon Macs

If the module builds OK, but importing it fails with an error "undefined reference to `aarch64_ldadd4_acq_rel`", try rebuilding with the following command

````bash
CFLAGS=-mno-outline-atomics CC=$(brew --prefix gcc)/bin/gcc-13 pip install --no-cache-dir -e .
````

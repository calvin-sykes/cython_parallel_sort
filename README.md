# parallel-sort

[![Test build](https://github.com/calvin-sykes/cython_parallel_sort/actions/workflows/python-package.yml/badge.svg)](https://github.com/calvin-sykes/cython_parallel_sort/actions/workflows/python-package.yml) [![PyPI version](https://badge.fury.io/py/parallel-sort.svg)](https://badge.fury.io/py/parallel-sort)

This module provides a simple Cython interface to parallel sorting algorithms available in C++. It provides functions for in-place and out-of-place sorts, as well as indirect sorting (aka. "argsort").

By default it requires a C++17-capable compiler, and will use the parallel execution policy introduced in that standard. For older compilers without C++17 support, the [GNU Parallel Mode](https://gcc.gnu.org/onlinedocs/libstdc++/manual/parallel_mode.html) sorting routines may be used instead.

## Usage

````python
import parallel_sort
import numpy as np

x = np.random.random(size=10000)

x_sorted = parallel_sort.sort(x)

assert np.all(np.diff(x) >= 0) # x is now sorted
````

## Installing

Requirements: numpy, OpenMP, C++17-capable g++, Cython (only for installation from source).

Installing from wheel via `pip` should "just work":

````bash
pip install parallel_sort
````

Alternatively, the module can be built for older compilers that do not support C++17, but do supply the GNU Parallel Mode library. To build without C++17, clone the repository and set `use_cxx17 = False` in `setup.py`. Then run:

````bash
pip install -e .
````

to compile and install the module.

Installation has been tested on linux (Ubuntu, CentOS) and Mac (via Homebrew).
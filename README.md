# parallel-sort

[![Test build](https://github.com/calvin-sykes/cython_parallel_sort/actions/workflows/python-package.yml/badge.svg)](https://github.com/calvin-sykes/cython_parallel_sort/actions/workflows/python-package.yml) [![PyPI version](https://badge.fury.io/py/parallel-sort.svg)](https://badge.fury.io/py/parallel-sort)

This module provides a simple Cython interface to the [GNU Parallel Mode](https://gcc.gnu.org/onlinedocs/libstdc++/manual/parallel_mode.html) sorting routines, to allow them to be used from Python code.

Functions are included for in-place and out-of-place sorts, as well as indirect sorting (aka. "argsort").

## Usage

````python
import parallel_sort
import numpy as np

x = np.random.random(size=10000)

x_sorted = parallel_sort.parallel_sort(x)

assert np.all(np.diff(x) >= 0) # x is now sorted
````

## Installing

Requirements: numpy, OpenMP.

To install from source Cython is required, in addition to a working installation of the GNU Parallel libraries.
Installing from a wheel via `pip` should "just work":

````bash
pip install parallel_sort
````

Installation has only been tested on linux.
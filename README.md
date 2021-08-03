# parallel_sort

This module provides a simple Cython interface to the [GNU Parallel Mode](https://gcc.gnu.org/onlinedocs/libstdc++/manual/parallel_mode.html) sorting routines, to enable them to be used from Python code.

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

To install, numpy and cython are required, in addition to a working installation of the GNU Parallel libraries.
Installation has only been tested on Linux.

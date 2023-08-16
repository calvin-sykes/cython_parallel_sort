# cython: boundscheck = False
# cython: wraparound = False
# cython: language_level = 3

import numpy as np
cimport cython 

ctypedef fused real:
    cython.char
    cython.uchar
    cython.short
    cython.ushort
    cython.int
    cython.uint
    cython.long
    cython.ulong
    cython.longlong
    cython.ulonglong
    cython.float
    cython.double

cdef extern from "parallel_sort.hpp":
    cdef cppclass IndexCompare[T]:
        IndexCompare() nogil
        IndexCompare(T*) nogil
        operator()(cython.long i1, cython.long i2) nogil

    cdef void __sort[T](T first, T last)
    cdef void __sort[T, Compare](T first, T last, Compare c)

def check_ndarray(func):
    def wrapped(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TypeError as e:
            raise TypeError("Only NumPy arrays of arithmetic types may be sorted") from e
    return wrapped

@check_ndarray
def sort_inplace(real[:] a):
    """In-place parallel sort for numpy types"""
    __sort(&a[0], &a[a.shape[0]])

@check_ndarray
def sort(real[:] a):
    """Parallel sort for numpy types"""
    cdef real[:] a_copy = np.copy(a)
    __sort(&a_copy[0], &a_copy[a_copy.shape[0]])
    return np.array(a_copy)

@check_ndarray
def argsort(real[:] a):
    """Parallel indirect sort for numpy types"""
    cdef long[:] indices = np.arange(a.shape[0], dtype=long)
    cdef IndexCompare[real] compare = IndexCompare[real](&a[0])
    __sort(&indices[0], &indices[indices.shape[0]], compare)
    return np.array(indices)

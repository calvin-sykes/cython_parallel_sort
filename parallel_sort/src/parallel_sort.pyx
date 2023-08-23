# cython: boundscheck = False
# cython: wraparound = False
# cython: language_level = 3

import numpy as np
cimport numpy as cnp
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

cdef extern from "numpy/halffloat.h" nogil:
    ctypedef cnp.uint16_t npy_half
    int npy_half_lt(npy_half h1, npy_half h2)

cdef extern from "parallel_sort.hpp" nogil:
    cdef cppclass IndexCompare[T]:
        IndexCompare()
        IndexCompare(T*)
    cdef cppclass IndexCompareF16:
        IndexCompareF16()
        IndexCompareF16(cnp.uint16_t*)

    cdef void __sort[T](T first, T last)
    cdef void __sort[T, Compare](T first, T last, Compare c)

def check_ndarray(func):
    """
    Input validation decorator for parallel sort functions.
    Checks that parameter is a NumPy array, and dispatches to specialised functions when
    array datatype is half-precision float.
    """
    def wrapped(arry):
        if not isinstance(arry, np.ndarray):
            raise TypeError("Only NumPy arrays of arithmetic types may be sorted")
        if arry.dtype == np.float16:
            uint_arry = arry.view(np.uint16)
            return f16_funcs[func.__name__](uint_arry)
        else:
            return func(arry)
    return wrapped

@check_ndarray
def sort_inplace(real[:] a):
    """In-place parallel sort for numpy types"""
    __sort(&a[0], &a[a.shape[0]])

@check_ndarray
def sort(real[:] a):
    """Parallel sort for numpy types"""
    cdef cnp.ndarray[ndim=1, dtype=real] a_copy = np.copy(a)
    __sort(&a_copy[0], &a_copy[a_copy.shape[0]])
    return a_copy

@check_ndarray
def argsort(real[:] a):
    """Parallel indirect sort for numpy types"""
    cdef cnp.ndarray[ndim=1, dtype=long] indices = np.arange(a.shape[0], dtype=long)
    cdef IndexCompare[real] compare = IndexCompare[real](&a[0])
    __sort(&indices[0], &indices[indices.shape[0]], compare)
    return indices

# "overloads" for fp16

def _sort_inplace_f16(cnp.uint16_t[:] a):
    """In-place parallel sort for half-precision type"""
    __sort(&a[0], &a[a.shape[0]], &npy_half_lt)

def _sort_f16(cnp.uint16_t[:] a):
    """Parallel sort for half-precision type"""
    cdef cnp.ndarray[ndim=1, dtype=cnp.uint16_t] a_copy = np.copy(a)
    __sort(&a_copy[0], &a_copy[a.shape[0]], &npy_half_lt)
    a_copy.dtype = np.float16
    return a_copy

def _argsort_f16(cnp.uint16_t[:] a):
    """Parallel indirect sort for half-precision type"""
    cdef cnp.ndarray[ndim=1, dtype=long] indices = np.arange(a.shape[0], dtype=long)
    cdef IndexCompareF16 compare = IndexCompareF16(&a[0])
    __sort(&indices[0], &indices[indices.shape[0]], compare)
    return indices

f16_funcs = {
    "sort_inplace": _sort_inplace_f16,
    "sort": _sort_f16,
    "argsort": _argsort_f16
}

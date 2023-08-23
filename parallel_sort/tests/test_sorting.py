import numpy as np
import psutil
import pytest

import parallel_sort

np.random.seed(1234567)


def test_version():
    assert parallel_sort.__version__ != "unknown"


def test_parallel_sort_int():
    x = np.random.randint(int(1e6), size=1000)

    numpy_sort = np.sort(x)
    test_sort = parallel_sort.sort(x)

    assert np.all(test_sort == numpy_sort)


def test_parallel_sort_float():
    x = np.random.random(size=1000)

    numpy_sort = np.sort(x)
    test_sort = parallel_sort.sort(x)

    assert np.all(test_sort == numpy_sort)


def test_parallel_sort_float16():
    x = np.random.random(size=1000).astype(np.float16)

    numpy_sort = np.sort(x)
    test_sort = parallel_sort.sort(x)

    assert np.all(test_sort == numpy_sort)


def test_parallel_sort_uint16():
    x = np.random.randint(int(10000), size=1000, dtype=np.uint16)

    numpy_sort = np.sort(x)
    test_sort = parallel_sort.sort(x)

    assert np.all(test_sort == numpy_sort)


def test_parallel_inplace_sort_int():
    x = np.random.randint(int(1e6), size=1000)
    test_x = x.copy()

    x.sort()
    parallel_sort.sort_inplace(test_x)

    assert np.all(test_x == x)


def test_parallel_inplace_sort_float():
    x = np.random.random(size=1000)
    test_x = np.copy(x)

    x.sort()
    parallel_sort.sort_inplace(test_x)

    assert np.all(test_x == x)


def test_parallel_inplace_sort_float16():
    x = np.random.random(size=1000).astype(np.float16)
    test_x = np.copy(x)

    x.sort()
    parallel_sort.sort_inplace(test_x)

    assert np.all(test_x == x)


def test_parallel_inplace_sort_uint16():
    x = np.random.randint(int(10000), size=1000, dtype=np.uint16)
    test_x = x.copy()

    x.sort()
    parallel_sort.sort_inplace(test_x)

    assert np.all(test_x == x)


def test_parallel_argsort_int():
    x = np.random.randint(int(1e6), size=1000)

    numpy_indices = np.argsort(x)
    test_indices = parallel_sort.argsort(x)

    # The parallel sorts may not offer the same stability guarantees as NumPy
    # So the indices might not match in cases where there are repeated array values
    try:
        assert np.all(test_indices == numpy_indices)
    except AssertionError:
        assert np.all(x[test_indices] == x[numpy_indices])


def assert_argsort(x, numpy_indices, test_indices):
    # The parallel sorts do not offer the same stability guarantees as NumPy,
    # so indices may not match if there are repeated array values.
    # But values should still all be equal
    try:
        assert np.all(test_indices == numpy_indices)
    except AssertionError:
        assert np.all(x[test_indices] == x[numpy_indices])


def test_parallel_argsort_float():
    x = np.random.random(size=1000)

    numpy_indices = np.argsort(x)
    test_indices = parallel_sort.argsort(x)

    assert_argsort(x, numpy_indices, test_indices)


def test_parallel_argsort_float16():
    x = np.random.random(size=1000).astype(np.float16)

    numpy_indices = np.argsort(x)
    test_indices = parallel_sort.argsort(x)

    assert_argsort(x, numpy_indices, test_indices)


def test_parallel_argsort_uint16():
    x = np.random.randint(int(10000), size=1000, dtype=np.uint16)

    numpy_indices = np.argsort(x)
    test_indices = parallel_sort.argsort(x)

    assert_argsort(x, numpy_indices, test_indices)


def test_typechecking():
    x = [1, 2, 3, 4]

    with pytest.raises(TypeError):
        parallel_sort.sort(x)

    with pytest.raises(TypeError):
        parallel_sort.sort_inplace(x)

    with pytest.raises(TypeError):
        parallel_sort.argsort(x)


def test_cpu_usage():
    x = np.random.randint(int(1e6), size=int(1e7))

    psutil.cpu_percent(None)
    x.sort()
    cpu_numpy = psutil.cpu_percent(None)
    parallel_sort.sort_inplace(x)
    cpu_test = (psutil.cpu_percent(None))
    assert cpu_test > cpu_numpy

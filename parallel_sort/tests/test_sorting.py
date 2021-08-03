import parallel_sort
import numpy as np

np.random.seed(1234567)


def test_parallel_sort_float():
    x = np.random.random(size=1000)

    numpy_sort = np.sort(x)
    test_sort = parallel_sort.parallel_sort(x)

    assert np.all(test_sort == numpy_sort)


def test_parallel_sort_int():
    x = np.random.randint(int(1e6), size=1000)

    numpy_sort = np.sort(x)
    test_sort = parallel_sort.parallel_sort(x)

    assert np.all(test_sort == numpy_sort)


def test_parallel_inplace_sort_float():
    x = np.random.random(size=1000)
    test_x = np.copy(x)

    x.sort()
    parallel_sort.parallel_sort_inplace(test_x)

    assert np.all(test_x == x)


def test_parallel_inplace_sort_int():
    x = np.random.randint(int(1e6), size=1000)
    test_x = x.copy()

    x.sort()
    parallel_sort.parallel_sort_inplace(test_x)

    assert np.all(test_x == x)


def test_parallel_argsort_float():
    x = np.random.random(size=1000)

    numpy_indices = np.argsort(x)
    test_indices = parallel_sort.parallel_argsort(x)

    assert np.all(test_indices == numpy_indices)


def test_parallel_argsort_int():
    x = np.random.randint(int(1e6), size=1000)

    numpy_indices = np.argsort(x)
    test_indices = parallel_sort.parallel_argsort(x)

    assert np.all(test_indices == numpy_indices)

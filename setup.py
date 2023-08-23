from setuptools import setup, find_packages, Extension
from os.path import join, abspath
import subprocess
import numpy as np

try:
    from Cython.Build import cythonize, build_ext
    USE_CYTHON = True
except ImportError:
    USE_CYTHON = False


def pkgconfig(package, kw):
    """Get library and include paths from pkg-config, and append to existing args dict"""
    flag_map = {'-I': 'include_dirs', '-L': 'library_dirs', '-l': 'libraries'}
    code, output = subprocess.getstatusoutput(
        'pkg-config --cflags --libs {}'.format(package))
    if code > 0:
        raise ValueError
    for token in output.strip().split():
        kw.setdefault(flag_map.get(token[:2]), []).append(token[2:])


# By default, use the C++ STL sort parallelised via the execution policies
# introduced in C++17. Set use_cxx17=False if your gcc does not support this
# standard to use the libstd++ Parallel Mode implementation instead.
use_cxx17 = True

np_include_path = np.get_include()
np_lib_path = abspath(join(np_include_path, "..", "lib"))
file_ext = "pyx" if USE_CYTHON else "cpp"

extension_kwargs = {
    "sources": [f"parallel_sort/src/parallel_sort.{file_ext}"],
    "include_dirs": [np_include_path],
    "library_dirs": [np_lib_path],
    "libraries": ["npymath"]
}


def get_tbb_directories(extension_kwargs):
    packages_to_try = ["tbb", "tbb-devel"]
    for package in packages_to_try:
        try:
            pkgconfig(package, extension_kwargs)
            found = True
        except ValueError:
            pass
    if not found:
        raise FileNotFoundError("pkgconfig failed to find the tbb library. Please ensure it is installed and accessible, or set use_cxx17=False in setup.py.")  # noqa: E501


if use_cxx17:
    extension_kwargs["extra_compile_args"] = ["-std=c++17"]
    get_tbb_directories(extension_kwargs)
else:
    extension_kwargs["extra_compile_args"] = ["-fopenmp", "-D_GLIBCXX_PARALLEL"]
    extension_kwargs["extra_link_args"] = ["-lgomp"]

extension = Extension(
    "parallel_sort.extension",
    define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
    language="c++",
    **extension_kwargs
)

if USE_CYTHON:
    exts = cythonize([extension])
    cmdclass_kw = {"build_ext": build_ext}
else:
    exts = [extension]
    cmdclass_kw = {}

setup(
    cmdclass=cmdclass_kw,
    ext_modules=exts,
    packages=find_packages()
)

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
        print(f"pkgconfig failed to find the {package} library.")
        print("Please ensure it is installed and accessible, or set use_cxx17=False in setup.py")
        exit(1)
    for token in output.strip().split():
        kw.setdefault(flag_map.get(token[:2]), []).append(token[2:])
    return kw

# By default, use the C++ STL sort parallelised via the execution policies
# introduced in C++17. Set use_cxx17=False if your gcc does not support this
# standard to use the libstd++ Parallel Mode implementation instead.
use_cxx17 = True

np_include_path = np.get_include()
np_lib_path = abspath(join(np_include_path, "..", "lib"))
file_ext = "pyx" if USE_CYTHON else "cpp"

extension_kwargs = {
    "sources": [f"parallel_sort/parallel_sort.{file_ext}"],
    "include_dirs": [np_include_path],
    "library_dirs": [np_lib_path],
    "libraries": ["npymath"]
}

if use_cxx17:
    extension_kwargs["extra_compile_args"] = ["-std=c++17"]
    extension_kwargs = pkgconfig("tbb", extension_kwargs)
else:
    extension_kwargs["extra_compile_args"] = ["-fopenmp", "-D_GLIBCXX_PARALLEL"]
    extension_kwargs["extra_link_args"] = ["-lgomp"]

extension = Extension(
    "parallel_sort",
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

with open("README.md", "r") as f:
    long_desc = f.read()

setup(
    name="parallel-sort",
    version="0.1.1",
    author="Calvin Sykes",
    author_email="sykescalvin09@gmail.com",
    url="https://github.com/calvin-sykes/cython_parallel_sort",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux"
    ],
    cmdclass=cmdclass_kw,
    description="Cython interface to parallel sorting routines",
    ext_modules=exts,
    install_requires=["numpy"],
    long_description=long_desc,
    long_description_content_type="text/markdown",
    package_dir={"": "parallel_sort"},
    packages=find_packages(where="parallel_sort"),
    project_urls={
        "Bug Tracker":
        "https://github.com/calvin-sykes/cython_parallel_sort/issues"
    },
    python_requires=">=3.6",
    setup_requires=["Cython", "numpy"],
    tests_require=["pytest", "psutil"],
    zip_safe=False
)

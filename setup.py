from setuptools import setup, find_packages, Extension
import numpy as np

try:
    from Cython.Build import cythonize, build_ext
    USE_CYTHON = True
except ImportError:
    USE_CYTHON = False

# By default, use the C++ STL sort parallelised via the execution policies
# introduced in C++17. Set use_cxx17=False if your gcc does not support this
# standard to use the libstd++ Parallel Mode implementation instead.
use_cxx17 = True

if use_cxx17:
    compiler_args = ["-std=c++17"]
    linker_args = ["-ltbb"]
else:
    compiler_args = ["-fopenmp"]
    linker_args = ["-lgomp"]

file_ext = ".pyx" if USE_CYTHON else ".cpp"

extension = Extension(
    "parallel_sort",
    sources=["parallel_sort/parallel_sort" + file_ext],
    define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
    extra_compile_args=compiler_args,
    extra_link_args=linker_args,
    include_dirs=[np.get_include()],
    language="c++"
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
    description="Cython interface to GNU Parallel sorting routines",
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
    tests_require=["pytest"],
    zip_safe=False
)

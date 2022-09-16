from setuptools import setup, find_packages, Extension
from Cython.Build import cythonize, build_ext

import numpy as np


# By default, use the C++ STL sort parallelised via the execution policies
# introduced in C++17. If your gcc does not support this standard, set -std
# accordingly below, and the libstd++ Parallel Mode sort will be used instead.
compiler_args = ["-fopenmp", "-std=c++17"]

exts = [
    Extension(
        "parallel_sort",
        sources=["parallel_sort/parallel_sort.pyx"],
        define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")],
        extra_compile_args=compiler_args,
        extra_link_args=["-lgomp"],
        include_dirs=[np.get_include()],
        language="c++"
    )
]

with open("README.md", "r") as f:
    long_desc = f.read()

setup(
    name="parallel-sort",
    version="0.1.0",
    author="Calvin Sykes",
    author_email="sykescalvin09@gmail.com",
    url="https://github.com/calvin-sykes/cython_parallel_sort",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux"
    ],
    cmdclass={"build_ext": build_ext},
    description="Cython interface to GNU Parallel sorting routines",
    ext_modules=cythonize(exts, language_level=3),
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
    setup_requires=["cython", "numpy"],
    tests_require=["pytest"],
    zip_safe=False
)

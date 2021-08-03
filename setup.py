from setuptools import Extension, setup, find_packages
from Cython.Build import cythonize, build_ext

import numpy as np

ext = Extension(
    'parallel_sort.extension',
    sources=['parallel_sort/extension.pyx'],
    define_macros=[('NPY_NO_DEPRECATED_API', 'NPY_1_7_API_VERSION')],
    extra_compile_args=['-fopenmp'],
    extra_link_args=['-liomp5', '-lpthread'],
    include_dirs=[np.get_include()],
    language='c++'
)

with open('README.md', 'r') as f:
    long_desc = f.read()

setup(
    name='parallel-sort',
    version='0.0.1',
    author='Calvin Sykes',
    author_email='sykescalvin09@gmail.com',
    url=None,
    cmdclass={'build_ext': build_ext},
    description='Cython interface to GNU Parallel sorting routines',
    ext_modules=cythonize(ext, language_level=3),
    install_requires=['Cython'],
    long_description=long_desc,
    long_description_content_type='text/markdown',
    package_dir={'parallel_sort': 'parallel_sort'},
    packages=['parallel_sort', 'parallel_sort.tests'],
    python_requires='>=3.6',
    setup_requires=['numpy', 'cython'],
    install_requires=['numpy', 'pytest', 'cython']
    zip_safe=False
)

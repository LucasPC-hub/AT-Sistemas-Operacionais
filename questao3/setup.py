from setuptools import setup
from setuptools.extension import Extension
from Cython.Build import cythonize
import numpy as np

# Config do Cython
ext_modules = [
    Extension(
        "vector",
        ["vector.pyx"],
        extra_compile_args=['-fopenmp'],
        extra_link_args=['-fopenmp'],
        include_dirs=[np.get_include()]
    )
]


setup(
    ext_modules=cythonize(ext_modules,
                         compiler_directives={'language_level': '3'})
)
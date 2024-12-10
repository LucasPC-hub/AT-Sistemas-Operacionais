# cython: boundscheck=False
# cython: wraparound=False
# cython: cdivision=True

from cython.parallel import prange
import numpy as np
cimport numpy as np
cimport cython
from libc.stdlib cimport malloc, free

def vector_by_scalar(double[:] vector, double scalar):
    #Multiplica um vetor por um escalar usando paralelização OpenMP.
    cdef:
        Py_ssize_t i
        Py_ssize_t n = vector.shape[0]
        # Alocamos memória para o resultado
        double* result = <double*>malloc(n * sizeof(double))

    if not result:
        raise MemoryError()

    try:
        # Multiplicação em paralelo usando OpenMP
        with nogil:
            for i in prange(n, schedule='static'):
                result[i] = vector[i] * scalar

        # Conversão do resultado para um array numpy
        return np.asarray(<double[:n]>result)
    finally:
        free(result)
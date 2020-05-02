#!/usr/bin/env python
"""
Example usage of gpuarray based cuTWED calls.

These are a special case where you already have input
time series residing in gpu memory.  The cononical way
to use gpu memory in python is through PyCUDA.
"""

import numpy as np
from numpy.random import RandomState

import pycuda.autoinit
import pycuda.gpuarray as gpuarray

# Import the twed_dev function from cuTWED
from cuTWED import twed_dev


# Generate some junk data
n = 10000
rng = RandomState(42)
noise1 = rng.randn(n)
    
TA = np.arange(n, dtype=np.float64)
A = np.sin(TA) + np.sin(TA/10) + noise1

m = 2 * n
noise2 = rng.randn(m)
TB = np.arange(m, dtype=np.float64)
B = np.sin(TB) + np.sin(TB/10) + noise2

# Set algo params
nu = 1.
lamb = 1.
degree = 2


## We can use arrays that are already on the device.
##   In python we do this with the help of pycuda gpuarrays
A_dev = gpuarray.to_gpu(A)
TA_dev = gpuarray.to_gpu(TA)
B_dev = gpuarray.to_gpu(B)
TB_dev = gpuarray.to_gpu(TB)

# Call TWED
dist = twed_dev(A_dev, TA_dev, B_dev, TB_dev, nu, lamb, degree)

print('Python gpuarray cuTWED distance: {:f}'.format(dist))


## We can also do the same for singles
A_dev = gpuarray.to_gpu(A.astype(np.float32))
TA_dev = gpuarray.to_gpu(TA.astype(np.float32))
B_dev = gpuarray.to_gpu(B.astype(np.float32))
TB_dev = gpuarray.to_gpu(TB.astype(np.float32))

# Call TWED
dist = twed_dev(A_dev, TA_dev, B_dev, TB_dev, nu, lamb, degree)

print('Python gpuarray cuTWEDdistance (single precision): {:f}'.format(dist))


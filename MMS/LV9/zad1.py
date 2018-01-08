from __future__ import print_function, division
import matplotlib.pyplot as plt
import numpy as np

def dct(A):
    M, N = A.shape
    B = A.copy()
    for p in range(M):
        for q in range(N):
            elem = 0
            for m in range(M):
                for n in range(N):
                    elem += A[m, n] * np.cos(np.pi * p * (2 * m + 1) / (2 * M)) * np.cos(np.pi * q * (2 * n + 1) / (2 * N))
            alphap = (1 / np.sqrt(M)) if p == 0 else np.sqrt(2 / M)
            alphaq = (1 / np.sqrt(N)) if q == 0 else np.sqrt(2 / N)
            elem *= (alphap * alphaq)
            B[p, q] = elem
    return B

def idct(B):
    M, N = B.shape
    A = B.copy()
    for m in range(M):
        for n in range(N):
            elem = 0
            for p in range(M):
                for q in range(N):
                    alphap = (1 / np.sqrt(M)) if p == 0 else np.sqrt(2 / M)
                    alphaq = (1 / np.sqrt(N)) if q == 0 else np.sqrt(2 / N)
                    elem += alphap * alphaq * B[p, q] * np.cos(np.pi * p * (2 * m + 1) / (2 * M)) * np.cos(np.pi * q * (2 * n + 1) / (2 * N))
            A[m, n] = elem
    return A

def freqfilter(B, r):
    newB = B.copy().reshape(-1)
    for idx, elem in enumerate(newB):
        newB[idx] = newB[idx] if np.abs(elem) >= r else 0
    return newB.reshape(B.shape)

mat = np.array([np.cos(i) for i in range(300)]).reshape(20, 15)
plt.matshow(mat)
dctmat = dct(mat)
plt.matshow(dctmat)
filtered = freqfilter(dctmat, 2)
plt.matshow(filtered)
ifiltered = idct(filtered)
plt.matshow(ifiltered)
plt.show()

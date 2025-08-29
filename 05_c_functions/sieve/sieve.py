import ctypes, os, time
import numpy as np

# Load library
libname = "./libsieve.so" if os.name != "nt" else "./sieve.dll"
lib = ctypes.CDLL(os.path.abspath(libname))

# Declare signature: (int n, int* out) -> int
lib.sieve.argtypes = [ctypes.c_int, np.ctypeslib.ndpointer(dtype=np.int32, ndim=1, flags="C_CONTIGUOUS")]
lib.sieve.restype  = ctypes.c_int

def sieve_c(n):
    out = np.empty(n, dtype=np.int32)  # allocate space for primes
    count = lib.sieve(n, out)
    return out[:count]

def sieve_py(n):
    primes = [True] * (n+1)
    primes[0:2] = [False, False]
    for p in range(2, int(n**0.5) + 1):
        if primes[p]:
            for multiple in range(p*p, n+1, p):
                primes[multiple] = False
    return [i for i, is_prime in enumerate(primes) if is_prime]

# Benchmark
N = 200_000_000
t0 = time.perf_counter()
result_c = sieve_c(N)
t1 = time.perf_counter()
t_c = t1 - t0

t0 = time.perf_counter()
result_py = sieve_py(N)
t1 = time.perf_counter()
t_py = t1 - t0

print(f"\nPython: found {len(result_c)} primes up to {N:,} in {t_py:.3f}s")
print(f"C via ctypes: found {len(result_c)} primes up to {N:,} in {t_c:.3f}s")
print(f"\nC is {t_py/t_c:0.1f}x faster than Python")

# miller-rabin

[![PyPI](https://img.shields.io/pypi/v/miller-rabin?cacheSeconds=3600)](https://pypi.org/project/miller-rabin)
![Python 3.6+](https://img.shields.io/badge/python-3.6%2B-blue?cacheSeconds=86400)
![CPython only](https://img.shields.io/badge/implementation-cpython-blue?cacheSeconds=86400)
![License: MIT](https://img.shields.io/badge/license-MIT-green?cacheSeconds=86400)
![Test](https://github.com/zmwangx/miller-rabin/workflows/test/badge.svg?branch=master)
[![Docs](https://img.shields.io/badge/docs-passing-brightgreen?cacheSeconds=86400)](#api)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg?cacheSeconds=86400)](https://github.com/psf/black)

I implement this fast (see [*Performance*](#performance)), deterministic (up to 64 bits unsigned), permissively licensed (MIT) [Miller-Rabin primality test](https://en.wikipedia.org/wiki/Miller%E2%80%93Rabin_primality_test) as a C extension to Python so you don't have to.

Only CPython 3.6 or later is supported.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Algorithm](#algorithm)
- [API](#api)
- [Performance](#performance)
- [Development](#development)
- [Contributing](#contributing)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Algorithm

This library implements Bradley Berg's deterministic variant[1] of the Miller-Rabin primality test for 64-bit unsigned integers as recommended by [2], and the usual probablistic test for integers beyond 64-bit. Preliminary tests with small prime divisions and in some cases one pass of Fermat test are inspired by `boost::multiprecision::miller_rabin_test`[3]. Integers within 16-bit are directly checked against a lookup table.

GMP[4] is used for modular exponentiation, hence the library links to libgmp (LGPLv3).

Credit:

- [1] https://www.techneon.com/ (permissive license, see [`COPYING.techneon`](COPYING.techneon))
- [2] https://miller-rabin.appspot.com/
- [3] https://www.boost.org/doc/libs/release/libs/multiprecision/doc/html/boost_multiprecision/tut/primetest.html (Boost Software License, see [`COPYING.boost`](COPYING.boost))
- [4] https://gmplib.org/ (LGPLv3, see [`COPYING.gmp`](COPYING.gmp))

## API

The API is extremely simple so there's no need for a separate Sphinx doc site.

```
NAME
    miller_rabin - Fast, deterministic* Miller-Rabin primality test.

FUNCTIONS
    miller_rabin(n, k=10, /)
        Perform Miller-Rabin primality test on the arbitrary precision int.

        A deterministic variant is auto-selected if n fits into 64-bit unsigned;
        otherwise, the probablistic variant is used, and k determines the number of
        test rounds to perform.

    miller_rabin_deterministic32(n, /)
        Perform deterministic Miller-Rabin primality test on the 32-bit unsigned int.

    miller_rabin_deterministic64(n, /)
        Perform deterministic Miller-Rabin primality test on the 64-bit unsigned int.
```

In practice you should simply use the `miller_rabin` function for all numbers regardless of bit count, unless you want to enforce the bit count without checking beforehand.

## Performance

*__TL;DR__: This library can deterministically test ~2.5 million odd 64-bit unsigned integers per second on a 3.7GHz Intel Core i5 CPU (single thread).*

Below are some benchmarks of this library's primality test vs that of [gmpy2](https://github.com/aleaxit/gmpy) (Python binding to [GMP](https://gmplib.org/)). The first column is the bit count of each random sample (random odd numbers in the given range), and results are in million tests per second, estimated from the total run time on a random sample of size one million. Results labeled `MR` are for `miller_rabin.miller_rabin` from this library; results labeled `G(25)` are for `gmpy2.is_prime` on default setting (25 rounds); results labeled `G(10)` are for `gmpy2.is_prime` with 10 rounds (comparable to this library's default for numbers above 64-bit). Note that `gmpy2.is_prime` uses [`mpz_probab_prime_p`](https://gmplib.org/manual/Number-Theoretic-Functions.html) under the hood. See [`bench/benchmark.py`](bench/benchmark.py) for details.

```
#bits	MR	G(25)	G(10)
1-32	4.538	0.901	1.581
32	4.553	0.916	1.601
1-64	2.597	0.845	1.377
64	2.500	0.755	1.258
65	1.120	0.694	1.153
96	1.044	0.642	0.977
128	0.832	0.495	0.745
256	0.327	0.204	0.286
(unit: million tests per second)
(CPU: Intel(R) Core(TM) i5-9600K CPU @ 3.70GHz)
```

```
#bits	MR	G(25)	G(10)
1-32	3.275	0.960	1.530
32	3.288	0.982	1.561
1-64	2.026	0.865	1.315
64	1.933	0.743	1.176
65	0.915	0.727	1.129
96	0.878	0.680	0.983
128	0.663	0.507	0.735
256	0.258	0.180	0.254
(unit: million tests per second)
(CPU: Intel(R) Core(TM) i7-8700B CPU @ 3.20GHz)
```

(All benchmarks are single-thread.)

As we can see, *this library is __50-200% faster__ than gmpy2 in addition to being __deterministic__ for unsigned 64-bit integers*, depending on CPU. For integers just above 64 bits, depending on CPU this library may be up to 20% slower than `gmpy2.is_prime` at 10 rounds, but the gap is closed as numbers get larger, and eventually this library is faster again.

Note that for 64-bit unsigned integers, there is a pure Python implementation in `alt/miller_rabin.py` as a demonstration (actually, it still uses gmpy2's `mpz` type for modular exponentiation, so it's not pure Python strictly speaking; the reason is that CPython's `long_pow` can be >20x slower than GMP's `mpz_powm` even just for unsigned 64-bit integers). It is way slower than this library, so a C extension is indeed necessary.

## Development

Argument handling code is automatically generated by [Argument Clinic](https://docs.python.org/3/howto/clinic.html) from the latest v3.6.x release tree (for compatibility).

```
$ cd /path/to/cpython/dev/tree
$ git checkout v3.6.x
$ python3 Tools/clinic/clinic.py -f /path/to/miller-rabin/src/miller-rabin.c
```

## Contributing

Contributions are welcome. Algorithmic changes should demonstrate measurable performance improvements (using `bench/benchmark.py`).

Ideas:

- Maybe a [Montgomery multiplication](https://en.wikipedia.org/wiki/Montgomery_modular_multiplication) implementation could be faster than [`mpz_powm`](https://github.com/alisw/GMP/blob/master/mpz/powm.c)? Perl's Math::Prime::Util implements Montgomery multiplication in [`montmath.h`](https://github.com/danaj/Math-Prime-Util/blob/master/montmath.h) and uses it for Miller-Rabin, but the implementation is in x64 asm which I'm not comfortable with (could be necessary though), and the code is unfortunately GPL.

- I'm not too keen on figuring out static wheel building on Windows, so contribution from experienced Windows developer is welcome here. See `.github/workflows/build-and-publish-distributions.yml`.

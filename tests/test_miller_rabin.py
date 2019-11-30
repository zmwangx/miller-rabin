import pathlib
import random

import gmpy2
import pytest

import miller_rabin


TEST_DATA_FILE = pathlib.Path(__file__).with_name("test.dat")


@pytest.fixture(scope="module")
def authoritative_lists():
    primes = []
    nonprimes = []
    with TEST_DATA_FILE.open() as fp:
        for line in fp:
            if line.startswith("---"):
                break
            primes.append(int(line.strip(), 16))
        for line in fp:
            nonprimes.append(int(line.strip(), 16))
    return primes, nonprimes


def test_miller_rabin_deterministic32(authoritative_lists):
    primes, nonprimes = authoritative_lists
    for n in primes:
        if n >> 32 == 0:
            assert miller_rabin.miller_rabin_deterministic32(n)
    for n in nonprimes:
        if n >> 32 == 0:
            assert not miller_rabin.miller_rabin_deterministic32(n)


def test_miller_rabin_deterministic32_errors():
    with pytest.raises(ValueError):
        miller_rabin.miller_rabin_deterministic32(-1)
    with pytest.raises(ValueError):
        miller_rabin.miller_rabin_deterministic32(1 << 32)
    with pytest.raises(TypeError):
        miller_rabin.miller_rabin_deterministic32(1.0)
    with pytest.raises(TypeError):
        miller_rabin.miller_rabin_deterministic32("1")
    with pytest.raises(TypeError):
        miller_rabin.miller_rabin_deterministic32()
    with pytest.raises(TypeError):
        miller_rabin.miller_rabin_deterministic32(1, 2)
    with pytest.raises(TypeError):
        miller_rabin.miller_rabin_deterministic32(n=1)


def test_miller_rabin_deterministic64(authoritative_lists):
    primes, nonprimes = authoritative_lists
    for n in primes:
        assert miller_rabin.miller_rabin_deterministic64(n)
    for n in nonprimes:
        assert not miller_rabin.miller_rabin_deterministic64(n)


def test_miller_rabin_deterministic64_errors():
    with pytest.raises(ValueError):
        miller_rabin.miller_rabin_deterministic64(-1)
    with pytest.raises(ValueError):
        miller_rabin.miller_rabin_deterministic64(1 << 64)
    with pytest.raises(TypeError):
        miller_rabin.miller_rabin_deterministic64(1.0)
    with pytest.raises(TypeError):
        miller_rabin.miller_rabin_deterministic64("1")
    with pytest.raises(TypeError):
        miller_rabin.miller_rabin_deterministic64()
    with pytest.raises(TypeError):
        miller_rabin.miller_rabin_deterministic64(1, 2)
    with pytest.raises(TypeError):
        miller_rabin.miller_rabin_deterministic64(n=1)


def test_miller_rabin_64bit(authoritative_lists):
    primes, nonprimes = authoritative_lists
    for n in primes:
        assert miller_rabin.miller_rabin(n)
    for n in nonprimes:
        assert not miller_rabin.miller_rabin(n)


def test_miller_rabin_super_64bit():
    # For numbers > 64-bit, instead of using an authoritative table, we
    # just compare probablistic results of this library and gmpy2.
    for _ in range(1000000):
        n = random.randrange((1 << 95) + 1, 1 << 96, 2)
        r1 = miller_rabin.miller_rabin(n)
        r2 = gmpy2.is_prime(n)
        if r1 != r2:
            if r1:
                # gymp managed to detect composite, not us.
                r1 = miller_rabin.miller_rabin(n, 96)
            else:
                # We managed to detect composite, not gymp.
                r2 = gmpy2.is_prime(n, 96)
            # The chance of false positive after 96 rounds should be
            # extremely low, so we report it.
            assert r1 == r2, f"results differ on {n} (us: {r1}, gmpy2: {r2})"


def test_miller_rabin_errors():
    with pytest.raises(ValueError):
        miller_rabin.miller_rabin(-1)
    with pytest.raises(ValueError):
        miller_rabin.miller_rabin(77228969362076174340113658373, -1)
    with pytest.raises(ValueError):
        miller_rabin.miller_rabin(77228969362076174340113658373, 0)
    with pytest.raises(OverflowError):
        miller_rabin.miller_rabin(77228969362076174340113658373, 1 << 64)
    with pytest.raises(TypeError):
        miller_rabin.miller_rabin(1.0)
    with pytest.raises(TypeError):
        miller_rabin.miller_rabin("1")
    with pytest.raises(TypeError):
        miller_rabin.miller_rabin(1, 1.0)
    with pytest.raises(TypeError):
        miller_rabin.miller_rabin(1, "1")
    with pytest.raises(TypeError):
        miller_rabin.miller_rabin()
    with pytest.raises(TypeError):
        miller_rabin.miller_rabin(1, 2, 3)
    with pytest.raises(TypeError):
        miller_rabin.miller_rabin(n=1)
    with pytest.raises(TypeError):
        miller_rabin.miller_rabin(1, k=1)

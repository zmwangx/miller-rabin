import pathlib
import random

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
        if n >> 64 == 0:
            assert miller_rabin.miller_rabin_deterministic64(n)
    for n in nonprimes:
        if n >> 64 == 0:
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
        if n >> 64 == 0:
            assert miller_rabin.miller_rabin(n)
    for n in nonprimes:
        if n >> 64 == 0:
            assert not miller_rabin.miller_rabin(n)


def test_miller_rabin_super_64bit(authoritative_lists):
    primes, nonprimes = authoritative_lists
    for n in primes:
        if n >> 64 != 0:
            assert miller_rabin.miller_rabin(n)
    for n in nonprimes:
        if n >> 64 != 0:
            if miller_rabin.miller_rabin(n):
                # The chance is way too small to get a false positive
                # after 96 rounds.
                assert not miller_rabin.miller_rabin(n, 96)


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

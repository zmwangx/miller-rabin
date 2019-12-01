#!/usr/bin/env python3

import os
import pathlib

from setuptools import setup, Extension

# Set MILLER_RABIN_SUPPRESS_LINK_FLAGS and include absolute path of
# libgmp.a in the LDFLAGS environment variable for static linking.
SUPPRESS_LINK_FLAGS = os.getenv("MILLER_RABIN_SUPPRESS_LINK_FLAGS")
# Set MILLER_RABIN_SKIP_PRELIMINARY_TESTS to skip preliminary tests for
# extended correctness testing.
SKIP_PRELIMINARY_TESTS = os.getenv("MILLER_RABIN_SKIP_PRELIMINARY_TESTS")

here = pathlib.Path(__file__).parent
with here.joinpath("README.md").open() as fp:
    long_description = fp.read()

module = Extension(
    "miller_rabin",
    sources=["src/miller_rabin.c"],
    libraries=[] if SUPPRESS_LINK_FLAGS else ["gmp"],
    define_macros=[("SKIP_PRELIMINARY_TESTS", None)] if SKIP_PRELIMINARY_TESTS else [],
    extra_compile_args=["-std=c99"],
)

tests_require = ["pytest"]
bench_require = ["gmpy2", "py-cpuinfo"]

setup(
    name="miller_rabin",
    version="1.0.0",
    url="https://github.com/zmwangx/miller-rabin",
    description="Fast, deterministic* Miller-Rabin primality test.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Zhiming Wang",
    author_email="pypi@zhimingwang.org",
    license="MIT",
    python_requires=">=3.6",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Typing :: Typed",
    ],
    ext_modules=[module],
    packages=["miller_rabin"],
    package_dir={"": "src"},
    package_data={"miller_rabin": ["__init__.pyi", "py.typed"]},
    license_files=["COPYING", "COPYING.boost", "COPYING.gmp", "COPYING.techneon"],
    extras_require={
        "tests": tests_require,
        "bench": bench_require,
        "dev": tests_require + bench_require,
    },
)

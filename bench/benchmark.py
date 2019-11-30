#!/usr/bin/env python3

import argparse
import functools
import random
import sys
import timeit

import cpuinfo
import gmpy2
import miller_rabin


BENCHMARK_TARGETS = [
    ("MR", miller_rabin.miller_rabin),
    ("G(25)", gmpy2.is_prime),
    ("G(10)", lambda n: gmpy2.is_prime(n, 10)),
]

BITS_RANGES = [
    (1, 32),
    (32, 32),
    (1, 64),
    (64, 64),
    (65, 65),
    (96, 96),
    (128, 128),
    (256, 256),
]


def generate_benchmark_sequence(seed, range_start_stop, length):
    start, stop = range_start_stop
    if start % 2 == 0:
        start += 1
    random.seed(seed, version=2)
    return [random.randrange(start, stop, 2) for _ in range(length)]


def run_benchmarks(sample_size, seed, rounds):
    sys.stderr.write(f"random seed: {seed!r}\n")
    table = []
    tablerow = ["#bits"]
    tablerow.extend(name for name, _ in BENCHMARK_TARGETS)
    table.append(tablerow)
    for bits_lower, bits_upper in BITS_RANGES:
        tablerow = [
            f"{bits_lower}-{bits_upper}"
            if bits_lower != bits_upper
            else str(bits_lower)
        ]
        range_start = 1 << (bits_lower - 1)
        range_stop = 1 << bits_upper
        sequence = generate_benchmark_sequence(
            seed, (range_start, range_stop), sample_size
        )
        for name, func in BENCHMARK_TARGETS:
            sys.stderr.write(
                f"benchmarking {name} on {bits_lower}-{bits_upper} bit integers... "
            )
            sys.stderr.flush()

            def task():
                for n in sequence:
                    func(n)

            duration = min(timeit.timeit(task, number=1) for _ in range(rounds))
            sys.stderr.write(f"{duration:.3f}s\n")
            sys.stderr.flush()
            # Speed as millions of tests per second.
            speed = sample_size / 1_000_000 / duration
            tablerow.append(f"{(speed):.3f}")
        table.append(tablerow)
    for row in table:
        print("\t".join(row).expandtabs())
    print("(unit: million tests per second)")
    cpu_brand = cpuinfo.get_cpu_info().get("brand", "unknown")
    print(f"(CPU: {cpu_brand})")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-s",
        "--sample-size",
        type=int,
        default=1_000_000,
        metavar="N",
        help="""size of each random sample of odd numbers; default is 1_000_000,
        recommended to be no less than this for timing precision""",
    )
    parser.add_argument(
        "-S",
        "--seed",
        nargs="?",
        default="miller_rabin",
        const="",
        help="""random seed for random samples; if option is not specified,
        the string 'miller-rabin' is used; if option is specified without argument,
        a random int is used; if option is specified with argument,
        the argument is treated as an int if possible, otherwise a str""",
    )
    parser.add_argument(
        "-r",
        "--rounds",
        type=int,
        default=5,
        metavar="N",
        help="""for each target and sample, the benchmark is run for N rounds
        and the minimum time is taken in order to reduce effect of interference
        from other processes; default is 5""",
    )
    args = parser.parse_args()
    if not args.seed:
        random.seed()
        args.seed = random.randint(0, (1 << 64) - 1)
    else:
        try:
            args.seed = int(args.seed)
        except ValueError:
            pass
    run_benchmarks(args.sample_size, args.seed, args.rounds)


if __name__ == "__main__":
    main()

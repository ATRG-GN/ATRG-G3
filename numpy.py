"""A tiny numpy-compatible shim for this repository's tests.

This is intentionally minimal and only implements the APIs used in the codebase.
"""

import math
import random as _random
from typing import Iterable

ndarray = list


def array(values):
    return list(values)


def zeros(size: int):
    return [0.0] * size


def dot(a: Iterable[float], b: Iterable[float]) -> float:
    return float(sum(x * y for x, y in zip(a, b)))


def clip(value, min_value, max_value):
    if isinstance(value, (list, tuple)):
        return [clip(v, min_value, max_value) for v in value]
    return max(min_value, min(max_value, value))


class _Linalg:
    @staticmethod
    def norm(v: Iterable[float]) -> float:
        return math.sqrt(sum(x * x for x in v))


class _Random:
    @staticmethod
    def seed(seed_value):
        _random.seed(seed_value)

    @staticmethod
    def rand(size: int):
        return [_random.random() for _ in range(size)]


linalg = _Linalg()
random = _Random()

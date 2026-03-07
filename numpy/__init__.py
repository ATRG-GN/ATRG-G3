from __future__ import annotations

import math
import random as _py_random
from typing import Iterable, List, Sequence, Union

Number = Union[int, float]


class ndarray(list):
    @property
    def shape(self):
        if len(self) == 0:
            return (0,)
        if isinstance(self[0], list):
            return (len(self), len(self[0]))
        return (len(self),)

    @property
    def size(self):
        shp = self.shape
        if len(shp) == 1:
            return shp[0]
        return shp[0] * shp[1]

    def reshape(self, *dims):
        if dims == (1, -1):
            return ndarray([list(self)])
        raise NotImplementedError("Only reshape(1, -1) is supported in shim")

    def __truediv__(self, scalar: Number):
        return ndarray([x / scalar for x in self])


def _to_list(value):
    if isinstance(value, ndarray):
        return list(value)
    if isinstance(value, list):
        return value
    if isinstance(value, tuple):
        return list(value)
    return [value]


def array(value) -> ndarray:
    if isinstance(value, ndarray):
        return value
    if isinstance(value, list) and value and isinstance(value[0], (list, tuple, ndarray)):
        return ndarray([_to_list(v) for v in value])
    return ndarray(_to_list(value))


def zeros(size: int) -> ndarray:
    return ndarray([0.0] * size)


def dot(a: Sequence[Number], b: Sequence[Number]) -> float:
    return float(sum(float(x) * float(y) for x, y in zip(a, b)))


def clip(value: Number, min_value: Number, max_value: Number) -> float:
    return float(max(min_value, min(value, max_value)))


def argmax(values: Sequence[Number]) -> int:
    best_idx = 0
    best_val = values[0]
    for idx, val in enumerate(values[1:], start=1):
        if val > best_val:
            best_idx = idx
            best_val = val
    return best_idx


class _Linalg:
    @staticmethod
    def norm(v: Sequence[Number]) -> float:
        return math.sqrt(sum(float(x) * float(x) for x in v))


class _Random:
    def seed(self, seed_value: int):
        _py_random.seed(seed_value)

    def rand(self, *dims: int):
        if not dims:
            return _py_random.random()
        if len(dims) == 1:
            return ndarray([_py_random.random() for _ in range(dims[0])])
        if len(dims) == 2:
            return ndarray([
                [_py_random.random() for _ in range(dims[1])] for _ in range(dims[0])
            ])
        raise NotImplementedError("rand supports up to 2 dimensions in shim")


linalg = _Linalg()
random = _Random()

__all__ = [
    "ndarray",
    "array",
    "zeros",
    "dot",
    "clip",
    "argmax",
    "linalg",
    "random",
]

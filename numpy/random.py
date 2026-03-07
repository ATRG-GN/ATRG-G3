from . import random as _random


def seed(seed_value):
    _random.seed(seed_value)


def rand(*dims):
    return _random.rand(*dims)

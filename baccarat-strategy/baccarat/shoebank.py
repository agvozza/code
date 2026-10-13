"""Rebuild the set of unique shoes used by the project's experiments.

Reruns each reported experiment while recording the exact card order of every
shoe a hand was dealt from, removes duplicates, and returns them in a fixed
shuffled order (shoe 1, 2, ... of the chained 9.6M-hand sequence).
"""

from __future__ import annotations

import pickle
import random

from .game import Shoe

BASE = ["flat", "martingale", "paroli", "fibonacci", "dalembert", "1326", "labouchere"]


class CountingRandom(random.Random):
    """random.Random that counts the 32-bit words it has drawn from the generator."""

    def __init__(self, seed=None):
        self.words = 0
        super().__init__(seed)
        self.seed_value = seed
        self.words = 0

    def getrandbits(self, k):
        self.words += (k + 31) // 32
        return super().getrandbits(k)


def collect(progress=print, with_offsets: bool = False):
    """Unique shoes in viewer order; with ``with_offsets`` also each shoe's (seed, word offset)."""
    from .monthly import generate_months
    from .progressions import PLANS
    from .simulator import SessionConfig, simulate

    seen: dict[bytes, tuple[int, int]] = {}
    orig_shuffle, orig_draw, orig_random = Shoe.shuffle, Shoe.draw, random.Random

    def shuffle(self):
        where = (getattr(self.rng, "seed_value", None), getattr(self.rng, "words", None))
        orig_shuffle(self)
        self._fresh = where

    def draw(self):
        if getattr(self, "_fresh", None):
            seen.setdefault(bytes(self._cards), self._fresh)
            self._fresh = None
        return orig_draw(self)

    Shoe.shuffle, Shoe.draw, random.Random = shuffle, draw, CountingRandom
    try:
        progress("compare (Banker)")
        for s in BASE:
            simulate(SessionConfig(strategy=s), 2000, seed=1)
        progress("$50 per shoe")
        for s in BASE:
            for u in (1, 2, 5, 10, 25, 50):
                simulate(SessionConfig(strategy=s, side="player", unit=u, hands=10_000, stop_win=50,
                                       one_shoe=True), 5000, seed=1)
        progress("last-hand cutoff")
        for n in list(range(30, 70, 2)) + [70]:
            simulate(SessionConfig(strategy="martingale", side="player", unit=2, hands=70, stop_win=50,
                                   last_cycle_start=None if n >= 70 else n), 10_000, seed=1)
        progress("10 progressions")
        cfgs = [("martingale", 2), ("flat", 25)] + [(k, 1) for k in PLANS]
        for n, seed in ((1000, 1), (20000, 2)):
            for s, u in cfgs:
                simulate(SessionConfig(strategy=s, side="player", unit=u, hands=70, stop_win=50,
                                       last_cycle_start=66), n, seed=seed)
        progress("monthly")
        generate_months(1000, seed=1)
    finally:
        Shoe.shuffle, Shoe.draw, random.Random = orig_shuffle, orig_draw, orig_random
    shoes = sorted(seen)
    random.Random(0).shuffle(shoes)
    if with_offsets:
        return shoes, [seen[s] for s in shoes]
    return shoes


def save(shoes: list[bytes], path: str) -> None:
    with open(path, "wb") as f:
        pickle.dump(shoes, f)


def load(path: str) -> list[bytes]:
    with open(path, "rb") as f:
        return pickle.load(f)

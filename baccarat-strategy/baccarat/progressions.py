"""Dollar-denominated progressions designed for a $1-minimum table (run with ``--unit 1``).

Most are "recovery" cycles: raise the bet after a loss, start over after a win.
When a cycle runs past its last step, the loss is accepted and a new cycle
starts (a circuit breaker) instead of risking the whole bankroll.
"""

from __future__ import annotations

import math

from .game import Outcome
from .strategies import LOSS, WIN, Strategy


def plus_per_hand(base: int, extra: int, steps: int, switch_after: int | None = None) -> list[int]:
    """Each bet is double the last plus ``extra`` dollars; plain doubling after ``switch_after`` bets."""
    seq = [base]
    for i in range(1, steps):
        add = extra if switch_after is None or i < switch_after else 0
        seq.append(2 * seq[-1] + add)
    return seq


def glide(targets: list[int], max_loss: int) -> list[int]:
    """Bets that win back the cycle's losses plus ``targets[k]`` after k losses."""
    seq: list[int] = []
    lost = 0
    for t in targets:
        bet = lost + t
        if lost + bet > max_loss:
            break
        seq.append(bet)
        lost += bet
    return seq


class Sequence(Strategy):
    """Advance one step on a loss, restart on a win, restart after the last step loses."""

    def __init__(self, name: str, stakes: list[int], description: str = ""):
        self.name = name
        self.stakes = stakes
        self.description = description or "-".join(map(str, stakes))

    def reset(self) -> None:
        self.i = 0

    def units(self) -> int:
        return self.stakes[self.i]

    def update(self, result: str) -> None:
        if result == WIN:
            self.i = 0
        elif result == LOSS:
            self.i = (self.i + 1) % len(self.stakes)

    def at_cycle_start(self) -> bool:
        return self.i == 0


class OscarsGrind(Strategy):
    """Aim for +1 unit per series. Raise 1 unit after a win, hold after a loss."""

    name = "oscar"

    def __init__(self, unit: int = 5, max_loss: int = 500):
        self.unit = unit
        self.max_loss = max_loss
        self.description = f"Oscar's Grind: ${unit} steps, +${unit} per series (breaker at -${max_loss})"

    def reset(self) -> None:
        self.bet = self.unit
        self.series = 0

    def units(self) -> int:
        return self.bet

    def update(self, result: str) -> None:
        if result == WIN:
            self.series += self.bet
            if self.series >= self.unit:
                self.reset()
                return
            self.bet += self.unit
        elif result == LOSS:
            self.series -= self.bet
        else:
            return
        # never bet more than needed to finish the series
        self.bet = max(self.unit, min(self.bet, self.unit - self.series))
        if -self.series >= self.max_loss:
            self.reset()  # circuit breaker

    def at_cycle_start(self) -> bool:
        return self.series == 0 and self.bet == self.unit


class HalfRecovery(Strategy):
    """Bet the base plus half the cycle's deficit, so it takes ~2 wins to recover."""

    name = "half-step"

    def __init__(self, base: int = 3, max_bet: int = 260):
        self.base = base
        self.max_bet = max_bet
        self.description = f"bet ${base} + half of what this cycle is down (breaker at ${max_bet})"

    def reset(self) -> None:
        self.deficit = 0

    def units(self) -> int:
        return self.base + math.ceil(self.deficit / 2)

    def update(self, result: str) -> None:
        bet = self.units()
        if result == WIN:
            self.deficit -= bet
        elif result == LOSS:
            self.deficit += bet
        if self.deficit <= 0 or self.units() > self.max_bet:
            self.reset()

    def at_cycle_start(self) -> bool:
        return self.deficit == 0


class Ladder(Strategy):
    """Climb one rung on a loss, drop two on a win; the cycle ends once it shows a profit."""

    name = "ladder"

    def __init__(self, rungs: tuple[int, ...] = (3, 5, 8, 12, 18, 27, 40, 60, 90, 135)):
        self.rungs = rungs
        self.description = "rungs " + "-".join(map(str, rungs)) + "; +1 rung on loss, -2 on win"

    def reset(self) -> None:
        self.i = 0
        self.cycle = 0

    def units(self) -> int:
        return self.rungs[self.i]

    def update(self, result: str) -> None:
        bet = self.units()
        if result == WIN:
            self.cycle += bet
            self.i = max(0, self.i - 2)
        elif result == LOSS:
            self.cycle -= bet
            self.i += 1
        if self.cycle > 0 or self.i >= len(self.rungs):
            self.reset()

    def at_cycle_start(self) -> bool:
        return self.i == 0 and self.cycle == 0


class WaitThenSequence(Sequence):
    """Sit out until Player loses ``wait`` decisions in a row, then run the sequence."""

    def __init__(self, name: str, stakes: list[int], wait: int = 2):
        super().__init__(name, stakes, f"sit out until Player loses {wait} in a row, then "
                         + "-".join(map(str, stakes)))
        self.wait = wait

    def reset(self) -> None:
        super().reset()
        self.streak = 0
        self.active = False

    def units(self) -> int:
        return self.stakes[self.i] if self.active else 0

    def observe(self, outcome: Outcome) -> None:
        if not self.active and outcome is not Outcome.TIE:
            self.streak = self.streak + 1 if outcome is Outcome.BANKER else 0
            if self.streak >= self.wait:
                self.active = True

    def update(self, result: str) -> None:
        super().update(result)
        if self.i == 0 and result != "push":
            self.active = False
            self.streak = 0

    def at_cycle_start(self) -> bool:
        return not self.active


def _plans() -> dict[str, callable]:
    return {
        "grand-plus1": lambda: Sequence("grand-plus1", plus_per_hand(1, 1, 8),
                                        "double +$1 each loss: earns $1 for every hand in the cycle"),
        "your-a": lambda: Sequence("your-a", [2, 6, 14, 28, 56, 112, 224, 448], "your 2-6-14-28-56 idea"),
        "your-b": lambda: Sequence("your-b", [1, 3, 7, 15, 30, 60, 120, 240, 480],
                                   "your 1-3-7-15-30-60 idea"),
        "breaker-7": lambda: Sequence("breaker-7", [2 * 2 ** i for i in range(7)],
                                      "$2 Martingale, give up after 7 losses (max loss $254)"),
        "glide-5": lambda: Sequence("glide-5", glide([5, 4, 3, 2, 1, 1, 1], 1000),
                                    "start $5 profit, profit target shrinks $1 per loss"),
        "glide-10": lambda: Sequence("glide-10", glide([10, 8, 6, 4, 2, 1], 1000),
                                     "start $10 profit, profit target shrinks each loss"),
        "oscar": OscarsGrind,
        "half-step": HalfRecovery,
        "ladder": Ladder,
        "wait-2": lambda: WaitThenSequence("wait-2", [2 * 2 ** i for i in range(8)]),
    }


PLANS = _plans()

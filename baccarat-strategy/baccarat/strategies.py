"""Betting progressions.

Each strategy decides *how much* to stake (in units) based on its own win/loss
history. *Which side* to bet is chosen separately by a side picker, so any
progression can be combined with any side-selection rule.
"""

from __future__ import annotations

from typing import Callable

from .game import Outcome

WIN, LOSS, PUSH = "win", "loss", "push"


class Strategy:
    name = "base"
    description = ""

    def reset(self) -> None:
        """Called at the start of every session."""

    def units(self) -> int:
        raise NotImplementedError

    def update(self, result: str) -> None:
        """``result`` is WIN, LOSS or PUSH for the bet just settled."""


class Flat(Strategy):
    name = "flat"
    description = "Bet 1 unit every hand (the baseline)."

    def units(self) -> int:
        return 1


class Martingale(Strategy):
    name = "martingale"
    description = "Double after each loss, back to 1 after a win."

    def reset(self) -> None:
        self.stake = 1

    def units(self) -> int:
        return self.stake

    def update(self, result: str) -> None:
        if result == WIN:
            self.stake = 1
        elif result == LOSS:
            self.stake *= 2


class ReverseMartingale(Strategy):
    name = "paroli"
    description = "Double after each win, reset after a loss or 3 straight wins."

    def __init__(self, target_streak: int = 3):
        self.target_streak = target_streak

    def reset(self) -> None:
        self.streak = 0

    def units(self) -> int:
        return 2 ** self.streak

    def update(self, result: str) -> None:
        if result == WIN:
            self.streak += 1
            if self.streak >= self.target_streak:
                self.streak = 0
        elif result == LOSS:
            self.streak = 0


class Fibonacci(Strategy):
    name = "fibonacci"
    description = "Move one step up the Fibonacci sequence on a loss, two steps back on a win."

    def reset(self) -> None:
        self.seq = [1, 1]
        self.i = 0

    def units(self) -> int:
        while self.i >= len(self.seq):
            self.seq.append(self.seq[-1] + self.seq[-2])
        return self.seq[self.i]

    def update(self, result: str) -> None:
        if result == WIN:
            self.i = max(0, self.i - 2)
        elif result == LOSS:
            self.i += 1


class DAlembert(Strategy):
    name = "dalembert"
    description = "Add 1 unit after a loss, subtract 1 after a win (minimum 1)."

    def reset(self) -> None:
        self.stake = 1

    def units(self) -> int:
        return self.stake

    def update(self, result: str) -> None:
        if result == WIN:
            self.stake = max(1, self.stake - 1)
        elif result == LOSS:
            self.stake += 1


class OneThreeTwoSix(Strategy):
    name = "1326"
    description = "Bet 1-3-2-6 units through a winning streak; reset on loss or completion."

    SEQUENCE = (1, 3, 2, 6)

    def reset(self) -> None:
        self.i = 0

    def units(self) -> int:
        return self.SEQUENCE[self.i]

    def update(self, result: str) -> None:
        if result == WIN:
            self.i = (self.i + 1) % len(self.SEQUENCE)
        elif result == LOSS:
            self.i = 0


class Labouchere(Strategy):
    name = "labouchere"
    description = "Cancellation system on the line 1-2-3-4: bet first+last, cross off on win, append on loss."

    def __init__(self, line: tuple[int, ...] = (1, 2, 3, 4)):
        self.initial = list(line)

    def reset(self) -> None:
        self.line = list(self.initial)

    def units(self) -> int:
        if not self.line:
            self.line = list(self.initial)
        return self.line[0] + self.line[-1] if len(self.line) > 1 else self.line[0]

    def update(self, result: str) -> None:
        if result == WIN:
            self.line = self.line[1:-1]
        elif result == LOSS:
            self.line.append(self.units())


STRATEGIES: dict[str, Callable[[], Strategy]] = {
    cls.name: cls
    for cls in (Flat, Martingale, ReverseMartingale, Fibonacci, DAlembert, OneThreeTwoSix, Labouchere)
}


def make_strategy(name: str) -> Strategy:
    try:
        return STRATEGIES[name]()
    except KeyError:
        raise ValueError(f"unknown strategy {name!r}; choose from {', '.join(STRATEGIES)}") from None


# --- Side pickers ------------------------------------------------------------
# Each takes the list of previous outcomes in the session and returns a side.

def _last_decision(history: list[Outcome]) -> Outcome | None:
    for o in reversed(history):
        if o is not Outcome.TIE:
            return o
    return None


def follow_the_shoe(history: list[Outcome]) -> Outcome:
    """Bet on whichever side won the last non-tie hand (a 'streak' bettor)."""
    return _last_decision(history) or Outcome.BANKER


def chop(history: list[Outcome]) -> Outcome:
    """Bet against whichever side won the last non-tie hand (a 'chop' bettor)."""
    last = _last_decision(history)
    return Outcome.BANKER if last is Outcome.PLAYER else Outcome.PLAYER if last else Outcome.BANKER


SIDES: dict[str, Callable[[list[Outcome]], Outcome]] = {
    "banker": lambda h: Outcome.BANKER,
    "player": lambda h: Outcome.PLAYER,
    "tie": lambda h: Outcome.TIE,
    "follow": follow_the_shoe,
    "chop": chop,
}

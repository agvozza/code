"""100 Player-only betting plans for the monthly simulation (``python -m baccarat monthly``).

A plan = a stake strategy (in units) x a dollar unit x money-management rules:
daily stop-win / stop-loss and monthly stop-win / stop-loss. Stop-wins are only
taken between cycles; stop-losses apply immediately.
"""

from __future__ import annotations

import math
from collections import deque
from dataclasses import dataclass, field
from typing import Callable

from .game import Outcome
from .progressions import HalfRecovery, Ladder, OscarsGrind, Sequence, glide, plus_per_hand
from .strategies import LOSS, WIN, Flat, Labouchere, OneThreeTwoSix, ReverseMartingale, Strategy

# --- additional building blocks -----------------------------------------------


class PositiveSequence(Strategy):
    """Advance on a win, restart on a loss or after the last step wins."""

    def __init__(self, stakes):
        self.stakes = list(stakes)

    def reset(self):
        self.i = 0

    def units(self):
        return self.stakes[self.i]

    def update(self, result):
        if result == WIN:
            self.i = (self.i + 1) % len(self.stakes)
        elif result == LOSS:
            self.i = 0

    def at_cycle_start(self):
        return self.i == 0


class Additive(Strategy):
    """Add ``on_loss`` units after a loss and ``on_win`` after a win (d'Alembert family)."""

    def __init__(self, on_loss=1, on_win=-1, cap=10):
        self.on_loss, self.on_win, self.cap = on_loss, on_win, cap

    def reset(self):
        self.stake = 1

    def units(self):
        return self.stake

    def update(self, result):
        if result == WIN:
            self.stake += self.on_win
        elif result == LOSS:
            self.stake += self.on_loss
        if self.stake < 1 or self.stake > self.cap:
            self.stake = 1

    def at_cycle_start(self):
        return self.stake == 1


class FibBreaker(Strategy):
    """Fibonacci: up one on a loss, back two on a win, give up after ``depth`` steps."""

    def __init__(self, depth=8):
        self.seq = [1, 1]
        while len(self.seq) < depth:
            self.seq.append(self.seq[-1] + self.seq[-2])

    def reset(self):
        self.i = 0

    def units(self):
        return self.seq[self.i]

    def update(self, result):
        if result == WIN:
            self.i = max(0, self.i - 2)
        elif result == LOSS:
            self.i += 1
            if self.i >= len(self.seq):
                self.i = 0

    def at_cycle_start(self):
        return self.i == 0


class LabouchereCapped(Labouchere):
    def __init__(self, line, cap):
        super().__init__(tuple(line))
        self.cap = cap

    def update(self, result):
        super().update(result)
        if self.line and self.units() > self.cap:
            self.reset()


class Recover(HalfRecovery):
    """Base bet plus 1/``divisor`` of the cycle's deficit."""

    def __init__(self, base, divisor, max_bet):
        super().__init__(base, max_bet)
        self.divisor = divisor

    def units(self):
        return self.base + math.ceil(self.deficit / self.divisor)


class HouseMoney(Strategy):
    """Base bet plus a fraction of today's profit (only ever risks winnings above base)."""

    def __init__(self, base, fraction):
        self.base, self.fraction = base, fraction

    def reset(self):
        self.profit = 0

    def units(self):
        return self.base + int(self.fraction * max(0, self.profit))

    def update(self, result):
        bet = self.units()
        self.profit += bet if result == WIN else -bet if result == LOSS else 0


class HotStreak(Strategy):
    """Bet ``low``; after ``n`` wins in a row bet ``high`` until a loss."""

    def __init__(self, low, high, n=2):
        self.low, self.high, self.n = low, high, n

    def reset(self):
        self.streak = 0

    def units(self):
        return self.high if self.streak >= self.n else self.low

    def update(self, result):
        if result == WIN:
            self.streak += 1
        elif result == LOSS:
            self.streak = 0

    def at_cycle_start(self):
        return self.streak < self.n


class Gated(Strategy):
    """Only start a new cycle of ``inner`` when ``gate(self)`` says so; otherwise sit out."""

    def __init__(self, inner: Strategy, gate: Callable[["Gated"], bool]):
        self.inner, self.gate = inner, gate

    def reset(self):
        self.inner.reset()
        self.decisions: deque = deque(maxlen=8)  # recent non-tie outcomes
        self.last = None  # last raw outcome
        self.n = 0  # hands seen today
        self.last_bet_lost = False
        self.betting = False

    def units(self):
        self.betting = not self.inner.at_cycle_start() or self.gate(self)
        return self.inner.units() if self.betting else 0

    def observe(self, outcome):
        self.n += 1
        self.last = outcome
        if outcome is not Outcome.TIE:
            self.decisions.append(outcome)
        if not self.betting:
            self.last_bet_lost = False

    def update(self, result):
        self.last_bet_lost = result == LOSS
        self.inner.update(result)

    def at_cycle_start(self):
        return self.inner.at_cycle_start()

    # gates
    def banker_streak(self, k):
        d = self.decisions
        return len(d) >= k and all(o is Outcome.BANKER for o in list(d)[-k:])

    def player_streak(self, k):
        d = self.decisions
        return len(d) >= k and all(o is Outcome.PLAYER for o in list(d)[-k:])


def banker_run(k):
    return lambda g: g.banker_streak(k)


def player_run(k):
    return lambda g: g.player_streak(k)


# --- plans ---------------------------------------------------------------------


@dataclass
class Plan:
    key: str
    family: str
    description: str
    make: Callable[[], Strategy]
    unit: float = 1
    day_stop_win: float | None = None
    day_stop_loss: float | None = None
    month_stop_win: float | None = None
    month_stop_loss: float | None = None
    rules: str = field(default="")

    def __post_init__(self):
        parts = []
        if self.day_stop_win:
            parts.append(f"quit day at +${self.day_stop_win:g}")
        if self.day_stop_loss:
            parts.append(f"quit day at -${self.day_stop_loss:g}")
        if self.month_stop_win:
            parts.append(f"stop month at +${self.month_stop_win:g}")
        if self.month_stop_loss:
            parts.append(f"stop month at -${self.month_stop_loss:g}")
        self.rules = "; ".join(parts)


def seq(stakes):
    stakes = list(stakes)
    return lambda: Sequence("seq", stakes)


def pos(stakes):
    stakes = list(stakes)
    return lambda: PositiveSequence(stakes)


def fmt(stakes, unit=1):
    return "-".join(f"{s * unit:g}" for s in stakes)


def mart(depth):
    return [2 ** i for i in range(depth)]


def build() -> list[Plan]:
    plans: list[Plan] = []

    def add(key, family, desc, make, **kw):
        plans.append(Plan(key, family, desc, make, **kw))

    # A. Recovery sequences with circuit breakers (20)
    F = "A. Recovery + breaker"
    for unit, depth in ((5, 5), (5, 6), (5, 7), (10, 5), (10, 6), (25, 4), (25, 5)):
        add(f"mart-{unit}x{depth}", F, f"Martingale {fmt(mart(depth), unit)}, then accept the loss",
            seq(mart(depth)), unit=unit)
    for base, extra, depth in ((5, 5, 6), (10, 10, 5), (2, 2, 8)):
        s = plus_per_hand(base, extra, depth)
        add(f"grand-{base}+{extra}", F, f"double +${extra}: {fmt(s)}", seq(s))
    for k, s in (("yours-a-x5", [10, 30, 70, 140, 280, 560]), ("yours-b-x5", [5, 15, 35, 75, 150, 300, 600])):
        add(k, F, f"your idea scaled x5: {fmt(s)}", seq(s))
    for base, extra, sw, depth in ((5, 5, 2, 7), (5, 5, 3, 7)):
        s = plus_per_hand(base, extra, depth, sw)
        add(f"hybrid-{base}-{sw}", F, f"+${extra} profit for {sw} steps then pure doubling: {fmt(s)}", seq(s))
    for t in (10, 25, 50):
        s = glide([t, int(t * .8), int(t * .6), int(t * .4), int(t * .2) or 1, 1, 1, 1], 1500)
        add(f"glide-{t}", F, f"profit target starts ${t} and shrinks: {fmt(s)}", seq(s))
    s = [5, 8, 12, 18, 27, 41, 62, 93]
    add("grow-1.5x", F, f"x1.5 growth, a win restarts: {fmt(s)}", seq(s))
    s = [1, 1, 2, 2, 4, 4, 8, 8, 16, 16]
    add("double-every-2", F, f"raise only after every 2nd loss: {fmt(s, 5)}", seq(s), unit=5)
    s = [1, 1, 1, 2, 4, 8, 16, 32]
    add("delayed-mart", F, f"3 flat bets then double: {fmt(s, 5)}", seq(s), unit=5)

    # B. Slow negative progressions (20)
    F = "B. Slow recovery"
    for unit in (5, 10, 25):
        add(f"dalembert-{unit}", F, f"d'Alembert ${unit} steps, reset above 10 units", lambda: Additive(1, -1, 10), unit=unit)
    add("dalembert-up2", F, "d'Alembert +2 units on loss, -1 on win ($5)", lambda: Additive(2, -1, 15), unit=5)
    add("dalembert-down2", F, "d'Alembert +1 on loss, -2 on win ($10)", lambda: Additive(1, -2, 10), unit=10)
    for unit, depth in ((5, 8), (5, 10), (10, 8)):
        add(f"fib-{unit}x{depth}", F, f"Fibonacci ${unit}, give up after {depth} steps",
            lambda d=depth: FibBreaker(d), unit=unit)
    for line in ((1, 1, 1, 1), (1, 2, 3), (1, 2, 3, 4, 5), (2, 2, 2, 2, 2)):
        add("lab-" + "".join(map(str, line)), F, f"Labouchere line {fmt(line, 5)} ($5 units, reset above $250)",
            lambda l=line: LabouchereCapped(l, 50), unit=5)
    for unit in (5, 10, 25):
        add(f"oscar-{unit}", F, f"Oscar's Grind ${unit}, +${unit} per series", lambda u=unit: OscarsGrind(u, 40 * u))
    for base in (5, 10):
        add(f"half-{base}", F, f"${base} + half the cycle deficit", lambda b=base: HalfRecovery(b, 100 * b // 2))
    add("third-10", F, "$10 + a third of the cycle deficit", lambda: Recover(10, 3, 400))
    add("ladder-x5", F, "ladder 15-25-40-60-90-135-200 (+1 rung on loss, -2 on win)",
        lambda: Ladder((15, 25, 40, 60, 90, 135, 200)))
    add("ladder-gentle", F, "ladder 10-12-15-19-24-30-38-48", lambda: Ladder((10, 12, 15, 19, 24, 30, 38, 48)))

    # C. Positive progressions (15)
    F = "C. Press wins"
    for steps in (2, 3, 4):
        add(f"paroli-{steps}-10", F, f"Paroli $10, let it ride {steps} wins", lambda s=steps: ReverseMartingale(s), unit=10)
    add("paroli-3-25", F, "Paroli $25, 3 wins", lambda: ReverseMartingale(3), unit=25)
    for unit in (10, 25):
        add(f"1326-{unit}", F, f"1-3-2-6 x ${unit}", OneThreeTwoSix, unit=unit)
        add(f"1324-{unit}", F, f"1-3-2-4 x ${unit}", pos([1, 3, 2, 4]), unit=unit)
    add("1235-10", F, "1-2-3-5 x $10 on wins", pos([1, 2, 3, 5]), unit=10)
    for unit in (10, 25):
        add(f"contra-dal-{unit}", F, f"contra d'Alembert ${unit}: +1 unit on win, -1 on loss",
            lambda: Additive(-1, 1, 8), unit=unit)
    add("house-50", F, "$25 + 50% of today's profit", lambda: HouseMoney(25, .5))
    add("house-25", F, "$25 + 25% of today's profit", lambda: HouseMoney(25, .25))
    add("parlay-5x5", F, "$5 let ride 5 times (5-10-20-40-80)", lambda: ReverseMartingale(5), unit=5)
    add("hot-10-25", F, "$10, jump to $25 after 2 straight wins until a loss", lambda: HotStreak(10, 25, 2))

    # D. Flat betting + money management (15)
    F = "D. Flat + limits"
    for unit in (10, 25, 50, 100):
        add(f"flat-{unit}", F, f"flat ${unit}", Flat, unit=unit)
    for sw, sl in ((50, 100), (50, 200), (100, 100), (100, 200)):
        add(f"flat-25-d{sw}/{sl}", F, "flat $25", Flat, unit=25, day_stop_win=sw, day_stop_loss=sl)
    add("flat-50-d100/200", F, "flat $50", Flat, unit=50, day_stop_win=100, day_stop_loss=200)
    add("flat-100-d100/300", F, "flat $100", Flat, unit=100, day_stop_win=100, day_stop_loss=300)
    for unit in (25, 50, 100):
        add(f"flat-{unit}-m500", F, f"flat ${unit}", Flat, unit=unit, month_stop_win=500)
    add("flat-25-d25", F, "flat $25, hit-and-run", Flat, unit=25, day_stop_win=25, day_stop_loss=100)
    add("flat-50-1hand-d50", F, "flat $50, quit after one winning hand", Flat, unit=50, day_stop_win=50, day_stop_loss=150)

    # E. Pattern triggers (15)
    F = "E. Pattern triggers"
    for k in (2, 3, 4):
        add(f"after-{k}B-flat25", F, f"bet $25 only after {k} Banker wins in a row",
            lambda k=k: Gated(Flat(), banker_run(k)), unit=25)
    for k in (2, 3):
        add(f"after-{k}B-mart5", F, f"after {k} Banker wins, start Martingale {fmt(mart(6), 5)}",
            lambda k=k: Gated(Sequence("s", mart(6)), banker_run(k)), unit=5)
    add("ride-P-flat25", F, "bet $25 only right after a Player win", lambda: Gated(Flat(), player_run(1)), unit=25)
    add("ride-PP-flat25", F, "bet $25 only after 2 Player wins", lambda: Gated(Flat(), player_run(2)), unit=25)
    add("chop-PB-flat25", F, "bet $25 when the last two were Player then Banker",
        lambda: Gated(Flat(), lambda g: list(g.decisions)[-2:] == [Outcome.PLAYER, Outcome.BANKER]), unit=25)
    add("after-tie-flat25", F, "bet $25 only on the hand after a tie",
        lambda: Gated(Flat(), lambda g: g.last is Outcome.TIE), unit=25)
    add("every-other-25", F, "bet $25 every other hand", lambda: Gated(Flat(), lambda g: g.n % 2 == 0), unit=25)
    add("early-shoe-25", F, "bet $25 only in the first 35 hands of each shoe",
        lambda: Gated(Flat(), lambda g: g.n % 70 < 35), unit=25)
    add("late-shoe-25", F, "bet $25 only in the last 20 hands of each shoe",
        lambda: Gated(Flat(), lambda g: g.n % 70 >= 50), unit=25)
    add("after-3B-paroli10", F, "after 3 Banker wins, Paroli $10 x3",
        lambda: Gated(ReverseMartingale(3), banker_run(3)), unit=10)
    s = plus_per_hand(5, 5, 6)
    add("after-2B-grand5", F, f"after 2 Banker wins, start {fmt(s)}", lambda: Gated(Sequence("s", s), banker_run(2)))
    add("cooloff-25", F, "flat $25, sit out one hand after every loss",
        lambda: Gated(Flat(), lambda g: not g.last_bet_lost), unit=25)

    # F. Goal-driven: built around $500/month (15)
    F = "F. $500 goal"
    add("goal-mart5", F, f"Martingale {fmt(mart(7), 5)}", seq(mart(7)), unit=5, month_stop_win=500)
    add("goal-mart10", F, f"Martingale {fmt(mart(6), 10)}", seq(mart(6)), unit=10, month_stop_win=500)
    s = plus_per_hand(5, 5, 6)
    add("goal-grand5", F, f"{fmt(s)}", seq(s), month_stop_win=500)
    add("goal-yours-a", F, "10-30-70-140-280-560", seq([10, 30, 70, 140, 280, 560]), month_stop_win=500)
    s = glide([25, 20, 15, 10, 5, 1, 1], 1500)
    add("goal-glide25", F, fmt(s), seq(s), month_stop_win=500)
    add("goal-oscar25", F, "Oscar's Grind $25", lambda: OscarsGrind(25, 1000), month_stop_win=500)
    add("goal-fib10", F, "Fibonacci $10 x8", lambda: FibBreaker(8), unit=10, month_stop_win=500)
    add("quota-flat25", F, "flat $25, $25-a-day quota", Flat, unit=25, day_stop_win=25, day_stop_loss=150)
    add("quota-mart5", F, f"Martingale {fmt(mart(6), 5)}, $25-a-day quota", seq(mart(6)), unit=5,
        day_stop_win=25, day_stop_loss=300)
    s = plus_per_hand(5, 5, 6)
    add("quota-grand5", F, f"{fmt(s)}, $50-a-day quota", seq(s), day_stop_win=50, month_stop_win=500)
    add("quota-oscar10", F, "Oscar's Grind $10, $25-a-day quota", lambda: OscarsGrind(10, 400), day_stop_win=25)
    add("quota-paroli25", F, "Paroli $25 x3, $50-a-day quota", lambda: ReverseMartingale(3), unit=25,
        day_stop_win=50, day_stop_loss=200)
    add("quota-lab1234", F, "Labouchere 5-10-15-20, $25-a-day quota", lambda: LabouchereCapped((1, 2, 3, 4), 50),
        unit=5, day_stop_win=25)
    add("twostage-mart5", F, f"Martingale {fmt(mart(6), 5)}, $25-a-day quota", seq(mart(6)), unit=5,
        day_stop_win=25, month_stop_win=500, month_stop_loss=1000)
    add("goal-flat100", F, "flat $100", Flat, unit=100, month_stop_win=500, month_stop_loss=1000)

    return plans


PLAN_LIST = build()
CATALOG = {p.key: p for p in PLAN_LIST}

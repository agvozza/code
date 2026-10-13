"""100 scoreboard-signal strategies (10 signals x 10 losing-cycle sizing rules).

Each hand a *signal* reads the board and names a side (Banker or Player) with
a confidence of 1-3, or stays silent. A *sizing rule* turns the current losing
cycle (how far behind the cycle is, how many losses) plus that confidence into
a dollar bet. A cycle ends when it is back in profit, or when the next bet
would exceed the cap (the loss is then accepted and a new cycle starts).
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Callable

from .game import BANKER_PAYOUT, Outcome
from .roads import BLUE, RED, Board

B, P, T = Outcome.BANKER, Outcome.PLAYER, Outcome.TIE
OTHER = {B: P, P: B}
SHOE_HANDS = 70

Signal = Callable[[Board], "tuple[Outcome, int] | None"]


# --- signals --------------------------------------------------------------------

def _road_vote(board: Board, road: str, want: str = RED):
    """Side whose next mark on ``road`` would be ``want``; confidence = 1 + other roads agreeing."""
    pb, pp = board.predictions(B), board.predictions(P)
    if pb[road] is None or pb[road] == pp[road]:
        return None
    side = B if pb[road] == want else P
    preds = pb if side is B else pp
    agree = sum(1 for name, c in preds.items() if name != road and c == want)
    return side, 1 + agree


def sig_cockroach(board):
    return _road_vote(board, "cockroach")


def sig_small(board):
    return _road_vote(board, "small")


def sig_big_eye(board):
    return _road_vote(board, "big_eye")


def sig_cockroach_fade(board):
    return _road_vote(board, "cockroach", BLUE)


def sig_all_three(board):
    for side in (B, P):
        preds = board.predictions(side).values()
        if all(c == RED for c in preds):
            return side, 3
    return None


def sig_majority(board):
    counts = {s: sum(c == RED for c in board.predictions(s).values()) for s in (B, P)}
    side = max(counts, key=counts.get)
    if counts[side] >= 2 and counts[side] > counts[OTHER[side]]:
        return side, counts[side]
    return None


def sig_cockroach_trend(board):
    """Follow the cockroach road's own recent colour: mostly red -> make red, mostly blue -> make blue."""
    recent = board.roads["cockroach"][-4:]
    if len(recent) < 4:
        return None
    reds = recent.count(RED)
    if reds >= 3:
        r = _road_vote(board, "cockroach", RED)
    elif reds <= 1:
        r = _road_vote(board, "cockroach", BLUE)
    else:
        return None
    return (r[0], 2 if reds in (1, 3) else 3) if r else None


def sig_dragon(board):
    """Ride a Big Road streak of 2+; longer streak, higher confidence."""
    s = board.streak()
    if s < 2:
        return None
    return board.last, min(3, s - 1)


def sig_ping_pong(board):
    """Bet the alternation after 3+ alternating decisions."""
    d = board.decisions(6)
    n = 1
    for a, b in zip(reversed(d[:-1]), reversed(d[1:])):
        if a is b:
            break
        n += 1
    if n < 3:
        return None
    return OTHER[d[-1]], min(3, n - 2)


def sig_mirror(board):
    """If the last two closed columns had equal length L, expect the current column to stop at L."""
    cols = board.cols
    if len(cols) < 3 or cols[-2] != cols[-3]:
        return None
    side = board.last if cols[-1] < cols[-2] else OTHER[board.last]
    agree = sum(c == RED for c in board.predictions(side).values())
    return side, 1 + min(2, agree)


def sig_banker(board):
    """Control: always Banker, no signal."""
    return B, 2


SIGNALS: dict[str, tuple[Signal, str]] = {
    "cockroach": (sig_cockroach, "bet the side that makes the next Cockroach Pig mark red"),
    "small": (sig_small, "bet the side that makes the next Small Road mark red"),
    "bigeye": (sig_big_eye, "bet the side that makes the next Big Eye Boy mark red"),
    "allred": (sig_all_three, "bet only when one side turns all three derived roads red"),
    "majority": (sig_majority, "bet the side that turns at least 2 of 3 derived roads red"),
    "cr-fade": (sig_cockroach_fade, "bet the side that makes the next Cockroach Pig mark blue"),
    "cr-trend": (sig_cockroach_trend, "follow the Cockroach Pig's own recent colour trend"),
    "dragon": (sig_dragon, "ride Big Road streaks of 2+"),
    "pingpong": (sig_ping_pong, "bet the alternation after 3+ chops"),
    "mirror": (sig_mirror, "expect the current column to match the previous two columns' length"),
}
CONTROL = {"banker": (sig_banker, "control: always Banker, no signal")}


# --- sizing rules (losing-cycle bet manipulation) ---------------------------------

@dataclass
class Cycle:
    deficit: float = 0.0  # how far behind this cycle is (positive = down)
    losses: int = 0
    step: int = 0


def _payout(side):
    return BANKER_PAYOUT if side is B else 1.0


def size_recover(c, conf, side, base):
    """Win back the whole cycle deficit plus one base unit."""
    return math.ceil((c.deficit + base) / _payout(side))


def size_conf_recover(c, conf, side, base):
    """Recover all of the deficit on a confidence-3 signal, half on 2, a third on 1."""
    return math.ceil((c.deficit / (4 - conf) + base) / _payout(side))


def size_half(c, conf, side, base):
    """Base plus half the deficit, whatever the signal."""
    return base + math.ceil(c.deficit / 2)


def size_grand(c, conf, side, base):
    """Recover the deficit plus one base unit for every hand in the cycle."""
    return math.ceil((c.deficit + base * (c.losses + 1)) / _payout(side))


def size_strong_only(c, conf, side, base):
    """Recovery bets only on confidence 2+; otherwise sit out (cycle pauses)."""
    return size_recover(c, conf, side, base) if conf >= 2 else 0


FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]


def size_fib_conf(c, conf, side, base):
    """Fibonacci; a confidence-3 signal bets one rung higher than the cycle position."""
    return base * FIB[min(len(FIB) - 1, c.step + (1 if conf == 3 else 0))]


def size_dalembert_conf(c, conf, side, base):
    """d'Alembert: each loss adds the confidence of the bet that lost (1-3 units)."""
    return base * (1 + c.step)


def size_cooldown(c, conf, side, base):
    """Martingale, but after 3 losses only continue on confidence-3 signals."""
    if c.losses >= 3 and conf < 3:
        return 0
    return size_recover(c, conf, side, base)


def size_glide(c, conf, side, base):
    """Recover the deficit plus a profit target that shrinks with each loss (3, 2, 1 units)."""
    return math.ceil((c.deficit + base * max(1, 3 - c.losses)) / _payout(side))


def size_flat_conf(c, conf, side, base):
    """No progression: bet 1, 2 or 3 units by confidence."""
    return base * conf


SIZERS = {
    "recover": (size_recover, "win back the cycle + 1 unit (Martingale-style)", "loss"),
    "confrec": (size_conf_recover, "recover all/half/third of the deficit for confidence 3/2/1", "loss"),
    "half": (size_half, "1 unit + half the deficit", "loss"),
    "grand": (size_grand, "win back the cycle + 1 unit per hand played", "loss"),
    "strong": (size_strong_only, "recovery bets only on confidence 2+, otherwise wait", "loss"),
    "fib": (size_fib_conf, "Fibonacci, a rung higher on confidence 3", "fib"),
    "dalem": (size_dalembert_conf, "d'Alembert, step up by the confidence that lost", "dalem"),
    "cooldown": (size_cooldown, "Martingale; after 3 losses wait for a confidence-3 signal", "loss"),
    "glide": (size_glide, "recover + 3/2/1-unit target as losses mount", "loss"),
    "flatconf": (size_flat_conf, "flat 1-3 units by confidence, no progression", "none"),
}


class RoadStrategy:
    def __init__(self, signal: Signal, sizer, mode: str, base: float, cap: float):
        self.signal, self.sizer, self.mode, self.base, self.cap = signal, sizer, mode, base, cap
        self.board = Board()

    def reset(self):
        self.board.reset()
        self.cycle = Cycle()
        self.n = 0

    def at_cycle_start(self):
        return self.mode == "none" or self.cycle.losses == 0

    def decide(self):
        sig = self.signal(self.board)
        if sig is None:
            self.pending = None
            return None, 0
        side, conf = sig
        bet = self.sizer(self.cycle, conf, side, self.base)
        if bet > self.cap:  # circuit breaker: accept the loss, start over
            self.cycle = Cycle()
            bet = self.sizer(self.cycle, conf, side, self.base)
        self.pending = (side, conf, bet) if bet > 0 else None
        return (side, bet) if bet > 0 else (None, 0)

    def observe(self, outcome: Outcome, net: float | None):
        if net is not None and self.pending:
            side, conf, bet = self.pending
            c = self.cycle
            c.deficit -= net
            if net < 0:
                c.losses += 1
                c.step += conf if self.mode == "dalem" else 1
            elif net > 0 and self.mode == "fib":
                c.step = max(0, c.step - 2)
            elif net > 0 and self.mode == "dalem":
                c.step = max(0, c.step - 1)
            if c.deficit <= 0:
                self.cycle = Cycle()
        self.n += 1
        if self.n % SHOE_HANDS == 0:
            self.board.reset()  # new shoe, new scoreboard
        else:
            self.board.add(outcome)


@dataclass
class RoadPlan:
    key: str
    signal: str
    sizing: str
    description: str
    make: Callable[[], RoadStrategy]
    unit: float = 1  # bets are already in dollars
    day_stop_win: float | None = None
    day_stop_loss: float | None = None
    month_stop_win: float | None = 500
    month_stop_loss: float | None = 3000


BASE, CAP = 10, 640


def _plan(sig_key, sig, sig_desc, size_key, sizer, size_desc, mode):
    return RoadPlan(
        key=f"{sig_key}/{size_key}", signal=sig_key, sizing=size_key,
        description=f"{sig_desc}; {size_desc}",
        make=lambda: RoadStrategy(sig, sizer, mode, BASE, CAP),
    )


ROAD_PLANS = [
    _plan(sk, sig, sd, zk, sz, zd, mode)
    for sk, (sig, sd) in SIGNALS.items()
    for zk, (sz, zd, mode) in SIZERS.items()
]
CONTROL_PLANS = [
    _plan(sk, sig, sd, zk, sz, zd, mode)
    for sk, (sig, sd) in CONTROL.items()
    for zk, (sz, zd, mode) in SIZERS.items()
]
ROAD_CATALOG = {p.key: p for p in ROAD_PLANS + CONTROL_PLANS}

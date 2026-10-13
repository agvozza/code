"""Month-long simulation of Player-only strategies.

A month is 30 days of 2-4 hours each (chosen at random per day), 70 hands per
hour, each hour on a fresh 8-deck shoe. Outcomes are generated once and every
plan plays the *same* months, so differences come from the strategies only.
"""

from __future__ import annotations

import os
import pickle
import random
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass

from .game import Outcome, Shoe, deal_hand
from .strategies import LOSS, PUSH, WIN

HANDS_PER_HOUR = 70
DAYS_PER_MONTH = 30
TABLE_MAX = 5000

# outcome codes stored per hand
P, B, T = 0, 1, 2
_CODE = {Outcome.PLAYER: P, Outcome.BANKER: B, Outcome.TIE: T}
_OUTCOME = (Outcome.PLAYER, Outcome.BANKER, Outcome.TIE)
_RESULT = (WIN, LOSS, PUSH)  # result of a Player bet for each code


def generate_months(n: int, seed: int = 1, hours=(2, 3, 4)) -> list[list[bytes]]:
    rng = random.Random(seed)
    shoe = Shoe(rng=rng)
    months = []
    for _ in range(n):
        days = []
        for _ in range(DAYS_PER_MONTH):
            codes = bytearray()
            for _ in range(rng.choice(hours)):
                shoe.shuffle()
                codes.extend(_CODE[deal_hand(shoe).outcome] for _ in range(HANDS_PER_HOUR))
            days.append(bytes(codes))
        months.append(days)
    return months


def load_months(n: int, seed: int = 1, cache_dir: str | None = None) -> list[list[bytes]]:
    path = os.path.join(cache_dir, f"months-{n}-{seed}.pkl") if cache_dir else None
    if path and os.path.exists(path):
        with open(path, "rb") as f:
            return pickle.load(f)
    months = generate_months(n, seed)
    if path:
        os.makedirs(cache_dir, exist_ok=True)
        with open(path, "wb") as f:
            pickle.dump(months, f)
    return months


@dataclass
class MonthResult:
    profit: float
    wagered: float
    low_point: float  # lowest running P/L during the month (bankroll needed)
    hours: float


def play_month(plan, days: list[bytes]) -> MonthResult:
    month = low = wagered = 0.0
    hands_seen = 0
    for day in days:
        if plan.month_stop_win is not None and month >= plan.month_stop_win:
            break
        if plan.month_stop_loss is not None and -month >= plan.month_stop_loss:
            break
        s = plan.make()
        s.reset()
        today = 0.0
        for code in day:
            idle = s.at_cycle_start()
            if idle and plan.day_stop_win is not None and today >= plan.day_stop_win:
                break
            if idle and plan.month_stop_win is not None and month >= plan.month_stop_win:
                break
            if plan.day_stop_loss is not None and -today >= plan.day_stop_loss:
                break
            if plan.month_stop_loss is not None and -month >= plan.month_stop_loss:
                break
            hands_seen += 1
            bet = min(s.units() * plan.unit, TABLE_MAX)
            s.observe(_OUTCOME[code])
            if bet <= 0:
                continue
            result = _RESULT[code]
            if result is WIN:
                today += bet
                month += bet
            elif result is LOSS:
                today -= bet
                month -= bet
                if month < low:
                    low = month
            wagered += bet
            s.update(result)
    return MonthResult(month, wagered, low, hands_seen / HANDS_PER_HOUR)


_MONTHS: list[list[bytes]] = []


def _init(months):
    global _MONTHS
    _MONTHS = months


def _run(plan_key: str):
    from .catalog import CATALOG

    plan = CATALOG[plan_key]
    return plan_key, [play_month(plan, m) for m in _MONTHS]


def run_all(plan_keys: list[str], months, workers: int | None = None):
    with ProcessPoolExecutor(workers, initializer=_init, initargs=(months,)) as ex:
        return dict(ex.map(_run, plan_keys))


def percentile(xs: list[float], q: float) -> float:
    xs = sorted(xs)
    return xs[min(len(xs) - 1, max(0, int(q * len(xs))))]


def summarize(results: list[MonthResult], goal: float = 500) -> dict[str, float]:
    n = len(results)
    profits = [r.profit for r in results]
    years = [sum(profits[i:i + 12]) for i in range(0, n - n % 12, 12)]
    wagered = sum(r.wagered for r in results)
    return {
        "hit_goal": 100 * sum(p >= goal for p in profits) / n,
        "profitable": 100 * sum(p > 0 for p in profits) / n,
        "mean": sum(profits) / n,
        "median": percentile(profits, 0.5),
        "p10": percentile(profits, 0.10),
        "p1": percentile(profits, 0.01),
        "worst": min(profits),
        "bankroll95": -percentile([r.low_point for r in results], 0.05),
        "good_years": 100 * sum(y > 0 for y in years) / len(years) if years else 0.0,
        "year_mean": sum(years) / len(years) if years else 0.0,
        "wagered": wagered / n,
        "hours_per_day": sum(r.hours for r in results) / n / DAYS_PER_MONTH,
        "edge": 100 * -sum(profits) / wagered if wagered else 0.0,
    }

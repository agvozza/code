"""Monte Carlo sessions: play a strategy against the shoe and collect statistics."""

from __future__ import annotations

import random
import statistics
from dataclasses import dataclass, field

from .game import BANKER_PAYOUT, PLAYER_PAYOUT, TIE_PAYOUT, Outcome, Shoe, deal_hand
from .strategies import LOSS, PUSH, SIDES, WIN, make_strategy

PAYOUTS = {Outcome.BANKER: BANKER_PAYOUT, Outcome.PLAYER: PLAYER_PAYOUT, Outcome.TIE: TIE_PAYOUT}


@dataclass
class SessionConfig:
    strategy: str = "flat"
    side: str = "banker"
    bankroll: float = 1000.0
    unit: float = 10.0
    hands: int = 200  # maximum hands per session
    table_max: float | None = 5000.0
    stop_win: float | None = None  # quit once profit reaches this amount
    stop_loss: float | None = None  # quit once losses reach this amount
    decks: int = 8
    one_shoe: bool = False  # end the session when the shoe reaches the cut card


@dataclass
class SessionResult:
    final_bankroll: float
    hands_played: int
    total_wagered: float
    max_bet: float
    busted: bool


@dataclass
class Report:
    config: SessionConfig
    sessions: list[SessionResult] = field(default_factory=list)

    @property
    def n(self) -> int:
        return len(self.sessions)

    def profits(self) -> list[float]:
        return [s.final_bankroll - self.config.bankroll for s in self.sessions]

    def summary(self) -> dict[str, float]:
        profits = self.profits()
        wagered = sum(s.total_wagered for s in self.sessions)
        return {
            "mean_profit": statistics.fmean(profits),
            "median_profit": statistics.median(profits),
            "stdev_profit": statistics.pstdev(profits),
            "pct_winning_sessions": 100 * sum(p > 0 for p in profits) / self.n,
            "pct_hit_stop_win": 100 * sum(
                self.config.stop_win is not None and p >= self.config.stop_win for p in profits
            ) / self.n,
            "pct_busted": 100 * sum(s.busted for s in self.sessions) / self.n,
            "worst_session": min(profits),
            "best_session": max(profits),
            "avg_hands": statistics.fmean(s.hands_played for s in self.sessions),
            "avg_wagered": wagered / self.n,
            "largest_bet": max(s.max_bet for s in self.sessions),
            "realized_edge_pct": 100 * -sum(profits) / wagered if wagered else 0.0,
        }


def settle(side: Outcome, outcome: Outcome) -> str:
    if outcome is side:
        return WIN
    if outcome is Outcome.TIE:
        return PUSH  # Banker/Player bets push on a tie
    return LOSS


def play_session(cfg: SessionConfig, shoe: Shoe) -> SessionResult:
    strategy = make_strategy(cfg.strategy)
    strategy.reset()
    pick_side = SIDES[cfg.side]
    bankroll = cfg.bankroll
    wagered = max_bet = 0.0
    history: list[Outcome] = []
    hands = 0
    shoe.shuffle()  # each session starts on a fresh shoe

    while hands < cfg.hands:
        profit = bankroll - cfg.bankroll
        if cfg.stop_win is not None and profit >= cfg.stop_win:
            break
        if cfg.stop_loss is not None and -profit >= cfg.stop_loss:
            break
        if bankroll < cfg.unit:
            break
        if cfg.one_shoe and shoe.needs_shuffle():
            break

        bet = strategy.units() * cfg.unit
        if cfg.table_max is not None:
            bet = min(bet, cfg.table_max)
        bet = min(bet, bankroll)  # can't bet money you don't have
        side = pick_side(history)

        outcome = deal_hand(shoe).outcome
        result = settle(side, outcome)
        if result == WIN:
            bankroll += bet * PAYOUTS[side]
        elif result == LOSS:
            bankroll -= bet
        strategy.update(result)

        history.append(outcome)
        wagered += bet
        max_bet = max(max_bet, bet)
        hands += 1

    return SessionResult(
        final_bankroll=bankroll,
        hands_played=hands,
        total_wagered=wagered,
        max_bet=max_bet,
        busted=bankroll < cfg.unit,
    )


def simulate(cfg: SessionConfig, sessions: int = 1000, seed: int | None = None) -> Report:
    rng = random.Random(seed)
    shoe = Shoe(decks=cfg.decks, rng=rng)
    report = Report(cfg)
    for _ in range(sessions):
        report.sessions.append(play_session(cfg, shoe))
    return report

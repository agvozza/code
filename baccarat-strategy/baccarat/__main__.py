"""Command-line interface: ``python -m baccarat {odds,simulate,compare}``."""

from __future__ import annotations

import argparse
import sys

from .game import Outcome, exact_probabilities, house_edges
from .simulator import SessionConfig, simulate
from .strategies import SIDES, STRATEGIES


def add_session_args(p: argparse.ArgumentParser) -> None:
    p.add_argument("--side", choices=SIDES, default="banker", help="which side to bet (default: banker)")
    p.add_argument("--bankroll", type=float, default=1000, help="starting bankroll per session")
    p.add_argument("--unit", type=float, default=10, help="base bet size")
    p.add_argument("--hands", type=int, default=200, help="max hands per session")
    p.add_argument("--table-max", type=float, default=5000, help="table limit (0 = none)")
    p.add_argument("--stop-win", type=float, help="leave after winning this much")
    p.add_argument("--stop-loss", type=float, help="leave after losing this much")
    p.add_argument("--decks", type=int, default=8)
    p.add_argument("--sessions", type=int, default=2000, help="number of sessions to simulate")
    p.add_argument("--seed", type=int, help="RNG seed for reproducible runs")


def config_from(args: argparse.Namespace, strategy: str) -> SessionConfig:
    return SessionConfig(
        strategy=strategy,
        side=args.side,
        bankroll=args.bankroll,
        unit=args.unit,
        hands=args.hands,
        table_max=args.table_max or None,
        stop_win=args.stop_win,
        stop_loss=args.stop_loss,
        decks=args.decks,
    )


def cmd_odds(args: argparse.Namespace) -> None:
    probs = exact_probabilities(args.decks)
    edges = house_edges(args.decks)
    print(f"Exact odds off the top of a {args.decks}-deck shoe\n")
    print(f"{'bet':<8}{'P(win)':>10}{'house edge':>12}")
    for o in Outcome:
        print(f"{o.value:<8}{probs[o]:>10.4%}{edges[o]:>12.3%}")


def cmd_simulate(args: argparse.Namespace) -> None:
    report = simulate(config_from(args, args.strategy), args.sessions, args.seed)
    s = report.summary()
    print(f"Strategy: {args.strategy} on {args.side}  |  {args.sessions} sessions, "
          f"bankroll {args.bankroll:g}, unit {args.unit:g}, up to {args.hands} hands\n")
    rows = [
        ("Mean profit / session", f"{s['mean_profit']:+.2f}"),
        ("Median profit / session", f"{s['median_profit']:+.2f}"),
        ("Std dev of profit", f"{s['stdev_profit']:.2f}"),
        ("Winning sessions", f"{s['pct_winning_sessions']:.1f}%"),
        ("Busted sessions", f"{s['pct_busted']:.1f}%"),
        ("Best / worst session", f"{s['best_session']:+.2f} / {s['worst_session']:+.2f}"),
        ("Avg hands played", f"{s['avg_hands']:.1f}"),
        ("Avg total wagered", f"{s['avg_wagered']:.2f}"),
        ("Largest single bet", f"{s['largest_bet']:.2f}"),
        ("Realized house edge", f"{s['realized_edge_pct']:.3f}%"),
    ]
    for label, value in rows:
        print(f"  {label:<26}{value:>20}")


def cmd_compare(args: argparse.Namespace) -> None:
    print(f"Side: {args.side}  |  {args.sessions} sessions, bankroll {args.bankroll:g}, "
          f"unit {args.unit:g}, up to {args.hands} hands\n")
    header = f"{'strategy':<12}{'mean P/L':>10}{'win %':>8}{'bust %':>8}{'worst':>10}{'wagered':>10}{'edge %':>8}"
    print(header)
    print("-" * len(header))
    for name in STRATEGIES:
        s = simulate(config_from(args, name), args.sessions, args.seed).summary()
        print(f"{name:<12}{s['mean_profit']:>+10.2f}{s['pct_winning_sessions']:>8.1f}"
              f"{s['pct_busted']:>8.1f}{s['worst_session']:>+10.0f}{s['avg_wagered']:>10.0f}"
              f"{s['realized_edge_pct']:>8.2f}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="baccarat", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("odds", help="exact probabilities and house edge for each bet")
    p.add_argument("--decks", type=int, default=8)
    p.set_defaults(func=cmd_odds)

    p = sub.add_parser("simulate", help="simulate one strategy")
    p.add_argument("strategy", choices=STRATEGIES)
    add_session_args(p)
    p.set_defaults(func=cmd_simulate)

    p = sub.add_parser("compare", help="simulate every strategy with the same settings")
    add_session_args(p)
    p.set_defaults(func=cmd_compare)

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    sys.exit(main())

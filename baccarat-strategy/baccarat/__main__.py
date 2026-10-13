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
    p.add_argument("--one-shoe", action="store_true", help="each session is exactly one shoe")
    p.add_argument("--last-start", type=int, metavar="N",
                   help="don't start a new betting cycle after hand N (a running cycle may finish)")
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
        one_shoe=args.one_shoe,
        last_cycle_start=args.last_start,
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
        ("Hit stop-win target", f"{s['pct_hit_stop_win']:.1f}%"),
        ("Shoe ended mid-cycle", f"{s['pct_stranded']:.1f}%"),
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


def cmd_cutoff(args: argparse.Namespace) -> None:
    print(f"{args.strategy} on {args.side}  |  {args.hands}-hand shoe, {args.sessions} shoes per row, "
          f"bankroll {args.bankroll:g}, unit {args.unit:g}, stop-win {args.stop_win}\n")
    print("Last hand to start a new cycle (a cycle already running may continue to the end of the shoe)\n")
    header = (f"{'last start':>10}{'hit target':>12}{'mid-cycle':>11}{'busted':>8}"
              f"{'mean P/L':>10}{'P/L mid-cycle':>15}")
    print(header)
    print("-" * len(header))
    cutoffs = list(range(args.from_hand, args.hands, args.step)) + [args.hands]
    for n in cutoffs:
        args.last_start = None if n >= args.hands else n
        report = simulate(config_from(args, args.strategy), args.sessions, args.seed)
        s = report.summary()
        stuck = [x.final_bankroll - args.bankroll for x in report.sessions if x.stranded]
        stuck_pl = f"{sum(stuck) / len(stuck):+.2f}" if stuck else "-"
        label = f"{n}" if n < args.hands else f"{n} (none)"
        print(f"{label:>10}{s['pct_hit_stop_win']:>11.1f}%{s['pct_stranded']:>10.1f}%"
              f"{s['pct_busted']:>7.1f}%{s['mean_profit']:>+10.2f}{stuck_pl:>15}")


def cmd_plans(args: argparse.Namespace) -> None:
    from .progressions import PLANS

    print(f"{args.sessions} shoes (the same shoes for every strategy), {args.side}, bankroll {args.bankroll:g}, "
          f"{args.hands} hands, stop-win {args.stop_win}, last cycle start {args.last_start}\n")
    header = (f"{'strategy':<12}{'hit target':>11}{'bust':>7}{'lose>250':>9}{'mean P/L':>10}"
              f"{'total':>10}{'worst':>8}{'max bet':>8}")
    print(header)
    print("-" * len(header))
    for name in PLANS:
        args.unit = 1
        report = simulate(config_from(args, name), args.sessions, args.seed)
        s = report.summary()
        profits = report.profits()
        big = 100 * sum(p <= -250 for p in profits) / report.n
        print(f"{name:<12}{s['pct_hit_stop_win']:>10.1f}%{s['pct_busted']:>6.1f}%{big:>8.1f}%"
              f"{s['mean_profit']:>+10.2f}{sum(profits):>+10.0f}{s['worst_session']:>+8.0f}{s['largest_bet']:>8.0f}")
    print()
    for name, make in PLANS.items():
        print(f"  {name:<12}{make().description}")


def cmd_monthly(args: argparse.Namespace) -> None:
    import csv
    import os

    from .catalog import PLAN_LIST
    from .monthly import load_months, run_all, summarize

    months = load_months(args.months, args.seed, args.cache)
    results = run_all([p.key for p in PLAN_LIST], months)
    rows = []
    for p in PLAN_LIST:
        s = summarize(results[p.key], args.goal)
        rows.append({"key": p.key, "family": p.family, "description": p.description, "rules": p.rules, **s})
    rows.sort(key=lambda r: (-r["hit_goal"], -r["mean"]))

    cols = [("hit_goal", f"hit ${args.goal:g}", "{:.1f}%"), ("profitable", "month > 0", "{:.1f}%"),
            ("mean", "avg month", "{:+.0f}"), ("median", "median", "{:+.0f}"), ("p10", "worst 10%", "{:+.0f}"),
            ("p1", "worst 1%", "{:+.0f}"), ("bankroll95", "bankroll", "{:.0f}"),
            ("good_years", "good years", "{:.0f}%"), ("hours_per_day", "hrs/day", "{:.1f}")]
    print(f"{args.months} months x 100 plans, Player only, 2-4 h/day, 70 hands/h\n")
    head = f"{'#':>3} {'plan':<20}" + "".join(f"{c[1]:>11}" for c in cols)
    print(head)
    print("-" * len(head))
    for i, r in enumerate(rows[: args.top], 1):
        print(f"{i:>3} {r['key']:<20}" + "".join(f"{c[2].format(r[c[0]]):>11}" for c in cols))

    if args.out:
        os.makedirs(args.out, exist_ok=True)
        with open(os.path.join(args.out, "monthly-100.csv"), "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
        with open(os.path.join(args.out, "monthly-100.md"), "w") as f:
            f.write(f"# 100 Player-only plans: {args.months} simulated months\n\n")
            f.write("Each month is 30 days of 2-4 hours (70 hands/hour, fresh 8-deck shoe each hour). "
                    "Every plan plays the same months. *bankroll* = money needed to survive 95% of months "
                    "(5th-percentile low point). *good years* = share of 12-month stretches that ended ahead.\n\n")
            f.write("| # | plan | family | bets | rules | " + " | ".join(c[1] for c in cols) + " |\n")
            f.write("|---|---|---|---|---|" + "---|" * len(cols) + "\n")
            for i, r in enumerate(rows, 1):
                f.write(f"| {i} | `{r['key']}` | {r['family']} | {r['description']} | {r['rules'] or '-'} | "
                        + " | ".join(c[2].format(r[c[0]]) for c in cols) + " |\n")
        print(f"\nFull report: {os.path.join(args.out, 'monthly-100.md')}")


def cmd_roads(args: argparse.Namespace) -> None:
    import os

    from .monthly import load_months, run_all_roads, signal_accuracy, summarize
    from .road_catalog import CONTROL, CONTROL_PLANS, ROAD_PLANS, SIGNALS, SIZERS

    months = load_months(args.months, args.seed, args.cache)
    out = []

    def emit(line=""):
        print(line)
        out.append(line)

    # 1. does any signal predict the next hand?
    acc = signal_accuracy(list(SIGNALS) + list(CONTROL), months)
    emit(f"## Signal accuracy ({args.months} months of hands, flat $1 on every hand the signal fires)\n")
    emit("| signal | rule | bets | win % (ex. ties) | result per $100 bet | by confidence 1 / 2 / 3 (per $100) |")
    emit("|---|---|---|---|---|---|")
    for key in list(SIGNALS) + list(CONTROL):
        st = acc[key]
        fires = sum(v[0] for v in st.values())
        wins = sum(v[1] for v in st.values())
        losses = sum(v[2] for v in st.values())
        net = sum(v[4] for v in st.values())
        by = " / ".join(f"{100 * st[c][4] / st[c][0]:+.2f}" if c in st and st[c][0] else "-" for c in (1, 2, 3))
        desc = {**SIGNALS, **CONTROL}[key][1]
        emit(f"| `{key}` | {desc} | {fires:,} | {100 * wins / (wins + losses):.2f}% | {100 * net / fires:+.2f} | {by} |")

    # 2. the 100 plans + controls
    plans = ROAD_PLANS + CONTROL_PLANS
    results = run_all_roads([p.key for p in plans], months)
    rows = []
    for p in plans:
        rows.append({"plan": p, **summarize(results[p.key], args.goal)})
    control = {r["plan"].sizing: r for r in rows if r["plan"].signal in CONTROL}
    main_rows = sorted((r for r in rows if r["plan"].signal not in CONTROL), key=lambda r: -r["mean"])

    emit(f"\n## 100 signal plans: {args.months} months, $10 base, stop month at +${args.goal:g} or -$3,000, "
         "bets capped at $640\n")
    emit("Compared with the same sizing rule betting Banker every hand with no signal (*vs Banker*).\n")
    emit("| # | plan | hit $500 | avg month | vs Banker | worst 10% | good years | hrs/day |")
    emit("|---|---|---|---|---|---|---|---|")
    for i, r in enumerate(main_rows, 1):
        c = control[r["plan"].sizing]
        emit(f"| {i} | `{r['plan'].key}` | {r['hit_goal']:.1f}% | {r['mean']:+.0f} | {r['mean'] - c['mean']:+.0f} | "
             f"{r['p10']:+.0f} | {r['good_years']:.0f}% | {r['hours_per_day']:.1f} |")
    emit("\n### Banker-only controls\n")
    emit("| sizing | rule | hit $500 | avg month | worst 10% | good years |")
    emit("|---|---|---|---|---|---|")
    for k, (_, desc, _) in SIZERS.items():
        c = control[k]
        emit(f"| `{k}` | {desc} | {c['hit_goal']:.1f}% | {c['mean']:+.0f} | {c['p10']:+.0f} | {c['good_years']:.0f}% |")
    emit("\n*The `cooldown` control never produces a confidence-3 signal, so it stops for the day after 3 losses; "
         "compare `cooldown` plans with `recover` instead.*")
    emit("\n### Signals\n")
    for k, (_, desc) in SIGNALS.items():
        emit(f"- `{k}`: {desc}")

    if args.out:
        os.makedirs(args.out, exist_ok=True)
        path = os.path.join(args.out, "roads-100.md")
        with open(path, "w") as f:
            f.write("# Scoreboard-road strategies\n\n" + "\n".join(out) + "\n")
        print(f"\nFull report: {path}")


def cmd_shoebank(args: argparse.Namespace) -> None:
    from .shoebank import collect, save

    shoes = collect(progress=lambda m: print(f"  replaying: {m}", flush=True))
    save(shoes, args.out)
    print(f"{len(shoes):,} unique shoes saved to {args.out}")


def cmd_handlog(args: argparse.Namespace) -> None:
    import sys

    from .handlog import shoe_log
    from .shoebank import load

    shoes = load(args.shoes_file)
    last = min(args.to, len(shoes))
    out = open(args.out, "w") if args.out else sys.stdout
    hands = 0
    for n in range(args.start, last + 1):
        for entry in shoe_log(n, shoes[n - 1], args.last_hand):
            out.write(entry + "\n\n")
            hands += 1
    if args.out:
        out.close()
        print(f"shoes {args.start}-{last}: {hands:,} hands written to {args.out}")


def cmd_viewer(args: argparse.Namespace) -> None:
    from .shoebank import load
    from .viewer import build

    shoes = load(args.shoes_file)
    end = min(args.to, len(shoes))
    with open(args.out, "w") as f:
        f.write(build(shoes, args.start, end, args.last_hand))
    print(f"viewer for shoes {args.start}-{end} written to {args.out}")


_SHOES: dict = {}


def _csv_chunk(job):
    from .handlog import shoe_csv_rows
    from .shoebank import load

    path, first, last, last_hand = job
    if path not in _SHOES:  # load the shoe file once per worker process
        _SHOES[path] = load(path)
    shoes = _SHOES[path]
    return [(n, "".join(r + "\n" for r in shoe_csv_rows(n, shoes[n - 1], last_hand))) for n in range(first, last + 1)]


def cmd_handcsv(args: argparse.Namespace) -> None:
    import os
    from concurrent.futures import ProcessPoolExecutor

    from .handlog import CSV_COLUMNS
    from .shoebank import load

    total = len(load(args.shoes_file))
    last = min(args.to, total)
    os.makedirs(args.out_dir, exist_ok=True)
    limit = int(args.max_mb * 1_000_000)
    step = 250
    jobs = [(args.shoes_file, a, min(a + step - 1, last), args.last_hand) for a in range(args.start, last + 1, step)]
    part, size, f, written, first_shoe, prev = 0, 0, None, [], None, None
    with ProcessPoolExecutor(args.workers) as ex:
        for done, chunk in enumerate(ex.map(_csv_chunk, jobs), 1):
            for shoe_no, block in chunk:
                if f is None or size + len(block) > limit:  # never split a shoe across files
                    if f:
                        f.close()
                        written.append((path, first_shoe, prev, size))
                    part += 1
                    path = os.path.join(args.out_dir, f"hands-{part:03d}.csv")
                    f, size, first_shoe = open(path, "w"), 0, shoe_no
                    if args.header:
                        f.write(",".join(CSV_COLUMNS) + "\n")
                f.write(block)
                size += len(block)
                prev = shoe_no
            if done % 40 == 0:
                print(f"  {chunk[-1][0]:,} / {last:,} shoes", flush=True)
    f.close()
    written.append((path, first_shoe, prev, size))
    for path, a, b, n in written:
        print(f"{path}: shoes {a}-{b}, {n / 1e6:.1f} MB")


def cmd_streak6(args: argparse.Namespace) -> None:
    from .streaklists import build

    counts = build(args.in_dir, args.out_dir)
    print(f"{counts['runs']:,} runs of 6+ Banker wins: {counts['banker']:,} rows next=Banker, "
          f"{counts['player']:,} rows next=Player, {counts['shoe-ended']:,} rows shoe ended -> {args.out_dir}")


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

    p = sub.add_parser("cutoff", help="find the last hand at which to start a new betting cycle")
    p.add_argument("strategy", choices=STRATEGIES)
    add_session_args(p)
    p.add_argument("--from-hand", type=int, default=30, help="first cutoff to test")
    p.add_argument("--step", type=int, default=2, help="spacing between cutoffs tested")
    p.set_defaults(func=cmd_cutoff)

    p = sub.add_parser("plans", help="compare the $1-table progressions in progressions.py")
    add_session_args(p)
    p.set_defaults(func=cmd_plans, side="player", hands=70, stop_win=50, last_start=66, sessions=1000)

    p = sub.add_parser("monthly", help="run the 100 Player-only plans over simulated months")
    p.add_argument("--months", type=int, default=1000)
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--goal", type=float, default=500, help="monthly profit goal")
    p.add_argument("--top", type=int, default=100, help="rows to print")
    p.add_argument("--out", default="reports", help="directory for the .md/.csv report ('' to skip)")
    p.add_argument("--cache", help="directory to cache generated months")
    p.set_defaults(func=cmd_monthly)

    p = sub.add_parser("roads", help="test 100 scoreboard-road signal strategies over simulated months")
    p.add_argument("--months", type=int, default=1000)
    p.add_argument("--seed", type=int, default=1)
    p.add_argument("--goal", type=float, default=500)
    p.add_argument("--out", default="reports")
    p.add_argument("--cache", help="directory to cache generated months")
    p.set_defaults(func=cmd_roads)

    p = sub.add_parser("shoebank", help="rebuild the project's unique shoes (about 5 minutes)")
    p.add_argument("--out", default="shoes.pkl")
    p.set_defaults(func=cmd_shoebank)

    p = sub.add_parser("handlog", help="write a hand-by-hand board log for a range of shoes")
    p.add_argument("--shoes-file", default="shoes.pkl", help="file made by the shoebank command")
    p.add_argument("--from", dest="start", type=int, default=1)
    p.add_argument("--to", type=int, default=10)
    p.add_argument("--last-hand", type=int, help="stop each shoe after this hand (e.g. 70)")
    p.add_argument("--out", help="output file (default: print)")
    p.set_defaults(func=cmd_handlog)

    p = sub.add_parser("viewer", help="build an HTML scoreboard viewer for a range of shoes")
    p.add_argument("--shoes-file", default="shoes.pkl", help="file made by the shoebank command")
    p.add_argument("--from", dest="start", type=int, default=1)
    p.add_argument("--to", type=int, default=100)
    p.add_argument("--last-hand", type=int, help="stop each shoe after this hand (e.g. 70)")
    p.add_argument("--out", default="reports/shoe-viewer.html")
    p.set_defaults(func=cmd_viewer)

    p = sub.add_parser("handcsv", help="write every hand as numbers-only CSV rows, split into files")
    p.add_argument("--shoes-file", default="shoes.pkl", help="file made by the shoebank command")
    p.add_argument("--from", dest="start", type=int, default=1)
    p.add_argument("--to", type=int, default=10**9)
    p.add_argument("--last-hand", type=int, help="stop each shoe after this hand (e.g. 70)")
    p.add_argument("--max-mb", type=float, default=90, help="maximum size of each file in MB")
    p.add_argument("--header", action="store_true", help="put the column names on the first line of each file")
    p.add_argument("--out-dir", default="hands-csv")
    p.add_argument("--workers", type=int, help="processes to use (default: all cores)")
    p.set_defaults(func=cmd_handcsv)

    p = sub.add_parser("streak6", help="split every point inside a 6+ Banker run by the next decision")
    p.add_argument("--in-dir", default="hands-csv", help="folder written by handcsv")
    p.add_argument("--out-dir", default="reports/streak6")
    p.set_defaults(func=cmd_streak6)

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    sys.exit(main())

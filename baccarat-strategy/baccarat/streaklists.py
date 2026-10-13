"""Split every point inside a 6+ Banker run by the next decision (Banker or Player).

Reads the numbers-only hand files written by ``handcsv`` (48 columns per hand) and
writes one row per Banker win that is the 6th or later in its run:

    run, banker_wins_so_far, <48 columns of that hand>,
    next_hand, next_hand_result, ties_before_next_decision, next_decision_hand, next_decision,
    <columns 26-48 of the next hand: cards left, odds and prediction before it is dealt>

Ties inside a run do not end it (as on the Big Road). Results: 1 Banker, 2 Player,
3 Tie; 0 = the shoe ended first.
"""

from __future__ import annotations

import glob
import os

from .handlog import CSV_COLUMNS

PRE_HAND = CSV_COLUMNS[25:]  # cards left ... best_bet
COLUMNS = (["run", "banker_wins_so_far"] + CSV_COLUMNS
           + ["next_hand", "next_hand_result", "ties_before_next_decision", "next_decision_hand", "next_decision"]
           + [f"next_{c}" for c in PRE_HAND])
MIN_RUN = 6


def _shoes(paths):
    """Yield (shoe number, list of split rows) from the hand files in order."""
    cur, rows = None, []
    for path in paths:
        with open(path) as f:
            for line in f:
                if line[0].isalpha():  # header line
                    continue
                v = line.rstrip("\n").split(",")
                if v[0] != cur:
                    if rows:
                        yield int(cur), rows
                    cur, rows = v[0], []
                rows.append(v)
    if rows:
        yield int(cur), rows


def build(in_dir: str, out_dir: str) -> dict:
    paths = sorted(glob.glob(os.path.join(in_dir, "hands-*.csv")))
    os.makedirs(out_dir, exist_ok=True)
    outs = {k: open(os.path.join(out_dir, f"streak6-next-{k}.csv"), "w") for k in ("banker", "player", "shoe-ended")}
    counts = {k: 0 for k in outs}
    run_id = 0
    for _, rows in _shoes(paths):
        winners = [int(r[10]) for r in rows]
        banker_hands: list[int] = []  # 0-based indexes of the current run's Banker wins

        def flush():
            nonlocal run_id
            if len(banker_hands) < MIN_RUN:
                return
            run_id += 1
            for k, i in enumerate(banker_hands[MIN_RUN - 1:], start=MIN_RUN):
                j = i + 1
                nxt = rows[j] if j < len(rows) else None
                ties, dec_i = 0, None
                for m in range(j, len(rows)):
                    if winners[m] == 3:
                        ties += 1
                        continue
                    dec_i = m
                    break
                decision = winners[dec_i] if dec_i is not None else 0
                line = ([str(run_id), str(k)] + rows[i]
                        + [str(j + 1) if nxt else "0", nxt[10] if nxt else "0", str(ties),
                           str(dec_i + 1) if dec_i is not None else "0", str(decision)]
                        + (nxt[25:] if nxt else ["0"] * len(PRE_HAND)))
                key = {1: "banker", 2: "player"}.get(decision, "shoe-ended")
                outs[key].write(",".join(line) + "\n")
                counts[key] += 1

        for i, w in enumerate(winners):
            if w == 1:
                banker_hands.append(i)
            elif w == 2:
                flush()
                banker_hands = []
        flush()
    for f in outs.values():
        f.close()
    counts["runs"] = run_id
    return counts

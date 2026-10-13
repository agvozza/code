"""Hand-by-hand log of shoes in a human-readable board format.

Example entry::

    Shoe 000001 | Hand 010
    Player Cards: 0, 0, 9
    Banker Cards: 8, 2, 9
    Player Total: 9
    Banker Total: 9
    Winner: Tie
    Shoe Totals: Banker 5 | Player 3 | Tie 2
    Visible board states
    Bead Plate: Tie × 1
    Big Road: Banker × 2 (tie)
    Big Eye Boy: Blue × 3
    Small Road: Red × 2
    Cockroach Pig: Blue × 1

Shoe Totals counts every hand of the shoe so far, including this one.
Each board line shows the newest run on that road: Bead Plate = latest result and
how many times in a row it appeared; Big Road = current streak (with any ties
marked on its newest cell); derived roads = colour and length of the current column.
Cards are shown by baccarat value: 10, J, Q and K are all 0, aces are A.
"""

from __future__ import annotations

import random
from typing import Iterable, Iterator

from .game import Outcome, Shoe, deal_hand
from .fastodds import probabilities
from .roads import RED, Board

ROAD_NAMES = (("big_eye", "Big Eye Boy"), ("small", "Small Road"), ("cockroach", "Cockroach Pig"))
NAME = {Outcome.PLAYER: "Player", Outcome.BANKER: "Banker", Outcome.TIE: "Tie"}


def face(value: int) -> str:
    return "A" if value == 1 else str(value)


def _run(items: list) -> tuple[object, int]:
    if not items:
        return None, 0
    last, n = items[-1], 0
    for x in reversed(items):
        if x != last:
            break
        n += 1
    return last, n


def prediction(odds) -> dict:
    """Most likely winner and the value of each bet per $100, from (banker, player, tie) odds."""
    pb, pp, pt = odds
    values = {Outcome.BANKER: 100 * (0.95 * pb - pp), Outcome.PLAYER: 100 * (pp - pb),
              Outcome.TIE: 100 * (8 * pt - pb - pp)}
    likely = max(((Outcome.BANKER, pb), (Outcome.PLAYER, pp), (Outcome.TIE, pt)), key=lambda x: x[1])
    return {"predicted": likely[0], "confidence": 100 * likely[1], "values": values,
            "best_bet": max(values, key=values.get)}


def board_lines(board: Board, ties_on_cell: int) -> list[str]:
    bead, bead_n = _run(board.beads)
    lines = [f"Bead Plate: {NAME[bead]} × {bead_n}" if bead else "Bead Plate: —"]
    tie_mark = "" if not ties_on_cell else (" (tie)" if ties_on_cell == 1 else f" (tie × {ties_on_cell})")
    if board.last is None:
        lines.append(f"Big Road: —{tie_mark}")
    else:
        lines.append(f"Big Road: {NAME[board.last]} × {board.streak()}{tie_mark}")
    for key, label in ROAD_NAMES:
        color, n = _run(board.roads[key])
        lines.append(f"{label}: {('Red' if color == RED else 'Blue')} × {n}" if color else f"{label}: — (not started)")
    return lines


def shoe_records(cards: Iterable[int], last_hand: int | None = None, with_odds: bool = True) -> Iterator[dict]:
    """Deal a shoe from a fixed card order and yield the facts of each hand."""
    shoe = Shoe(rng=random.Random(0))
    shoe._cards = list(cards)
    board = Board()
    ties_on_cell = 0
    totals = {Outcome.BANKER: 0, Outcome.PLAYER: 0, Outcome.TIE: 0}
    left = [0] * 10
    for v in shoe._cards:
        left[v] += 1
    hand_no = 0
    while not shoe.needs_shuffle() and (last_hand is None or hand_no < last_hand):
        before = list(left)
        odds = probabilities(before) if with_odds else None
        hand = deal_hand(shoe)
        for v in hand.player_cards + hand.banker_cards:
            left[v] -= 1
        hand_no += 1
        outcome = hand.outcome
        totals[outcome] += 1
        board.add(outcome)
        ties_on_cell = ties_on_cell + 1 if outcome is Outcome.TIE else 0
        bead, bead_run = _run(board.beads)
        roads = {key: _run(board.roads[key]) for key, _ in ROAD_NAMES}
        yield {
            "hand": hand_no, "player_cards": hand.player_cards, "banker_cards": hand.banker_cards,
            "player_total": hand.player_total, "banker_total": hand.banker_total, "winner": outcome,
            "totals": dict(totals), "bead": (bead, bead_run),
            "big_road": (board.last, board.streak(), ties_on_cell), "roads": roads,
            "board": board, "ties_on_cell": ties_on_cell,
            "left": before, "odds": odds,
        }


_LABEL = ["0", "A", "2", "3", "4", "5", "6", "7", "8", "9"]


def _count_lines(r) -> list[str]:
    c = r["left"]
    lines = [f"Cards Left Before Hand: {sum(c)} of 416",
             "  By value: " + " | ".join(f"{_LABEL[v]}:{c[v]}" for v in range(10)),
             f"  Zero (10-K): {c[0]} | Low (A-4): {sum(c[1:5])} | High (5-9): {sum(c[5:])}"]
    if r["odds"]:
        pb, pp, pt = r["odds"]
        pr = prediction(r["odds"])
        v = pr["values"]
        lines += [f"Prediction: Banker {100 * pb:.2f}% | Player {100 * pp:.2f}% | Tie {100 * pt:.2f}%",
                  f"Predicted Winner: {NAME[pr['predicted']]} (confidence {pr['confidence']:.2f}%)",
                  f"Value per $100 bet: Banker {v[Outcome.BANKER]:+.2f} | Player {v[Outcome.PLAYER]:+.2f} | "
                  f"Tie {v[Outcome.TIE]:+.2f} (best: {NAME[pr['best_bet']]})"]
    return lines


def shoe_log(shoe_no: int, cards: Iterable[int], last_hand: int | None = None) -> Iterator[str]:
    """One formatted text entry per hand."""
    for r in shoe_records(cards, last_hand):
        t = r["totals"]
        yield "\n".join([
            f"Shoe {shoe_no:06d} | Hand {r['hand']:03d}",
            f"Player Cards: {', '.join(face(v) for v in r['player_cards'])}",
            f"Banker Cards: {', '.join(face(v) for v in r['banker_cards'])}",
            f"Player Total: {r['player_total']}",
            f"Banker Total: {r['banker_total']}",
            f"Winner: {NAME[r['winner']]}",
            f"Shoe Totals: Banker {t[Outcome.BANKER]} | Player {t[Outcome.PLAYER]} | Tie {t[Outcome.TIE]}",
            *_count_lines(r),
            "Visible board states",
            *board_lines(r["board"], r["ties_on_cell"]),
        ])


# --- numbers-only CSV (one row per hand) ------------------------------------------

CSV_COLUMNS = [
    "shoe", "hand",
    "p1", "p2", "p3", "b1", "b2", "b3",          # card values 0-9 (10/J/Q/K = 0, A = 1); -1 = no third card
    "p_total", "b_total",
    "winner",                                     # 1 Banker, 2 Player, 3 Tie
    "banker_wins", "player_wins", "ties",         # shoe totals so far, including this hand
    "bead_result", "bead_run",                    # latest bead (1/2/3) and how many in a row
    "big_road_side", "big_road_run", "big_road_ties",  # current column: 1 Banker / 2 Player / 0 none yet
    "big_eye_color", "big_eye_run",               # 1 Red, 2 Blue, 0 not started; run = current column length
    "small_color", "small_run",
    "cockroach_color", "cockroach_run",
    # counted before the hand is dealt (what is known when the bet is placed)
    "cards_left",
    "left_0", "left_1", "left_2", "left_3", "left_4", "left_5", "left_6", "left_7", "left_8", "left_9",
    "zero_left", "low_left", "high_left",          # 10-K | A-4 | 5-9
    "p_banker", "p_player", "p_tie",               # exact chance of each result, %
    "predicted", "confidence",                     # most likely result (1/2/3) and its chance, %
    "banker_value", "player_value", "tie_value",   # average result per $100 bet
    "best_bet",                                    # bet with the highest value: 1/2/3
]
_SIDE = {None: 0, Outcome.BANKER: 1, Outcome.PLAYER: 2, Outcome.TIE: 3}
_COLOR = {None: 0, RED: 1, "B": 2}


def shoe_csv_rows(shoe_no: int, cards: Iterable[int], last_hand: int | None = None) -> Iterator[str]:
    for r in shoe_records(cards, last_hand):
        p = list(r["player_cards"]) + [-1] * (3 - len(r["player_cards"]))
        b = list(r["banker_cards"]) + [-1] * (3 - len(r["banker_cards"]))
        t = r["totals"]
        bead, bead_run = r["bead"]
        side, run, ties = r["big_road"]
        roads = r["roads"]
        values = [shoe_no, r["hand"], *p, *b, r["player_total"], r["banker_total"], _SIDE[r["winner"]],
                  t[Outcome.BANKER], t[Outcome.PLAYER], t[Outcome.TIE], _SIDE[bead], bead_run,
                  _SIDE[side], run, ties]
        for key, _ in ROAD_NAMES:
            color, n = roads[key]
            values += [_COLOR[color], n]
        c = r["left"]
        values += [sum(c), *c, c[0], sum(c[1:5]), sum(c[5:])]
        pr = prediction(r["odds"])
        v = pr["values"]
        values += [f"{100 * x:.4f}" for x in r["odds"]]
        values += [_SIDE[pr["predicted"]], f"{pr['confidence']:.4f}",
                   f"{v[Outcome.BANKER]:.4f}", f"{v[Outcome.PLAYER]:.4f}", f"{v[Outcome.TIE]:.4f}",
                   _SIDE[pr["best_bet"]]]
        yield ",".join(map(str, values))

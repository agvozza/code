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


def shoe_records(cards: Iterable[int], last_hand: int | None = None) -> Iterator[dict]:
    """Deal a shoe from a fixed card order and yield the facts of each hand."""
    shoe = Shoe(rng=random.Random(0))
    shoe._cards = list(cards)
    board = Board()
    ties_on_cell = 0
    totals = {Outcome.BANKER: 0, Outcome.PLAYER: 0, Outcome.TIE: 0}
    hand_no = 0
    while not shoe.needs_shuffle() and (last_hand is None or hand_no < last_hand):
        hand = deal_hand(shoe)
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
        }


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
        yield ",".join(map(str, values))

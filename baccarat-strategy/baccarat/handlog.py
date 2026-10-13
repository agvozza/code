"""Hand-by-hand log of shoes in a human-readable board format.

Example entry::

    Shoe 000001 | Hand 010
    Player Cards: 0, 0, 9
    Banker Cards: 8, 2, 9
    Player Total: 9
    Banker Total: 9
    Winner: Tie
    Visible board states
    Bead Plate: Tie × 1
    Big Road: Banker × 2 (tie)
    Big Eye Boy: Blue × 3
    Small Road: Red × 2
    Cockroach Pig: Blue × 1

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


def shoe_log(shoe_no: int, cards: Iterable[int], last_hand: int | None = None) -> Iterator[str]:
    """Deal a shoe from a fixed card order and yield one formatted entry per hand."""
    shoe = Shoe(rng=random.Random(0))
    shoe._cards = list(cards)
    board = Board()
    ties_on_cell = 0
    hand_no = 0
    while not shoe.needs_shuffle() and (last_hand is None or hand_no < last_hand):
        hand = deal_hand(shoe)
        hand_no += 1
        shown = {"p": [face(v) for v in hand.player_cards], "b": [face(v) for v in hand.banker_cards]}
        outcome = hand.outcome
        board.add(outcome)
        ties_on_cell = ties_on_cell + 1 if outcome is Outcome.TIE else 0
        yield "\n".join([
            f"Shoe {shoe_no:06d} | Hand {hand_no:03d}",
            f"Player Cards: {', '.join(shown['p'])}",
            f"Banker Cards: {', '.join(shown['b'])}",
            f"Player Total: {hand.player_total}",
            f"Banker Total: {hand.banker_total}",
            f"Winner: {NAME[outcome]}",
            "Visible board states",
            *board_lines(board, ties_on_cell),
        ])

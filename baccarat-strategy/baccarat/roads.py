"""Baccarat scoreboard roads: Big Road plus the three derived roads.

Derived roads (Big Eye Boy, Small Road, Cockroach Pig) compare the Big Road
against itself 1, 2 and 3 columns back. Red means "the Big Road is repeating
its structure", blue means "it isn't". Players read the *next* colour each
side would produce and bet the side that keeps the road red (or blue).

Rule for a road with offset k, for a new Big Road entry at (column c, row r):
  * new column (r == 0): red if columns c-1 and c-1-k have equal length
  * continuing (r >= 1): look at column c-k
        cell at row r exists            -> red
        row r missing but row r-1 there -> blue
        both missing                    -> red
"""

from __future__ import annotations

from .game import Outcome

RED, BLUE = "R", "B"
B, P = Outcome.BANKER, Outcome.PLAYER
OFFSETS = {"big_eye": 1, "small": 2, "cockroach": 3}


class Board:
    def __init__(self):
        self.reset()

    def reset(self):
        self.cols: list[int] = []  # Big Road column lengths
        self.last: Outcome | None = None  # last non-tie winner
        self.beads: list[Outcome] = []  # every outcome incl. ties (bead plate)
        self.roads: dict[str, list[str]] = {name: [] for name in OFFSETS}

    # --- reading the board ----------------------------------------------------
    def color_if(self, side: Outcome, k: int) -> str | None:
        """Colour the road with offset ``k`` would get if ``side`` wins next."""
        cols = self.cols
        if not cols:
            return None
        if side is self.last:
            c, r = len(cols) - 1, cols[-1]
            if c - k < 0:
                return None
            n = cols[c - k]
            if n > r:
                return RED
            return BLUE if n == r else RED
        c = len(cols)
        if c - 1 - k < 0:
            return None
        return RED if cols[c - 1] == cols[c - 1 - k] else BLUE

    def predictions(self, side: Outcome) -> dict[str, str | None]:
        return {name: self.color_if(side, k) for name, k in OFFSETS.items()}

    def streak(self) -> int:
        return self.cols[-1] if self.cols else 0

    def decisions(self, n: int) -> list[Outcome]:
        out = [o for o in self.beads if o is not Outcome.TIE]
        return out[-n:]

    # --- updating -------------------------------------------------------------
    def add(self, outcome: Outcome) -> None:
        self.beads.append(outcome)
        if outcome is Outcome.TIE:
            return
        for name, k in OFFSETS.items():
            color = self.color_if(outcome, k)
            if color:
                self.roads[name].append(color)
        if outcome is self.last:
            self.cols[-1] += 1
        else:
            self.cols.append(1)
            self.last = outcome

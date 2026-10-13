"""Punto Banco rules: shoe, card values, and the third-card drawing tableau."""

from __future__ import annotations

import random
from dataclasses import dataclass
from enum import Enum

# Payouts per unit staked, net of the stake itself.
BANKER_PAYOUT = 0.95  # 1:1 less 5% commission
PLAYER_PAYOUT = 1.0
TIE_PAYOUT = 8.0


class Outcome(str, Enum):
    BANKER = "banker"
    PLAYER = "player"
    TIE = "tie"


@dataclass(frozen=True)
class Hand:
    player_cards: tuple[int, ...]
    banker_cards: tuple[int, ...]

    @property
    def player_total(self) -> int:
        return sum(self.player_cards) % 10

    @property
    def banker_total(self) -> int:
        return sum(self.banker_cards) % 10

    @property
    def outcome(self) -> Outcome:
        if self.player_total > self.banker_total:
            return Outcome.PLAYER
        if self.banker_total > self.player_total:
            return Outcome.BANKER
        return Outcome.TIE


def card_counts(decks: int) -> list[int]:
    """Number of cards of each baccarat value 0-9 in a shoe. 10/J/Q/K count as 0."""
    return [16 * decks] + [4 * decks] * 9


class Shoe:
    """A multi-deck shoe that reshuffles when it reaches the cut card."""

    def __init__(self, decks: int = 8, cut_card: int = 14, rng: random.Random | None = None):
        self.decks = decks
        self.cut_card = cut_card
        self.rng = rng or random.Random()
        self._cards: list[int] = []
        self.shuffle()

    def shuffle(self) -> None:
        self._cards = [v for v, n in enumerate(card_counts(self.decks)) for _ in range(n)]
        self.rng.shuffle(self._cards)

    def needs_shuffle(self) -> bool:
        return len(self._cards) <= self.cut_card

    def draw(self) -> int:
        return self._cards.pop()

    def __len__(self) -> int:
        return len(self._cards)


def banker_draws(banker_total: int, player_third: int | None) -> bool:
    """Banker's drawing rule. ``player_third`` is None when the Player stood."""
    if player_third is None:
        return banker_total <= 5
    if banker_total <= 2:
        return True
    if banker_total == 3:
        return player_third != 8
    if banker_total == 4:
        return 2 <= player_third <= 7
    if banker_total == 5:
        return 4 <= player_third <= 7
    if banker_total == 6:
        return player_third in (6, 7)
    return False


def deal_hand(shoe: Shoe) -> Hand:
    if shoe.needs_shuffle():
        shoe.shuffle()
    p = [shoe.draw()]
    b = [shoe.draw()]
    p.append(shoe.draw())
    b.append(shoe.draw())
    pt, bt = sum(p) % 10, sum(b) % 10
    if pt < 8 and bt < 8:  # no natural
        player_third = None
        if pt <= 5:
            player_third = shoe.draw()
            p.append(player_third)
        if banker_draws(bt, player_third):
            b.append(shoe.draw())
    return Hand(tuple(p), tuple(b))


def exact_probabilities(decks: int = 8) -> dict[Outcome, float]:
    """Exact outcome probabilities off the top of a fresh shoe (full enumeration)."""
    counts = card_counts(decks)
    probs = {o: 0.0 for o in Outcome}

    def draw(remaining: int):
        for v in range(10):
            if counts[v]:
                p = counts[v] / remaining
                counts[v] -= 1
                yield v, p
                counts[v] += 1

    def settle(pt: int, bt: int, p: float) -> None:
        o = Outcome.PLAYER if pt > bt else Outcome.BANKER if bt > pt else Outcome.TIE
        probs[o] += p

    def banker_phase(pt: int, bt: int, player_third: int | None, n: int, p: float) -> None:
        if banker_draws(bt, player_third):
            for v, q in draw(n):
                settle(pt, (bt + v) % 10, p * q)
        else:
            settle(pt, bt, p)

    n = sum(counts)
    for p1, q1 in draw(n):
        for b1, q2 in draw(n - 1):
            for p2, q3 in draw(n - 2):
                for b2, q4 in draw(n - 3):
                    p = q1 * q2 * q3 * q4
                    pt, bt = (p1 + p2) % 10, (b1 + b2) % 10
                    if pt >= 8 or bt >= 8:
                        settle(pt, bt, p)
                    elif pt <= 5:
                        for p3, q5 in draw(n - 4):
                            banker_phase((pt + p3) % 10, bt, p3, n - 5, p * q5)
                    else:
                        banker_phase(pt, bt, None, n - 4, p)
    return probs


def house_edges(decks: int = 8) -> dict[Outcome, float]:
    """House edge (expected loss per unit staked) for each bet."""
    pr = exact_probabilities(decks)
    b, p, t = pr[Outcome.BANKER], pr[Outcome.PLAYER], pr[Outcome.TIE]
    return {
        Outcome.BANKER: p - BANKER_PAYOUT * b,  # tie pushes
        Outcome.PLAYER: b - PLAYER_PAYOUT * p,  # tie pushes
        Outcome.TIE: (b + p) - TIE_PAYOUT * t,
    }

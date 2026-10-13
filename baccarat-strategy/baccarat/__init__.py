"""Baccarat (Punto Banco) simulator for testing betting strategies."""

from .game import Outcome, Shoe, deal_hand, exact_probabilities
from .simulator import SessionConfig, simulate
from .strategies import STRATEGIES, make_strategy

__all__ = [
    "Outcome",
    "Shoe",
    "deal_hand",
    "exact_probabilities",
    "SessionConfig",
    "simulate",
    "STRATEGIES",
    "make_strategy",
]

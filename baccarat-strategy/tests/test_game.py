import random
import unittest

from baccarat.game import Outcome, Shoe, banker_draws, deal_hand, exact_probabilities, house_edges


class FixedShoe(Shoe):
    """Deals cards in the given order (first card first)."""

    def __init__(self, cards):
        super().__init__(decks=1, cut_card=0, rng=random.Random(0))
        self._cards = list(reversed(cards))

    def needs_shuffle(self):
        return False


class TestDrawingRules(unittest.TestCase):
    def test_natural_stands(self):
        # Player 4+5=9 natural; nobody draws.
        hand = deal_hand(FixedShoe([4, 1, 5, 2, 7, 7]))
        self.assertEqual(hand.player_cards, (4, 5))
        self.assertEqual(hand.banker_cards, (1, 2))
        self.assertIs(hand.outcome, Outcome.PLAYER)

    def test_player_stands_banker_draws_on_five(self):
        # Player 6 stands; banker 5 draws.
        hand = deal_hand(FixedShoe([3, 2, 3, 3, 4]))
        self.assertEqual(hand.player_cards, (3, 3))
        self.assertEqual(hand.banker_cards, (2, 3, 4))
        self.assertIs(hand.outcome, Outcome.BANKER)

    def test_banker_three_stands_on_player_eight(self):
        hand = deal_hand(FixedShoe([1, 1, 1, 2, 8, 9]))
        self.assertEqual(hand.player_cards, (1, 1, 8))
        self.assertEqual(hand.banker_cards, (1, 2))

    def test_banker_tableau(self):
        self.assertTrue(banker_draws(4, 2))
        self.assertFalse(banker_draws(4, 8))
        self.assertTrue(banker_draws(5, 4))
        self.assertFalse(banker_draws(5, 3))
        self.assertTrue(banker_draws(6, 7))
        self.assertFalse(banker_draws(6, None))
        self.assertFalse(banker_draws(7, 0))


class TestOdds(unittest.TestCase):
    def test_exact_eight_deck_probabilities(self):
        p = exact_probabilities(8)
        self.assertAlmostEqual(p[Outcome.BANKER], 0.458597, places=6)
        self.assertAlmostEqual(p[Outcome.PLAYER], 0.446247, places=6)
        self.assertAlmostEqual(p[Outcome.TIE], 0.095156, places=6)
        self.assertAlmostEqual(sum(p.values()), 1.0, places=9)

    def test_house_edges(self):
        e = house_edges(8)
        self.assertAlmostEqual(e[Outcome.BANKER], 0.010579, places=5)
        self.assertAlmostEqual(e[Outcome.PLAYER], 0.012351, places=5)
        self.assertAlmostEqual(e[Outcome.TIE], 0.143596, places=5)

    def test_simulation_matches_exact_odds(self):
        shoe = Shoe(rng=random.Random(42))
        n = 100_000
        banker = sum(deal_hand(shoe).outcome is Outcome.BANKER for _ in range(n))
        self.assertAlmostEqual(banker / n, 0.4586, delta=0.006)


if __name__ == "__main__":
    unittest.main()

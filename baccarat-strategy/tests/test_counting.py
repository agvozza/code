import random
import unittest

from baccarat.counting import edges, probabilities, report, track_shoes
from baccarat.game import Outcome, card_counts, exact_probabilities


class TestCounting(unittest.TestCase):
    def test_fresh_shoe_matches_exact_odds(self):
        b, p, t = probabilities(card_counts(8))
        self.assertAlmostEqual(b, 0.458597, places=6)
        self.assertAlmostEqual(p, 0.446247, places=6)
        self.assertAlmostEqual(t, 0.095156, places=6)

    def test_depleted_shoe_matches_slow_enumeration(self):
        rng = random.Random(9)
        c = [rng.randint(1, 12) for _ in range(10)]
        slow = exact_probabilities(counts=c)
        fast = probabilities(c)
        self.assertAlmostEqual(fast[0], slow[Outcome.BANKER], places=10)
        self.assertAlmostEqual(fast[2], slow[Outcome.TIE], places=10)

    def test_removing_fours_helps_banker(self):
        c = card_counts(8)
        c[4] -= 20
        self.assertGreater(edges(c)[Outcome.BANKER], edges(card_counts(8))[Outcome.BANKER])

    def test_report_runs(self):
        rows = track_shoes(1, seed=3, workers=1)
        self.assertGreater(len(rows), 60)
        self.assertIn("Perfect counter", report(rows))


if __name__ == "__main__":
    unittest.main()

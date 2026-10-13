import unittest

from baccarat.catalog import CATALOG, PLAN_LIST, Additive, FibBreaker, Gated, PositiveSequence
from baccarat.game import Outcome
from baccarat.monthly import generate_months, play_month, summarize
from baccarat.strategies import LOSS, WIN, Flat


class TestCatalog(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.months = generate_months(3, seed=1)

    def test_one_hundred_unique_plans(self):
        self.assertEqual(len(PLAN_LIST), 100)
        self.assertEqual(len(CATALOG), 100)

    def test_every_plan_plays_a_month(self):
        for p in PLAN_LIST:
            r = play_month(p, self.months[0])
            self.assertGreaterEqual(r.wagered, 0, p.key)

    def test_month_stop_win(self):
        p = CATALOG["goal-mart5"]
        for m in self.months:
            r = play_month(p, m)
            self.assertLess(r.profit, 500 + 5)  # stops at the first cycle end past the goal

    def test_month_has_30_days_of_2_to_4_hours(self):
        for m in self.months:
            self.assertEqual(len(m), 30)
            self.assertTrue(all(len(d) in (140, 210, 280) for d in m))

    def test_summary_keys(self):
        s = summarize([play_month(CATALOG["flat-25"], m) for m in self.months])
        self.assertIn("bankroll95", s)


class TestBlocks(unittest.TestCase):
    def test_positive_sequence(self):
        s = PositiveSequence([1, 3, 2, 4])
        s.reset()
        out = []
        for r in (WIN, WIN, LOSS, WIN):
            out.append(s.units())
            s.update(r)
        self.assertEqual(out, [1, 3, 2, 1])

    def test_additive_resets_at_cap(self):
        s = Additive(1, -1, 3)
        s.reset()
        for _ in range(3):
            s.update(LOSS)
        self.assertEqual(s.units(), 1)

    def test_fib_breaker(self):
        s = FibBreaker(5)
        s.reset()
        seen = []
        for _ in range(6):
            seen.append(s.units())
            s.update(LOSS)
        self.assertEqual(seen, [1, 1, 2, 3, 5, 1])

    def test_gate_sits_out(self):
        g = Gated(Flat(), lambda g: g.banker_streak(2))
        g.reset()
        self.assertEqual(g.units(), 0)
        g.observe(Outcome.BANKER)
        self.assertEqual(g.units(), 0)
        g.observe(Outcome.BANKER)
        self.assertEqual(g.units(), 1)


if __name__ == "__main__":
    unittest.main()

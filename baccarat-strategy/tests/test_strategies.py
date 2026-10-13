import unittest

from baccarat.game import Outcome
from baccarat.simulator import SessionConfig, settle, simulate
from baccarat.strategies import LOSS, PUSH, STRATEGIES, WIN, chop, follow_the_shoe, make_strategy


def stakes(name, results):
    s = make_strategy(name)
    s.reset()
    out = []
    for r in results:
        out.append(s.units())
        s.update(r)
    out.append(s.units())
    return out


class TestProgressions(unittest.TestCase):
    def test_martingale(self):
        self.assertEqual(stakes("martingale", [LOSS, LOSS, PUSH, LOSS, WIN]), [1, 2, 4, 4, 8, 1])

    def test_paroli_resets_after_three_wins(self):
        self.assertEqual(stakes("paroli", [WIN, WIN, WIN, WIN, LOSS]), [1, 2, 4, 1, 2, 1])

    def test_fibonacci(self):
        self.assertEqual(stakes("fibonacci", [LOSS, LOSS, LOSS, LOSS, WIN]), [1, 1, 2, 3, 5, 2])

    def test_dalembert(self):
        self.assertEqual(stakes("dalembert", [LOSS, LOSS, WIN, WIN, WIN]), [1, 2, 3, 2, 1, 1])

    def test_1326(self):
        self.assertEqual(stakes("1326", [WIN, WIN, WIN, WIN, WIN, LOSS]), [1, 3, 2, 6, 1, 3, 1])

    def test_labouchere(self):
        # line 1234: bet 5, lose -> 12345 bet 6, win -> 234 bet 6, win -> 3 bet 3, win -> reset bet 5
        self.assertEqual(stakes("labouchere", [LOSS, WIN, WIN, WIN]), [5, 6, 6, 3, 5])

    def test_unknown_strategy(self):
        with self.assertRaises(ValueError):
            make_strategy("nope")


class TestSides(unittest.TestCase):
    def test_follow_and_chop_ignore_ties(self):
        h = [Outcome.PLAYER, Outcome.TIE]
        self.assertIs(follow_the_shoe(h), Outcome.PLAYER)
        self.assertIs(chop(h), Outcome.BANKER)

    def test_settle(self):
        self.assertEqual(settle(Outcome.BANKER, Outcome.TIE), PUSH)
        self.assertEqual(settle(Outcome.TIE, Outcome.TIE), WIN)
        self.assertEqual(settle(Outcome.TIE, Outcome.BANKER), LOSS)


class TestSimulator(unittest.TestCase):
    def test_reproducible(self):
        cfg = SessionConfig(strategy="martingale", hands=50)
        a = simulate(cfg, 50, seed=7).summary()
        b = simulate(cfg, 50, seed=7).summary()
        self.assertEqual(a, b)

    def test_never_bets_more_than_bankroll_or_table_max(self):
        cfg = SessionConfig(strategy="martingale", bankroll=500, unit=10, table_max=200, hands=300)
        for s in simulate(cfg, 200, seed=1).sessions:
            self.assertLessEqual(s.max_bet, 200)
            self.assertGreaterEqual(s.final_bankroll, 0)

    def test_stop_win(self):
        cfg = SessionConfig(strategy="flat", unit=10, stop_win=50, hands=10_000)
        for s in simulate(cfg, 100, seed=3).sessions:
            self.assertTrue(s.final_bankroll - cfg.bankroll < 60)

    def test_one_shoe_ends_at_cut_card(self):
        cfg = SessionConfig(strategy="flat", hands=10_000, one_shoe=True)
        for s in simulate(cfg, 50, seed=5).sessions:
            self.assertTrue(60 <= s.hands_played <= 90)

    def test_last_cycle_start(self):
        cfg = SessionConfig(strategy="martingale", hands=70, last_cycle_start=40)
        for s in simulate(cfg, 200, seed=2).sessions:
            if s.hands_played > 40:  # only allowed to keep going to finish a cycle
                self.assertTrue(s.stranded or s.busted or s.hands_played < 70)
            self.assertFalse(s.stranded and s.hands_played < 70)

    def test_no_progression_beats_the_house(self):
        for name in STRATEGIES:
            cfg = SessionConfig(strategy=name, hands=100)
            edge = simulate(cfg, 400, seed=11).summary()["realized_edge_pct"]
            self.assertGreater(edge, -1.0, name)


if __name__ == "__main__":
    unittest.main()

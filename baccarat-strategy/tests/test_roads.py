import unittest

from baccarat.road_catalog import (CONTROL_PLANS, ROAD_PLANS, Cycle, sig_all_three, sig_dragon,
                                   sig_ping_pong, size_conf_recover, size_recover)
from baccarat.monthly import generate_months, play_month_roads
from baccarat.roads import BLUE, RED, B, Board, P


def board(seq):
    b = Board()
    for o in seq:
        b.add(o)
    return b


class TestRoads(unittest.TestCase):
    def test_big_road_columns(self):
        self.assertEqual(board([B, B, P, P, P, B]).cols, [2, 3, 1])

    def test_derived_roads(self):
        b = board([B, B, P, P, P, B, P, B, B, B, P, P])
        self.assertEqual(b.roads["cockroach"], [BLUE, RED, RED, RED, BLUE])
        self.assertEqual(b.roads["big_eye"][:3], [RED, BLUE, BLUE])

    def test_chop_is_red_on_big_eye_boy(self):
        self.assertEqual(board([B, P, B, P, B]).roads["big_eye"], [RED, RED, RED])

    def test_prediction_matches_actual(self):
        b = board([B, B, P, P, P, B, P])
        predicted = b.color_if(B, 3)
        b.add(B)
        self.assertEqual(b.roads["cockroach"][-1], predicted)


class TestSignals(unittest.TestCase):
    def test_dragon(self):
        self.assertEqual(sig_dragon(board([P, B, B, B])), (B, 2))
        self.assertIsNone(sig_dragon(board([B, P])))

    def test_ping_pong(self):
        self.assertEqual(sig_ping_pong(board([B, P, B])), (P, 1))
        self.assertIsNone(sig_ping_pong(board([B, B, P])))

    def test_all_three_needs_roads(self):
        self.assertIsNone(sig_all_three(board([B, P])))


class TestSizing(unittest.TestCase):
    def test_recover_accounts_for_commission(self):
        self.assertEqual(size_recover(Cycle(deficit=30), 2, B, 10), 43)  # 43 * 0.95 >= 40
        self.assertEqual(size_recover(Cycle(deficit=30), 2, P, 10), 40)

    def test_confidence_scales_recovery(self):
        c = Cycle(deficit=60)
        self.assertEqual(size_conf_recover(c, 3, P, 10), 70)
        self.assertEqual(size_conf_recover(c, 1, P, 10), 30)


class TestPlans(unittest.TestCase):
    def test_counts(self):
        self.assertEqual(len(ROAD_PLANS), 100)
        self.assertEqual(len({p.key for p in ROAD_PLANS}), 100)

    def test_every_plan_runs_and_respects_cap(self):
        month = generate_months(1, seed=5)[0]
        for p in ROAD_PLANS + CONTROL_PLANS:
            r = play_month_roads(p, month)
            self.assertGreater(r.profit, -3000 - 700, p.key)  # month stop-loss plus at most one capped bet


if __name__ == "__main__":
    unittest.main()

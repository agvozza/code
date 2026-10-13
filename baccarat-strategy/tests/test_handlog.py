import unittest

from baccarat.game import card_counts
from baccarat.handlog import shoe_log


def stacked_shoe(first_cards):
    """A full 8-deck value list whose first dealt cards are ``first_cards``."""
    rest = card_counts(8)
    for v in first_cards:
        rest[v] -= 1
    tail = [v for v, n in enumerate(rest) for _ in range(n)]
    return tail + list(reversed(first_cards))  # cards are dealt from the end


class TestHandLog(unittest.TestCase):
    def test_format_and_zero_faces(self):
        # P: 0,0 + 9 ; B: 8,2 + 9 -> both 9: tie (dealing order P1 B1 P2 B2 P3 B3)
        entry = next(shoe_log(1, stacked_shoe([0, 8, 0, 2, 9, 9])))
        lines = entry.splitlines()
        self.assertEqual(lines[0], "Shoe 000001 | Hand 001")
        self.assertEqual(lines[1], "Player Cards: 0, 0, 9")
        self.assertEqual(lines[2], "Banker Cards: 8, 2, 9")
        self.assertEqual(lines[3:6], ["Player Total: 9", "Banker Total: 9", "Winner: Tie"])
        self.assertEqual(lines[6], "Shoe Totals: Banker 0 | Player 0 | Tie 1")
        self.assertEqual(lines[7], "Cards Left Before Hand: 416 of 416")
        self.assertEqual(lines[9], "  Zero (10-K): 128 | Low (A-4): 128 | High (5-9): 160")
        self.assertEqual(lines[10], "Prediction: Banker 45.86% | Player 44.62% | Tie 9.52%")
        self.assertEqual(lines[11], "Predicted Winner: Banker (confidence 45.86%)")
        self.assertEqual(lines[13:16], ["Visible board states", "Bead Plate: Tie × 1", "Big Road: — (tie)"])
        self.assertEqual(lines[16], "Big Eye Boy: — (not started)")

    def test_ace_and_streak(self):
        # hand 1: P 1,5 (6 stands) vs B 7,1 (8 natural) -> Banker; hand 2 same -> Banker x 2
        entries = list(shoe_log(2, stacked_shoe([1, 7, 5, 1, 1, 7, 5, 1])))[:2]
        self.assertIn("Player Cards: A, 5", entries[0])
        self.assertIn("Big Road: Banker × 2", entries[1])
        self.assertIn("Bead Plate: Banker × 2", entries[1])
        self.assertIn("Shoe Totals: Banker 2 | Player 0 | Tie 0", entries[1])


if __name__ == "__main__":
    unittest.main()


class TestHandCsv(unittest.TestCase):
    def test_numbers_only_row(self):
        from baccarat.handlog import CSV_COLUMNS, shoe_csv_rows

        row = next(shoe_csv_rows(1, stacked_shoe([0, 8, 0, 2, 9, 9])))
        values = row.split(",")
        self.assertEqual(len(values), len(CSV_COLUMNS))
        for v in values:
            float(v)  # numbers only
        # P 0,0,9 = 9 ; B 8,2,9 = 9 ; tie ; totals 0/0/1 ; bead tie x1 ; no Big Road column, 1 tie
        self.assertEqual(",".join(values[:25]), "1,1,0,0,9,8,2,9,9,9,3,0,0,1,3,1,0,0,1,0,0,0,0,0,0")
        # before the first hand: a full shoe, 416 cards, fresh-shoe odds, Banker predicted, Banker best bet
        self.assertEqual(values[25:29], ["416", "128", "32", "32"])
        self.assertEqual(values[36:39], ["128", "128", "160"])
        self.assertEqual(values[39:44], ["45.8597", "44.6247", "9.5156", "1", "45.8597"])
        self.assertEqual(values[47], "1")

    def test_cards_left_counts_down(self):
        from baccarat.handlog import shoe_records

        recs = list(shoe_records(stacked_shoe([0, 8, 0, 2, 9, 9, 1, 7, 5, 1]), with_odds=False))[:2]
        self.assertEqual(sum(recs[0]["left"]), 416)
        self.assertEqual(sum(recs[1]["left"]), 410)  # six cards dealt in hand 1
        self.assertEqual(recs[1]["left"][9], 32 - 2)


class TestFastOdds(unittest.TestCase):
    def test_matches_python_enumeration(self):
        from baccarat.fastodds import probabilities
        from baccarat.game import Outcome, exact_probabilities

        c = [40, 10, 12, 9, 14, 11, 8, 13, 10, 12]
        slow = exact_probabilities(counts=c)
        fast = probabilities(c)
        self.assertAlmostEqual(fast[0], slow[Outcome.BANKER], places=12)
        self.assertAlmostEqual(fast[1], slow[Outcome.PLAYER], places=12)
        self.assertAlmostEqual(fast[2], slow[Outcome.TIE], places=12)

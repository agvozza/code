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
        self.assertEqual(lines[6:9], ["Visible board states", "Bead Plate: Tie × 1", "Big Road: — (tie)"])
        self.assertEqual(lines[9], "Big Eye Boy: — (not started)")

    def test_ace_and_streak(self):
        # hand 1: P 1,5 (6 stands) vs B 7,1 (8 natural) -> Banker; hand 2 same -> Banker x 2
        entries = list(shoe_log(2, stacked_shoe([1, 7, 5, 1, 1, 7, 5, 1])))[:2]
        self.assertIn("Player Cards: A, 5", entries[0])
        self.assertIn("Big Road: Banker × 2", entries[1])
        self.assertIn("Bead Plate: Banker × 2", entries[1])


if __name__ == "__main__":
    unittest.main()

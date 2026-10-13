# Numbers-only hand file: column key

One row per hand, 25 comma-separated integers, no letters. Files contain no header
line unless made with `--header`.

| # | column | values |
|---|---|---|
| 1 | shoe | shoe number (1-117,837) |
| 2 | hand | hand number within the shoe |
| 3-5 | p1, p2, p3 | Player cards in the order dealt: 0-9 (10/J/Q/K = 0, A = 1); -1 = no third card |
| 6-8 | b1, b2, b3 | Banker cards, same coding |
| 9 | p_total | Player total 0-9 |
| 10 | b_total | Banker total 0-9 |
| 11 | winner | 1 Banker, 2 Player, 3 Tie |
| 12 | banker_wins | Banker wins in the shoe so far, including this hand |
| 13 | player_wins | Player wins so far |
| 14 | ties | ties so far |
| 15 | bead_result | latest Bead Plate result: 1 Banker, 2 Player, 3 Tie |
| 16 | bead_run | how many times in a row that result has appeared |
| 17 | big_road_side | current Big Road column: 1 Banker, 2 Player, 0 none yet |
| 18 | big_road_run | length of that column |
| 19 | big_road_ties | ties marked on the column's newest cell |
| 20 | big_eye_color | Big Eye Boy current column: 1 Red, 2 Blue, 0 not started |
| 21 | big_eye_run | length of that column |
| 22 | small_color | Small Road, same coding |
| 23 | small_run | |
| 24 | cockroach_color | Cockroach Pig, same coding |
| 25 | cockroach_run | |

Example (shoe 1, hand 44):

```
1,44,5,0,1,0,7,-1,6,7,1,21,18,5,1,3,1,3,0,1,2,2,1,1,1
```

Player 5, 0, A = 6; Banker 0, 7 = 7; Banker wins. Shoe so far: Banker 21, Player 18,
Tie 5. Bead Plate Banker x3, Big Road Banker x3 with no tie, Big Eye Boy Red x2,
Small Road Blue x1, Cockroach Pig Red x1.

Build the files with:

```
python -m baccarat shoebank                     # once, about 5 minutes
python -m baccarat handcsv --max-mb 90          # writes hands-csv/hands-001.csv, ...
```

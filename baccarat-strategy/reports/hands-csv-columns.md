# Numbers-only hand file: column key

One row per hand, 48 comma-separated numbers, no letters. Files contain no header
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
| | **Columns 26-48 are counted before the hand is dealt** (what is known when the bet is placed) | |
| 26 | cards_left | cards still in the shoe (416 at the start; includes cards behind the cut card) |
| 27-36 | left_0 ... left_9 | how many of each value are left: 0 (10/J/Q/K), A, 2, ... 9 |
| 37 | zero_left | 10/J/Q/K left (of 128) |
| 38 | low_left | A-4 left (of 128) |
| 39 | high_left | 5-9 left (of 160) |
| 40 | p_banker | exact chance Banker wins this hand, % (4 decimals) |
| 41 | p_player | exact chance Player wins, % |
| 42 | p_tie | exact chance of a tie, % |
| 43 | predicted | most likely result: 1 Banker, 2 Player, 3 Tie |
| 44 | confidence | chance of that result, % |
| 45 | banker_value | average result of a $100 Banker bet (after 5% commission) |
| 46 | player_value | average result of a $100 Player bet |
| 47 | tie_value | average result of a $100 Tie bet (8:1) |
| 48 | best_bet | bet with the highest value: 1 Banker, 2 Player, 3 Tie |

Example (shoe 51690, hand 82, the last hand of the shoe):

```
51690,82,6,5,4,0,0,4,5,4,2,35,39,8,2,3,2,3,0,1,1,1,2,2,1,18,7,1,1,0,4,1,1,1,1,1,7,6,5,46.0833,45.6579,8.2588,1,46.0833,-1.8787,-0.4254,-25.6707,2
```

Player 6, 5, 4 = 5; Banker 0, 0, 4 = 4; Player wins. Shoe so far: Banker 35,
Player 39, Tie 8. Before the hand 18 cards were left (7 zero, 6 low, 5 high);
exact odds Banker 46.08%, Player 45.66%, Tie 8.26%; predicted Banker (46.08%);
best value bet Player (-$0.43 per $100).

Build the files with:

```
python -m baccarat shoebank                     # once, about 5 minutes
python -m baccarat handcsv --max-mb 90          # writes hands-csv/hands-001.csv, ...
```

## Banker streaks of 6+ (`banker-streaks-6plus-hands.csv`)

Every hand inside a run of 6 or more Banker wins in a row (ties inside a run do
not end it, as on the Big Road). Each row is the 25-column hand row above with
two numbers in front, so rows have 27 numbers:

| # | column | values |
|---|---|---|
| 1 | streak | run number, 1-69,079 (matches `banker-streaks-6plus.csv`) |
| 2 | streak_length | Banker wins in that run (6-22) |
| 3-27 | | the 25 hand columns above (shoe, hand, cards, ...) |

`banker-streaks-6plus.csv` has one labelled row per run: shoe, first and last
hand, Banker wins, ties inside, what ended it.

## Two lists: 6+ Banker runs split by the next decision

`streak6-next-banker.csv` / `streak6-next-player.csv` (and a small
`streak6-next-shoe-ended.csv`). One row for every Banker win that is the 6th or
later in its run, 78 numbers per row:

| # | column | values |
|---|---|---|
| 1 | run | run number (same numbering as `banker-streaks-6plus.csv`) |
| 2 | banker_wins_so_far | 6, 7, 8, ... |
| 3-50 | | the 48 hand columns above for that Banker win |
| 51 | next_hand | hand number of the next hand (0 = shoe ended) |
| 52 | next_hand_result | 1 Banker, 2 Player, 3 Tie, 0 none |
| 53 | ties_before_next_decision | ties between this hand and the next Banker/Player result |
| 54 | next_decision_hand | hand number of that next Banker/Player result |
| 55 | next_decision | 1 Banker (list "banker") or 2 Player (list "player") |
| 56-78 | next_... | columns 26-48 for the next hand: cards left, odds, prediction and bet values before it is dealt |

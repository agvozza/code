# Baccarat Betting Strategy

A Punto Banco (casino baccarat) simulator for testing betting strategies
against an accurate model of the game — 8-deck shoe, full third-card drawing
tableau, 5% Banker commission, 8:1 Tie.

Pure Python 3.10+, no dependencies.

## Quick start

```bash
python -m baccarat odds                       # exact probabilities & house edge
python -m baccarat simulate martingale --seed 1
python -m baccarat compare --seed 1           # every strategy, same settings
python -m baccarat cutoff martingale --side player --unit 2 --stop-win 50 --hands 70
                                              # best last hand to start a new cycle
python -m unittest                            # run tests
```

Session options (for `simulate` and `compare`):

| option | default | meaning |
|---|---|---|
| `--side` | `banker` | `banker`, `player`, `tie`, `follow` (bet last winner), `chop` (bet against last winner) |
| `--bankroll` | 1000 | starting money per session |
| `--unit` | 10 | base bet |
| `--hands` | 200 | max hands per session |
| `--table-max` | 5000 | table limit (`0` = none) |
| `--stop-win` / `--stop-loss` | — | leave the table at this profit / loss |
| `--one-shoe` | off | each session is exactly one shoe (ends at the cut card) |
| `--last-start N` | — | don't start a new betting cycle after hand N (a running cycle may finish) |
| `--sessions` | 2000 | sessions to simulate |
| `--seed` | — | for reproducible runs |

## Strategies

| name | rule |
|---|---|
| `flat` | 1 unit every hand (baseline) |
| `martingale` | double after a loss, reset after a win |
| `paroli` | double after a win, reset after a loss or 3 wins in a row |
| `fibonacci` | one step up the sequence on a loss, two back on a win |
| `dalembert` | +1 unit after a loss, −1 after a win |
| `1326` | 1-3-2-6 units through a winning streak |
| `labouchere` | cancellation line 1-2-3-4 |

Add your own by subclassing `Strategy` in `baccarat/strategies.py` and
registering it in `STRATEGIES`. Side-selection rules live in `SIDES`.

## What the numbers say

Exact odds off the top of an 8-deck shoe:

| bet | P(win) | house edge |
|---|---|---|
| Banker | 45.86% | 1.06% |
| Player | 44.62% | 1.24% |
| Tie | 9.52% | 14.36% |

Sample `compare --seed 1` (Banker, $1000 bankroll, $10 unit, 200 hands, 2000 sessions):

```
strategy      mean P/L   win %  bust %     worst   wagered  edge %
------------------------------------------------------------------
flat            -25.94    43.0     0.0      -571      2000    1.30
martingale      -80.53    50.9    41.9     -1000      5167    1.56
paroli          -48.84    41.9     0.0      -856      3437    1.42
fibonacci       -41.57    71.0    20.9     -1000      4148    1.00
dalembert      -112.52    53.1    38.4     -1000      8759    1.28
1326            -48.76    42.9     0.1      -996      4011    1.22
labouchere     -164.55    29.9    69.5     -1000     12204    1.35
```

Every hand is an independent bet with negative expectation, so **no staking
progression or pattern-following rule changes the house edge**. The realized
edge hovers around 1.06–1.24% for all of them (differences are sampling noise).
What progressions *do* change is the shape of the results: Martingale and
Fibonacci trade many small winning sessions for occasional total bankroll
wipe-outs, and because they put more money in action, the average loss per
session is larger than flat betting. The cheapest way to play is flat bets on
Banker with stop-loss limits.

## Layout

```
baccarat/
  game.py        shoe, drawing rules, exact odds
  strategies.py  stake progressions + side pickers
  simulator.py   session loop and statistics
  __main__.py    CLI
tests/
```

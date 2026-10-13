# 100 Player-only plans: 1000 simulated months

Each month is 30 days of 2-4 hours (70 hands/hour, fresh 8-deck shoe each hour). Every plan plays the same months. *bankroll* = money needed to survive 95% of months (5th-percentile low point). *good years* = share of 12-month stretches that ended ahead.

| # | plan | family | bets | rules | hit $500 | month > 0 | avg month | median | worst 10% | worst 1% | bankroll | good years | hrs/day |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | `goal-glide25` | F. $500 goal | 25-45-85-165-325-646 | stop month at +$500 | 91.1% | 91.1% | -749 | +509 | +500 | -21433 | 15243 | 36% | 0.4 |
| 2 | `goal-yours-a` | F. $500 goal | 10-30-70-140-280-560 | stop month at +$500 | 90.3% | 90.3% | -582 | +500 | +500 | -18300 | 12400 | 33% | 0.4 |
| 3 | `flat-100-m500` | D. Flat + limits | flat $100 | stop month at +$500 | 85.4% | 85.4% | -1495 | +500 | -9800 | -22600 | 17600 | 19% | 0.6 |
| 4 | `goal-grand5` | F. $500 goal | 5-15-35-75-155-315 | stop month at +$500 | 83.1% | 83.1% | -528 | +500 | -4275 | -10890 | 8485 | 30% | 0.8 |
| 5 | `goal-mart10` | F. $500 goal | Martingale 10-20-40-80-160-320 | stop month at +$500 | 82.6% | 82.6% | -633 | +500 | -4840 | -11650 | 8980 | 23% | 0.8 |
| 6 | `goal-oscar25` | F. $500 goal | Oscar's Grind $25 | stop month at +$500 | 82.4% | 82.4% | -1029 | +500 | -6425 | -16025 | 11950 | 16% | 0.7 |
| 7 | `goal-mart5` | F. $500 goal | Martingale 5-10-20-40-80-160-320 | stop month at +$500 | 77.0% | 77.3% | -574 | +500 | -4295 | -8595 | 7005 | 22% | 1.0 |
| 8 | `flat-50-m500` | D. Flat + limits | flat $50 | stop month at +$500 | 73.4% | 73.4% | -1336 | +500 | -7000 | -11950 | 10000 | 7% | 1.0 |
| 9 | `goal-fib10` | F. $500 goal | Fibonacci $10 x8 | stop month at +$500 | 69.3% | 69.7% | -729 | +500 | -4120 | -7770 | 6420 | 13% | 1.3 |
| 10 | `quota-grand5` | F. $500 goal | 5-15-35-75-155-315, $50-a-day quota | quit day at +$50; stop month at +$500 | 67.0% | 71.2% | -212 | +500 | -2135 | -5025 | 4190 | 30% | 0.2 |
| 11 | `goal-flat100` | F. $500 goal | flat $100 | stop month at +$500; stop month at -$1000 | 60.5% | 60.5% | -92 | +500 | -1000 | -1000 | 1000 | 24% | 0.0 |
| 12 | `flat-25-m500` | D. Flat + limits | flat $25 | stop month at +$500 | 54.2% | 54.7% | -1060 | +500 | -4025 | -6025 | 5275 | 2% | 1.7 |
| 13 | `quota-lab1234` | F. $500 goal | Labouchere 5-10-15-20, $25-a-day quota | quit day at +$25 | 38.6% | 50.5% | -433 | +20 | -3060 | -5510 | 4975 | 22% | 0.3 |
| 14 | `twostage-mart5` | F. $500 goal | Martingale 5-10-20-40-80-160, $25-a-day quota | quit day at +$25; stop month at +$500; stop month at -$1000 | 36.5% | 53.9% | -138 | +80 | -1050 | -1140 | 1090 | 28% | 0.3 |
| 15 | `grand-2+2` | A. Recovery + breaker | double +$2: 2-6-14-30-62-126-254-510 | - | 36.1% | 42.1% | -1044 | -910 | -5630 | -9982 | 8286 | 20% | 3.0 |
| 16 | `after-2B-grand5` | E. Pattern triggers | after 2 Banker wins, start 5-15-35-75-155-315 | - | 35.8% | 43.2% | -472 | -390 | -3165 | -5900 | 4760 | 30% | 3.0 |
| 17 | `yours-b-x5` | A. Recovery + breaker | your idea scaled x5: 5-15-35-75-150-300-600 | - | 32.9% | 36.4% | -2437 | -2340 | -10305 | -16245 | 14375 | 16% | 3.0 |
| 18 | `hybrid-5-3` | A. Recovery + breaker | +$5 profit for 3 steps then pure doubling: 5-15-35-70-140-280-560 | - | 32.2% | 36.0% | -2329 | -2225 | -9740 | -15270 | 13495 | 14% | 3.0 |
| 19 | `flat-100-d100/300` | D. Flat + limits | flat $100 | quit day at +$100; quit day at -$300 | 31.6% | 47.1% | -104 | -200 | -1400 | -2600 | 1900 | 34% | 0.0 |
| 20 | `hybrid-5-2` | A. Recovery + breaker | +$5 profit for 2 steps then pure doubling: 5-15-30-60-120-240-480 | - | 30.8% | 35.8% | -2065 | -2000 | -8485 | -13285 | 11645 | 13% | 3.0 |
| 21 | `glide-10` | A. Recovery + breaker | profit target starts $10 and shrinks: 10-18-34-66-130-259-518 | - | 30.1% | 33.5% | -2471 | -2214 | -9609 | -14703 | 12648 | 8% | 3.0 |
| 22 | `yours-a-x5` | A. Recovery + breaker | your idea scaled x5: 10-30-70-140-280-560 | - | 29.5% | 32.5% | -3703 | -3330 | -13910 | -22720 | 18720 | 4% | 3.0 |
| 23 | `mart-5x7` | A. Recovery + breaker | Martingale 5-10-20-40-80-160-320, then accept the loss | - | 28.6% | 34.7% | -1444 | -1350 | -5765 | -8930 | 7825 | 8% | 3.0 |
| 24 | `grand-5+5` | A. Recovery + breaker | double +$5: 5-15-35-75-155-315 | - | 28.4% | 33.5% | -1955 | -1725 | -7525 | -12405 | 10190 | 4% | 3.0 |
| 25 | `glide-25` | A. Recovery + breaker | profit target starts $25 and shrinks: 25-45-85-165-325-646 | - | 28.3% | 30.6% | -5080 | -4763 | -16855 | -27620 | 23010 | 2% | 3.0 |
| 26 | `mart-10x6` | A. Recovery + breaker | Martingale 10-20-40-80-160-320, then accept the loss | - | 26.6% | 31.3% | -2345 | -2210 | -8220 | -13450 | 10970 | 4% | 3.0 |
| 27 | `after-2B-mart5` | E. Pattern triggers | after 2 Banker wins, start Martingale 5-10-20-40-80-160 | - | 26.1% | 42.4% | -285 | -245 | -1745 | -3180 | 2550 | 24% | 3.0 |
| 28 | `quota-oscar10` | F. $500 goal | Oscar's Grind $10, $25-a-day quota | quit day at +$25 | 25.2% | 44.5% | -280 | -140 | -1560 | -3030 | 2460 | 13% | 0.4 |
| 29 | `half-10` | B. Slow recovery | $10 + half the cycle deficit | - | 25.0% | 29.2% | -2423 | -2124 | -8080 | -12496 | 10936 | 4% | 3.0 |
| 30 | `quota-paroli25` | F. $500 goal | Paroli $25 x3, $50-a-day quota | quit day at +$50; quit day at -$200 | 24.8% | 43.2% | -148 | -125 | -1325 | -2375 | 1825 | 34% | 0.2 |
| 31 | `third-10` | B. Slow recovery | $10 + a third of the cycle deficit | - | 24.7% | 29.3% | -2198 | -1919 | -7118 | -11484 | 9467 | 4% | 3.0 |
| 32 | `grand-10+10` | A. Recovery + breaker | double +$10: 10-30-70-150-310 | - | 24.7% | 26.8% | -3257 | -3160 | -10550 | -16230 | 14670 | 2% | 3.0 |
| 33 | `flat-50-d100/200` | D. Flat + limits | flat $50 | quit day at +$100; quit day at -$200 | 24.2% | 36.4% | -141 | +0 | -1200 | -2100 | 1650 | 24% | 0.1 |
| 34 | `fib-5x10` | B. Slow recovery | Fibonacci $5, give up after 10 steps | - | 23.9% | 33.1% | -1005 | -755 | -3940 | -6360 | 5355 | 5% | 3.0 |
| 35 | `mart-25x5` | A. Recovery + breaker | Martingale 25-50-100-200-400, then accept the loss | - | 23.4% | 25.1% | -5046 | -4900 | -14875 | -22800 | 20175 | 2% | 3.0 |
| 36 | `mart-5x6` | A. Recovery + breaker | Martingale 5-10-20-40-80-160, then accept the loss | - | 23.2% | 31.3% | -1172 | -1105 | -4110 | -6725 | 5485 | 4% | 3.0 |
| 37 | `glide-50` | A. Recovery + breaker | profit target starts $50 and shrinks: 50-90-170-330-650 | - | 23.2% | 24.2% | -8853 | -8210 | -25170 | -38230 | 33710 | 2% | 3.0 |
| 38 | `after-3B-mart5` | E. Pattern triggers | after 3 Banker wins, start Martingale 5-10-20-40-80-160 | - | 23.1% | 43.6% | -153 | -145 | -1210 | -2155 | 1765 | 29% | 3.0 |
| 39 | `fib-10x8` | B. Slow recovery | Fibonacci $10, give up after 8 steps | - | 22.2% | 28.9% | -1619 | -1660 | -5070 | -8060 | 7010 | 2% | 3.0 |
| 40 | `lab-22222` | B. Slow recovery | Labouchere line 10-10-10-10-10 ($5 units, reset above $250) | - | 21.2% | 24.2% | -3827 | -3870 | -9980 | -15350 | 13360 | 1% | 3.0 |
| 41 | `mart-25x4` | A. Recovery + breaker | Martingale 25-50-100-200, then accept the loss | - | 20.6% | 22.4% | -4119 | -4050 | -11200 | -16450 | 14375 | 0% | 3.0 |
| 42 | `lab-123` | B. Slow recovery | Labouchere line 5-10-15 ($5 units, reset above $250) | - | 20.5% | 23.7% | -3545 | -3515 | -9605 | -14700 | 12750 | 4% | 3.0 |
| 43 | `lab-1111` | B. Slow recovery | Labouchere line 5-5-5-5 ($5 units, reset above $250) | - | 20.2% | 25.2% | -2386 | -2250 | -6900 | -10745 | 9250 | 1% | 3.0 |
| 44 | `mart-10x5` | A. Recovery + breaker | Martingale 10-20-40-80-160, then accept the loss | - | 20.1% | 25.1% | -2018 | -1960 | -5950 | -9120 | 8070 | 2% | 3.0 |
| 45 | `half-5` | B. Slow recovery | $5 + half the cycle deficit | - | 19.7% | 28.6% | -1248 | -1079 | -4118 | -6486 | 5454 | 4% | 3.0 |
| 46 | `ladder-x5` | B. Slow recovery | ladder 15-25-40-60-90-135-200 (+1 rung on loss, -2 on win) | - | 19.1% | 23.8% | -2719 | -2585 | -7255 | -11270 | 10130 | 2% | 3.0 |
| 47 | `delayed-mart` | A. Recovery + breaker | 3 flat bets then double: 5-5-5-10-20-40-80-160 | - | 18.8% | 33.8% | -572 | -515 | -2175 | -3365 | 2925 | 5% | 3.0 |
| 48 | `oscar-25` | B. Slow recovery | Oscar's Grind $25, +$25 per series | - | 18.8% | 21.6% | -4237 | -4225 | -11200 | -17500 | 14725 | 2% | 3.0 |
| 49 | `lab-12345` | B. Slow recovery | Labouchere line 5-10-15-20-25 ($5 units, reset above $250) | - | 17.8% | 20.6% | -5023 | -5050 | -12605 | -20030 | 16190 | 1% | 3.0 |
| 50 | `flat-50-1hand-d50` | D. Flat + limits | flat $50, quit after one winning hand | quit day at +$50; quit day at -$150 | 17.6% | 47.1% | -52 | -100 | -700 | -1300 | 950 | 34% | 0.0 |
| 51 | `dalembert-25` | B. Slow recovery | d'Alembert $25 steps, reset above 10 units | - | 17.4% | 18.2% | -7521 | -7475 | -18425 | -28625 | 23725 | 0% | 3.0 |
| 52 | `flat-25-d50/200` | D. Flat + limits | flat $25 | quit day at +$50; quit day at -$200 | 17.0% | 29.1% | -181 | -250 | -1000 | -1500 | 1350 | 16% | 0.3 |
| 53 | `1326-25` | C. Press wins | 1-3-2-6 x $25 | - | 16.8% | 19.5% | -3925 | -4000 | -9625 | -13550 | 11850 | 0% | 3.0 |
| 54 | `mart-5x5` | A. Recovery + breaker | Martingale 5-10-20-40-80, then accept the loss | - | 16.7% | 25.1% | -1009 | -980 | -2975 | -4560 | 4035 | 2% | 3.0 |
| 55 | `contra-dal-25` | C. Press wins | contra d'Alembert $25: +1 unit on win, -1 on loss | - | 16.2% | 18.7% | -6353 | -6200 | -15600 | -22000 | 19625 | 0% | 3.0 |
| 56 | `late-shoe-25` | E. Pattern triggers | bet $25 only in the last 20 hands of each shoe | - | 16.1% | 30.6% | -518 | -525 | -1800 | -2700 | 2400 | 7% | 3.0 |
| 57 | `dalembert-down2` | B. Slow recovery | d'Alembert +1 on loss, -2 on win ($10) | - | 15.9% | 21.8% | -1899 | -1870 | -4880 | -7390 | 6450 | 1% | 3.0 |
| 58 | `oscar-10` | B. Slow recovery | Oscar's Grind $10, +$10 per series | - | 15.8% | 21.6% | -1695 | -1690 | -4480 | -7000 | 5890 | 2% | 3.0 |
| 59 | `fib-5x8` | B. Slow recovery | Fibonacci $5, give up after 8 steps | - | 15.7% | 28.9% | -809 | -830 | -2535 | -4030 | 3505 | 2% | 3.0 |
| 60 | `1324-25` | C. Press wins | 1-3-2-4 x $25 | - | 15.7% | 18.3% | -3668 | -3800 | -8675 | -12600 | 10725 | 0% | 3.0 |
| 61 | `parlay-5x5` | C. Press wins | $5 let ride 5 times (5-10-20-40-80) | - | 15.6% | 25.3% | -1011 | -1030 | -2940 | -4470 | 3735 | 2% | 3.0 |
| 62 | `after-2B-flat25` | E. Pattern triggers | bet $25 only after 2 Banker wins in a row | - | 15.5% | 31.6% | -486 | -450 | -1775 | -2650 | 2350 | 5% | 3.0 |
| 63 | `paroli-4-10` | C. Press wins | Paroli $10, let it ride 4 wins | - | 15.1% | 21.1% | -1663 | -1730 | -4390 | -5910 | 5460 | 0% | 3.0 |
| 64 | `dalembert-10` | B. Slow recovery | d'Alembert $10 steps, reset above 10 units | - | 15.1% | 18.2% | -3009 | -2990 | -7370 | -11450 | 9490 | 0% | 3.0 |
| 65 | `ride-PP-flat25` | E. Pattern triggers | bet $25 only after 2 Player wins | - | 15.0% | 28.8% | -475 | -475 | -1650 | -2625 | 2150 | 1% | 3.0 |
| 66 | `chop-PB-flat25` | E. Pattern triggers | bet $25 when the last two were Player then Banker | - | 14.7% | 29.6% | -459 | -475 | -1675 | -2575 | 2225 | 2% | 3.0 |
| 67 | `after-3B-flat25` | E. Pattern triggers | bet $25 only after 3 Banker wins in a row | - | 14.6% | 35.2% | -248 | -250 | -1175 | -1900 | 1600 | 10% | 3.0 |
| 68 | `paroli-3-25` | C. Press wins | Paroli $25, 3 wins | - | 14.6% | 18.3% | -3348 | -3375 | -8125 | -12150 | 10475 | 0% | 3.0 |
| 69 | `every-other-25` | E. Pattern triggers | bet $25 every other hand | - | 14.2% | 24.6% | -951 | -975 | -2600 | -3950 | 3350 | 2% | 3.0 |
| 70 | `dalembert-up2` | B. Slow recovery | d'Alembert +2 units on loss, -1 on win ($5) | - | 14.1% | 17.9% | -2786 | -2750 | -6885 | -9595 | 8710 | 0% | 3.0 |
| 71 | `house-50` | C. Press wins | $25 + 50% of today's profit | - | 14.1% | 14.7% | -3555 | -7046 | -9201 | -10823 | 9941 | 7% | 3.0 |
| 72 | `flat-100` | D. Flat + limits | flat $100 | - | 13.8% | 14.7% | -7799 | -7900 | -17600 | -24500 | 22200 | 0% | 3.0 |
| 73 | `flat-25-d100/200` | D. Flat + limits | flat $25 | quit day at +$100; quit day at -$200 | 13.5% | 25.3% | -368 | -300 | -1500 | -2100 | 1850 | 4% | 0.5 |
| 74 | `ride-P-flat25` | E. Pattern triggers | bet $25 only right after a Player win | - | 13.1% | 22.9% | -988 | -1025 | -2675 | -3975 | 3525 | 0% | 3.0 |
| 75 | `1326-10` | C. Press wins | 1-3-2-6 x $10 | - | 13.1% | 19.5% | -1570 | -1600 | -3850 | -5420 | 4740 | 0% | 3.0 |
| 76 | `contra-dal-10` | C. Press wins | contra d'Alembert $10: +1 unit on win, -1 on loss | - | 13.0% | 18.7% | -2541 | -2480 | -6240 | -8800 | 7850 | 0% | 3.0 |
| 77 | `after-3B-paroli10` | E. Pattern triggers | after 3 Banker wins, Paroli $10 x3 | - | 12.8% | 30.7% | -318 | -340 | -1200 | -1960 | 1620 | 8% | 3.0 |
| 78 | `cooloff-25` | E. Pattern triggers | flat $25, sit out one hand after every loss | - | 12.6% | 19.4% | -1360 | -1375 | -3300 | -5175 | 4450 | 0% | 3.0 |
| 79 | `dalembert-5` | B. Slow recovery | d'Alembert $5 steps, reset above 10 units | - | 12.6% | 18.2% | -1504 | -1495 | -3685 | -5725 | 4745 | 0% | 3.0 |
| 80 | `flat-50` | D. Flat + limits | flat $50 | - | 12.5% | 14.7% | -3900 | -3950 | -8800 | -12250 | 11100 | 0% | 3.0 |
| 81 | `early-shoe-25` | E. Pattern triggers | bet $25 only in the first 35 hands of each shoe | - | 12.1% | 21.4% | -1014 | -1000 | -2650 | -3950 | 3450 | 0% | 3.0 |
| 82 | `1235-10` | C. Press wins | 1-2-3-5 x $10 on wins | - | 11.8% | 18.0% | -1406 | -1460 | -3430 | -4710 | 4230 | 0% | 3.0 |
| 83 | `after-tie-flat25` | E. Pattern triggers | bet $25 only on the hand after a tie | - | 11.6% | 37.4% | -183 | -150 | -975 | -1675 | 1300 | 14% | 3.0 |
| 84 | `grow-1.5x` | A. Recovery + breaker | x1.5 growth, a win restarts: 5-8-12-18-27-41-62-93 | - | 11.5% | 24.8% | -731 | -653 | -2136 | -3287 | 2762 | 1% | 3.0 |
| 85 | `1324-10` | C. Press wins | 1-3-2-4 x $10 | - | 11.4% | 18.3% | -1467 | -1520 | -3470 | -5040 | 4290 | 0% | 3.0 |
| 86 | `oscar-5` | B. Slow recovery | Oscar's Grind $5, +$5 per series | - | 10.7% | 21.6% | -847 | -845 | -2240 | -3500 | 2945 | 2% | 3.0 |
| 87 | `house-25` | C. Press wins | $25 + 25% of today's profit | - | 10.7% | 11.3% | -3182 | -5582 | -7877 | -9637 | 8765 | 12% | 3.0 |
| 88 | `after-4B-flat25` | E. Pattern triggers | bet $25 only after 4 Banker wins in a row | - | 10.6% | 39.6% | -126 | -100 | -775 | -1300 | 1150 | 19% | 3.0 |
| 89 | `flat-25-d100/100` | D. Flat + limits | flat $25 | quit day at +$100; quit day at -$100 | 10.5% | 29.6% | -176 | -200 | -800 | -1400 | 1200 | 7% | 0.3 |
| 90 | `paroli-3-10` | C. Press wins | Paroli $10, let it ride 3 wins | - | 10.5% | 18.3% | -1339 | -1350 | -3250 | -4860 | 4190 | 0% | 3.0 |
| 91 | `flat-25` | D. Flat + limits | flat $25 | - | 9.9% | 14.7% | -1950 | -1975 | -4400 | -6125 | 5550 | 0% | 3.0 |
| 92 | `ladder-gentle` | B. Slow recovery | ladder 10-12-15-19-24-30-38-48 | - | 8.9% | 18.0% | -1100 | -1080 | -2559 | -3921 | 3386 | 0% | 3.0 |
| 93 | `hot-10-25` | C. Press wins | $10, jump to $25 after 2 straight wins until a loss | - | 8.4% | 17.7% | -1065 | -1055 | -2525 | -3600 | 3085 | 0% | 3.0 |
| 94 | `paroli-2-10` | C. Press wins | Paroli $10, let it ride 2 wins | - | 7.6% | 16.4% | -1046 | -1070 | -2370 | -3440 | 3010 | 0% | 3.0 |
| 95 | `quota-mart5` | F. $500 goal | Martingale 5-10-20-40-80-160, $25-a-day quota | quit day at +$25; quit day at -$300 | 7.2% | 54.0% | -78 | +75 | -595 | -1270 | 1045 | 28% | 0.2 |
| 96 | `double-every-2` | A. Recovery + breaker | raise only after every 2nd loss: 5-5-10-10-20-20-40-40-80-80 | - | 7.2% | 24.1% | -572 | -520 | -1610 | -2485 | 2100 | 2% | 3.0 |
| 97 | `flat-25-d50/100` | D. Flat + limits | flat $25 | quit day at +$50; quit day at -$100 | 5.8% | 36.4% | -70 | +0 | -600 | -1050 | 825 | 24% | 0.1 |
| 98 | `flat-10` | D. Flat + limits | flat $10 | - | 4.9% | 14.7% | -780 | -790 | -1760 | -2450 | 2220 | 0% | 3.0 |
| 99 | `quota-flat25` | F. $500 goal | flat $25, $25-a-day quota | quit day at +$25; quit day at -$150 | 3.7% | 49.0% | -64 | -125 | -475 | -1000 | 775 | 25% | 0.1 |
| 100 | `flat-25-d25` | D. Flat + limits | flat $25, hit-and-run | quit day at +$25; quit day at -$100 | 3.1% | 38.6% | -36 | +0 | -375 | -750 | 600 | 28% | 0.1 |

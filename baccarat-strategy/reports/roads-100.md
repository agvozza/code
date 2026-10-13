# Scoreboard-road strategies

## Signal accuracy (1000 months of hands, flat $1 on every hand the signal fires)

| signal | rule | bets | win % (ex. ties) | result per $100 bet | by confidence 1 / 2 / 3 (per $100) |
|---|---|---|---|---|---|
| `cockroach` | bet the side that makes the next Cockroach Pig mark red | 5,601,546 | 50.00% | -1.15 | -1.05 / -1.22 / -1.12 |
| `small` | bet the side that makes the next Small Road mark red | 5,800,542 | 50.02% | -1.14 | -1.07 / -1.20 / -1.12 |
| `bigeye` | bet the side that makes the next Big Eye Boy mark red | 5,999,490 | 50.00% | -1.16 | -1.08 / -1.24 / -1.12 |
| `allred` | bet only when one side turns all three derived roads red | 2,378,163 | 50.03% | -1.12 | - / - / -1.12 |
| `majority` | bet the side that turns at least 2 of 3 derived roads red | 5,725,027 | 49.99% | -1.18 | - / -1.22 / -1.12 |
| `cr-fade` | bet the side that makes the next Cockroach Pig mark blue | 5,601,546 | 50.00% | -1.15 | -1.25 / -1.07 / -1.17 |
| `cr-trend` | follow the Cockroach Pig's own recent colour trend | 3,252,788 | 50.03% | -1.10 | - / -1.11 / -1.06 |
| `dragon` | ride Big Road streaks of 2+ | 3,049,428 | 50.01% | -1.17 | -1.18 / -1.21 / -1.10 |
| `pingpong` | bet the alternation after 3+ chops | 1,500,765 | 50.04% | -1.05 | -1.06 / -1.15 / -0.95 |
| `mirror` | expect the current column to match the previous two columns' length | 1,978,793 | 50.01% | -1.11 | -1.11 / -0.99 / -1.13 |
| `banker` | control: always Banker, no signal | 6,298,180 | 50.68% | -1.06 | - / -1.06 / - |

## 100 signal plans: 1000 months, $10 base, stop month at +$500 or -$3,000, bets capped at $640

Compared with the same sizing rule betting Banker every hand with no signal (*vs Banker*).

| # | plan | hit $500 | avg month | vs Banker | worst 10% | good years | hrs/day |
|---|---|---|---|---|---|---|---|
| 1 | `majority/dalem` | 84.9% | -39 | -29 | -3100 | 45% | 0.0 |
| 2 | `pingpong/grand` | 82.9% | -66 | +41 | -3048 | 43% | 0.6 |
| 3 | `cockroach/dalem` | 84.1% | -71 | -61 | -3152 | 42% | 0.1 |
| 4 | `bigeye/dalem` | 83.8% | -84 | -74 | -3162 | 40% | 0.0 |
| 5 | `small/dalem` | 83.7% | -86 | -76 | -3152 | 43% | 0.0 |
| 6 | `cr-fade/cooldown` | 83.9% | -86 | +9 | -3084 | 36% | 0.3 |
| 7 | `cr-trend/dalem` | 83.4% | -99 | -89 | -3153 | 37% | 0.1 |
| 8 | `allred/dalem` | 83.2% | -101 | -90 | -3126 | 45% | 0.1 |
| 9 | `allred/grand` | 82.8% | -104 | +2 | -3054 | 34% | 0.4 |
| 10 | `mirror/dalem` | 82.9% | -111 | -101 | -3094 | 40% | 0.2 |
| 11 | `pingpong/strong` | 66.0% | -113 | +52 | -1840 | 39% | 1.6 |
| 12 | `pingpong/glide` | 82.6% | -116 | -2 | -3068 | 40% | 0.4 |
| 13 | `cr-fade/dalem` | 82.6% | -126 | -116 | -3160 | 36% | 0.1 |
| 14 | `allred/glide` | 82.3% | -128 | -13 | -3071 | 30% | 0.3 |
| 15 | `majority/confrec` | 82.7% | -131 | +42 | -3088 | 39% | 0.2 |
| 16 | `small/cooldown` | 82.1% | -138 | -42 | -3069 | 29% | 0.3 |
| 17 | `cr-trend/confrec` | 81.6% | -140 | +32 | -3086 | 34% | 0.5 |
| 18 | `mirror/glide` | 82.0% | -141 | -26 | -3085 | 37% | 0.3 |
| 19 | `mirror/grand` | 82.0% | -142 | -35 | -3097 | 40% | 0.4 |
| 20 | `pingpong/cooldown` | 66.9% | -144 | -49 | -2089 | 37% | 1.4 |
| 21 | `mirror/recover` | 81.2% | -146 | +19 | -3106 | 37% | 0.6 |
| 22 | `pingpong/recover` | 77.2% | -149 | +16 | -3032 | 36% | 0.9 |
| 23 | `mirror/strong` | 74.7% | -150 | +16 | -3019 | 45% | 1.1 |
| 24 | `majority/glide` | 81.7% | -154 | -40 | -3092 | 33% | 0.1 |
| 25 | `cr-trend/recover` | 81.5% | -156 | +9 | -3079 | 31% | 0.4 |
| 26 | `cr-trend/strong` | 81.5% | -156 | +9 | -3079 | 31% | 0.4 |
| 27 | `pingpong/fib` | 67.5% | -159 | +13 | -2456 | 39% | 1.5 |
| 28 | `bigeye/cooldown` | 81.3% | -167 | -71 | -3073 | 33% | 0.4 |
| 29 | `cr-fade/grand` | 81.3% | -167 | -61 | -3086 | 30% | 0.1 |
| 30 | `small/glide` | 81.3% | -167 | -53 | -3076 | 28% | 0.1 |
| 31 | `cr-trend/cooldown` | 77.1% | -168 | -73 | -3035 | 39% | 0.9 |
| 32 | `cr-fade/confrec` | 81.5% | -173 | -0 | -3094 | 27% | 0.3 |
| 33 | `mirror/confrec` | 78.1% | -175 | -3 | -3081 | 31% | 0.8 |
| 34 | `bigeye/confrec` | 81.4% | -176 | -3 | -3108 | 31% | 0.2 |
| 35 | `pingpong/confrec` | 70.3% | -177 | -5 | -3030 | 31% | 1.4 |
| 36 | `cr-trend/grand` | 81.0% | -178 | -71 | -3086 | 31% | 0.3 |
| 37 | `dragon/dalem` | 81.0% | -178 | -168 | -3112 | 30% | 0.2 |
| 38 | `cr-fade/glide` | 81.0% | -179 | -64 | -3086 | 31% | 0.1 |
| 39 | `mirror/fib` | 75.5% | -180 | -8 | -3058 | 34% | 1.0 |
| 40 | `bigeye/grand` | 80.8% | -181 | -75 | -3075 | 34% | 0.2 |
| 41 | `dragon/grand` | 80.7% | -182 | -75 | -3075 | 34% | 0.4 |
| 42 | `cockroach/grand` | 80.8% | -183 | -77 | -3088 | 31% | 0.2 |
| 43 | `allred/recover` | 79.4% | -184 | -19 | -3077 | 35% | 0.6 |
| 44 | `allred/confrec` | 79.4% | -184 | -12 | -3077 | 35% | 0.6 |
| 45 | `allred/strong` | 79.4% | -184 | -19 | -3077 | 35% | 0.6 |
| 46 | `allred/cooldown` | 79.4% | -184 | -88 | -3077 | 35% | 0.6 |
| 47 | `majority/grand` | 80.7% | -187 | -80 | -3090 | 35% | 0.2 |
| 48 | `cr-trend/glide` | 80.7% | -191 | -76 | -3103 | 31% | 0.2 |
| 49 | `small/confrec` | 80.9% | -193 | -20 | -3098 | 28% | 0.2 |
| 50 | `cockroach/confrec` | 80.9% | -193 | -20 | -3090 | 31% | 0.3 |
| 51 | `majority/cooldown` | 80.6% | -194 | -98 | -3091 | 27% | 0.3 |
| 52 | `small/fib` | 80.7% | -196 | -24 | -3112 | 31% | 0.4 |
| 53 | `small/strong` | 80.6% | -197 | -32 | -3100 | 30% | 0.3 |
| 54 | `bigeye/glide` | 80.5% | -197 | -83 | -3084 | 33% | 0.1 |
| 55 | `cockroach/glide` | 80.4% | -199 | -84 | -3081 | 29% | 0.1 |
| 56 | `cockroach/recover` | 80.6% | -199 | -34 | -3089 | 33% | 0.3 |
| 57 | `bigeye/fib` | 80.6% | -201 | -30 | -3118 | 28% | 0.4 |
| 58 | `cr-fade/fib` | 80.6% | -204 | -32 | -3119 | 35% | 0.3 |
| 59 | `dragon/strong` | 74.1% | -204 | -39 | -3033 | 36% | 1.0 |
| 60 | `cockroach/fib` | 80.4% | -205 | -33 | -3113 | 25% | 0.4 |
| 61 | `cockroach/strong` | 80.2% | -206 | -41 | -3081 | 28% | 0.4 |
| 62 | `bigeye/recover` | 80.2% | -206 | -41 | -3068 | 27% | 0.2 |
| 63 | `mirror/half` | 75.7% | -207 | -28 | -3063 | 30% | 0.9 |
| 64 | `pingpong/flatconf` | 35.5% | -207 | +509 | -1136 | 13% | 2.4 |
| 65 | `small/grand` | 80.1% | -210 | -103 | -3091 | 23% | 0.2 |
| 66 | `dragon/cooldown` | 76.7% | -210 | -114 | -3058 | 35% | 0.8 |
| 67 | `cr-fade/strong` | 80.4% | -211 | -45 | -3105 | 25% | 0.3 |
| 68 | `pingpong/half` | 68.6% | -211 | -33 | -3023 | 31% | 1.4 |
| 69 | `majority/half` | 80.4% | -213 | -35 | -3104 | 22% | 0.3 |
| 70 | `allred/fib` | 78.3% | -216 | -44 | -3090 | 27% | 0.7 |
| 71 | `dragon/recover` | 79.3% | -219 | -54 | -3086 | 31% | 0.5 |
| 72 | `bigeye/strong` | 79.9% | -219 | -54 | -3083 | 22% | 0.3 |
| 73 | `bigeye/half` | 79.9% | -229 | -51 | -3111 | 28% | 0.3 |
| 74 | `dragon/glide` | 79.6% | -229 | -115 | -3099 | 23% | 0.2 |
| 75 | `small/half` | 79.7% | -237 | -58 | -3096 | 25% | 0.3 |
| 76 | `cockroach/cooldown` | 79.3% | -239 | -143 | -3085 | 27% | 0.4 |
| 77 | `cr-trend/fib` | 77.8% | -243 | -72 | -3105 | 28% | 0.7 |
| 78 | `cr-fade/recover` | 79.4% | -246 | -80 | -3100 | 25% | 0.3 |
| 79 | `mirror/cooldown` | 75.7% | -246 | -151 | -3055 | 30% | 0.9 |
| 80 | `cr-trend/half` | 78.7% | -248 | -69 | -3112 | 23% | 0.6 |
| 81 | `pingpong/dalem` | 75.5% | -251 | -241 | -3055 | 24% | 0.8 |
| 82 | `allred/half` | 75.5% | -252 | -74 | -3086 | 25% | 0.8 |
| 83 | `majority/recover` | 78.9% | -252 | -87 | -3069 | 28% | 0.3 |
| 84 | `majority/strong` | 78.9% | -252 | -87 | -3069 | 28% | 0.3 |
| 85 | `majority/fib` | 79.1% | -253 | -81 | -3112 | 23% | 0.4 |
| 86 | `dragon/confrec` | 78.3% | -255 | -83 | -3145 | 20% | 0.6 |
| 87 | `cockroach/half` | 79.1% | -258 | -80 | -3110 | 24% | 0.3 |
| 88 | `dragon/half` | 77.5% | -272 | -93 | -3106 | 22% | 0.6 |
| 89 | `cr-fade/half` | 78.7% | -273 | -95 | -3110 | 30% | 0.3 |
| 90 | `small/recover` | 78.2% | -283 | -118 | -3096 | 27% | 0.3 |
| 91 | `dragon/fib` | 73.2% | -326 | -154 | -3114 | 20% | 0.8 |
| 92 | `mirror/flatconf` | 45.4% | -344 | +372 | -1708 | 11% | 2.1 |
| 93 | `dragon/flatconf` | 43.5% | -422 | +294 | -1840 | 6% | 2.1 |
| 94 | `allred/flatconf` | 55.2% | -427 | +289 | -2452 | 14% | 1.7 |
| 95 | `cr-trend/flatconf` | 48.1% | -495 | +221 | -2270 | 6% | 1.9 |
| 96 | `bigeye/flatconf` | 55.6% | -695 | +22 | -3009 | 1% | 1.4 |
| 97 | `cockroach/flatconf` | 54.7% | -707 | +9 | -3009 | 6% | 1.5 |
| 98 | `small/flatconf` | 53.6% | -722 | -6 | -3008 | 6% | 1.5 |
| 99 | `cr-fade/flatconf` | 53.1% | -725 | -9 | -3012 | 7% | 1.5 |
| 100 | `majority/flatconf` | 53.1% | -782 | -65 | -3011 | 4% | 1.4 |

### Banker-only controls

| sizing | rule | hit $500 | avg month | worst 10% | good years |
|---|---|---|---|---|---|
| `recover` | win back the cycle + 1 unit (Martingale-style) | 81.5% | -165 | -3078 | 34% |
| `confrec` | recover all/half/third of the deficit for confidence 3/2/1 | 81.5% | -173 | -3105 | 34% |
| `half` | 1 unit + half the deficit | 81.2% | -178 | -3092 | 33% |
| `grand` | win back the cycle + 1 unit per hand played | 83.0% | -107 | -3084 | 36% |
| `strong` | recovery bets only on confidence 2+, otherwise wait | 81.5% | -165 | -3078 | 34% |
| `fib` | Fibonacci, a rung higher on confidence 3 | 81.2% | -172 | -3092 | 31% |
| `dalem` | d'Alembert, step up by the confidence that lost | 85.8% | -10 | -3114 | 49% |
| `cooldown` | Martingale; after 3 losses wait for a confidence-3 signal | 22.9% | -96 | -640 | 20% |
| `glide` | recover + 3/2/1-unit target as losses mount | 82.8% | -115 | -3075 | 40% |
| `flatconf` | flat 1-3 units by confidence, no progression | 50.3% | -716 | -3006 | 4% |

*The `cooldown` control never produces a confidence-3 signal, so it stops for the day after 3 losses; compare `cooldown` plans with `recover` instead.*

### Signals

- `cockroach`: bet the side that makes the next Cockroach Pig mark red
- `small`: bet the side that makes the next Small Road mark red
- `bigeye`: bet the side that makes the next Big Eye Boy mark red
- `allred`: bet only when one side turns all three derived roads red
- `majority`: bet the side that turns at least 2 of 3 derived roads red
- `cr-fade`: bet the side that makes the next Cockroach Pig mark blue
- `cr-trend`: follow the Cockroach Pig's own recent colour trend
- `dragon`: ride Big Road streaks of 2+
- `pingpong`: bet the alternation after 3+ chops
- `mirror`: expect the current column to match the previous two columns' length

"""Perfect card tracking: exact odds of the next hand from the cards left in the shoe."""

from __future__ import annotations

from .game import BANKER_PAYOUT, TIE_PAYOUT, Outcome, Shoe, banker_draws, card_counts, deal_hand

_PAIRS = [(a, b) for a in range(10) for b in range(a, 10)]


def probabilities(counts: list[int]) -> tuple[float, float, float]:
    """Exact (banker, player, tie) probabilities for the next hand dealt from ``counts``.

    Card order within each two-card hand doesn't affect totals, so unordered pairs are
    enumerated with a weight of 2 for mixed pairs.
    """
    c = list(counts)
    n = sum(c)
    pb = pp = pt = 0.0
    for a, b in _PAIRS:
        wa = c[a]
        c[a] -= 1
        wb = c[b]
        c[b] -= 1
        if wa > 0 and wb > 0:
            w_player = wa * wb * (1 if a == b else 2)
            ptot = (a + b) % 10
            for x, y in _PAIRS:
                wx = c[x]
                c[x] -= 1
                wy = c[y]
                c[y] -= 1
                if wx > 0 and wy > 0:
                    w = w_player * wx * wy * (1 if x == y else 2)
                    btot = (x + y) % 10
                    m = n - 4
                    if ptot >= 8 or btot >= 8:
                        res = ((btot > ptot, ptot > btot, ptot == btot),)
                        probs = ((1.0, res[0]),)
                    else:
                        probs = _third_cards(c, m, ptot, btot)
                    for q, (bw, pw, tw) in probs:
                        if bw:
                            pb += w * q
                        elif pw:
                            pp += w * q
                        else:
                            pt += w * q
                c[x] += 1
                c[y] += 1
        c[a] += 1
        c[b] += 1
    total = pb + pp + pt
    return pb / total, pp / total, pt / total


def _settle(p, b):
    return (b > p, p > b, p == b)


def _third_cards(c, m, ptot, btot):
    out = []
    if ptot >= 6:  # player stands
        if banker_draws(btot, None):
            for v in range(10):
                if c[v]:
                    out.append((c[v] / m, _settle(ptot, (btot + v) % 10)))
        else:
            out.append((1.0, _settle(ptot, btot)))
        return out
    for p3 in range(10):
        if not c[p3]:
            continue
        q = c[p3] / m
        pt3 = (ptot + p3) % 10
        if banker_draws(btot, p3):
            c[p3] -= 1
            for v in range(10):
                if c[v]:
                    out.append((q * c[v] / (m - 1), _settle(pt3, (btot + v) % 10)))
            c[p3] += 1
        else:
            out.append((q, _settle(pt3, btot)))
    return out


def edges(counts: list[int]) -> dict[Outcome, float]:
    """Player's expected return per $1 for each bet (positive = player advantage)."""
    b, p, t = probabilities(counts)
    return {
        Outcome.BANKER: BANKER_PAYOUT * b - p,
        Outcome.PLAYER: p - b,
        Outcome.TIE: TIE_PAYOUT * t - (b + p),
    }


class TrackedShoe(Shoe):
    """A shoe that remembers how many of each card value are left."""

    def shuffle(self):
        super().shuffle()
        self.remaining = card_counts(self.decks)

    def draw(self):
        v = super().draw()
        self.remaining[v] -= 1
        return v


def play_shoe(rng, burn: int = 0):
    """Deal one shoe to the cut card; yield (hand number, edges before the hand, outcome)."""
    shoe = TrackedShoe(rng=rng)
    for _ in range(burn):
        shoe.draw()
    i = 0
    while not shoe.needs_shuffle():
        e = edges(shoe.remaining)
        hand = deal_hand(shoe)
        i += 1
        yield i, e, hand.outcome


# --- experiment ------------------------------------------------------------------

def _track(seed: int):
    import random

    rng = random.Random(seed)
    rows = []
    for i, e, outcome in play_shoe(rng):
        rows.append((seed, i, e[Outcome.BANKER], e[Outcome.PLAYER], e[Outcome.TIE], outcome.value[0]))
    return rows


def track_shoes(n: int, seed: int = 1, workers: int | None = None) -> list[tuple]:
    """Exact edges before every hand of ``n`` shoes: (shoe, hand, banker, player, tie, outcome)."""
    from concurrent.futures import ProcessPoolExecutor

    with ProcessPoolExecutor(workers) as ex:
        return [row for rows in ex.map(_track, range(seed * 100_000, seed * 100_000 + n)) for row in rows]


PAY = {"banker": 0.95, "player": 1.0, "tie": 8.0}
BETS = ("banker", "player", "tie")


def report(rows: list[tuple], last_hand: int | None = None, bet: float = 100,
           shoes_per_month: float = 78) -> str:
    """Summarize tracked shoes. ``last_hand`` truncates each shoe (an earlier cut card)."""
    recs = [dict(zip(("shoe", "hand", "banker", "player", "tie", "outcome"), r)) for r in rows]
    if last_hand:
        recs = [r for r in recs if r["hand"] <= last_hand]
    shoes = len({r["shoe"] for r in recs})
    n = len(recs)
    out = [f"{shoes} shoes, {n:,} hands ({n / shoes:.1f} per shoe)\n",
           "| bet | hands where it has the edge | avg edge then | best edge seen |", "|---|---|---|---|"]
    for k in BETS:
        pos = [r[k] for r in recs if r[k] > 0]
        avg = 100 * sum(pos) / len(pos) if pos else 0.0
        out.append(f"| {k} | {100 * len(pos) / n:.3f}% ({len(pos) / shoes:.2f} per shoe) | {avg:+.2f}% | "
                   f"{100 * max(r[k] for r in recs):+.2f}% |")
    out += ["", "| hands into the shoe | some bet has the edge |", "|---|---|"]
    for lo, hi in ((1, 40), (41, 60), (61, 70), (71, 75), (76, 80), (81, 99)):
        sub = [r for r in recs if lo <= r["hand"] <= hi]
        if sub:
            share = sum(max(r[k] for k in BETS) > 0 for r in sub) / len(sub)
            out.append(f"| {lo}-{hi} | {100 * share:.2f}% |")
    out += ["", f"Perfect counter: sit out unless a bet has at least the minimum edge, then bet ${bet:g} on it.",
            f"Monthly figures assume {shoes_per_month:g} shoes a month.\n",
            "| min edge | bets per shoe | expected $/shoe | expected $/month | actual $/shoe in this sample "
            "| flat bet needed for +$500/month |", "|---|---|---|---|---|---|"]
    for th in (0.0, 0.01, 0.02, 0.05):
        exp = act = bets = 0
        for r in recs:
            k = max(BETS, key=lambda k: r[k])
            if r[k] > th:
                bets += 1
                exp += bet * r[k]
                o = r["outcome"]
                if o == k[0]:
                    act += bet * PAY[k]
                elif not (o == "t" and k != "tie"):
                    act -= bet
        month = exp / shoes * shoes_per_month
        need = f"${bet * 500 / month:,.0f}" if month > 0 else "-"
        out.append(f"| {100 * th:.0f}% | {bets / shoes:.2f} | {exp / shoes:+.2f} | {month:+.2f} | "
                   f"{act / shoes:+.2f} | {need} |")
    return "\n".join(out)

"""Build a self-contained HTML viewer for a range of shoes (scoreboard + hand log)."""

from __future__ import annotations

import json
import random

from .game import Outcome, Shoe, deal_hand
from .handlog import board_lines, face
from .roads import RED, Board

CODE = {Outcome.PLAYER: "P", Outcome.BANKER: "B", Outcome.TIE: "T"}


def shoe_data(cards, last_hand=None):
    """Per hand: [player cards, banker cards, ptotal, btotal, winner, new road marks, board lines]."""
    shoe = Shoe(rng=random.Random(0))
    shoe._cards = list(cards)
    board = Board()
    ties = 0
    hands = []
    while not shoe.needs_shuffle() and (last_hand is None or len(hands) < last_hand):
        h = deal_hand(shoe)
        before = {k: len(v) for k, v in board.roads.items()}
        board.add(h.outcome)
        ties = ties + 1 if h.outcome is Outcome.TIE else 0
        marks = "".join(
            ("r" if board.roads[k][-1] == RED else "b") if len(board.roads[k]) > before[k] else "-"
            for k in ("big_eye", "small", "cockroach")
        )
        hands.append([
            " ".join(face(v) for v in h.player_cards), " ".join(face(v) for v in h.banker_cards),
            h.player_total, h.banker_total, CODE[h.outcome], marks, board_lines(board, ties),
        ])
    return hands


def build(shoes, start: int, end: int, last_hand=None) -> str:
    data = {str(n): shoe_data(shoes[n - 1], last_hand) for n in range(start, end + 1)}
    return TEMPLATE.replace("/*DATA*/null", json.dumps(data, separators=(",", ":"), ensure_ascii=False))


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Baccarat Shoe Viewer</title>
<style>
:root {
  --bg: #f6f5f1; --panel: #ffffff; --ink: #1d1d1f; --muted: #6b6b70; --line: #e2e0da; --grid: #ece9e2;
  --banker: #c8312b; --player: #2457c5; --tie: #1f8a4c; --accent: #1d1d1f; --chip: #f0eee8;
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --bg: #121214; --panel: #1b1b1f; --ink: #ececef; --muted: #9a9aa2; --line: #2c2c33; --grid: #26262c;
    --banker: #ef5b52; --player: #5b8cf0; --tie: #3fbf74; --accent: #ececef; --chip: #26262c;
  }
}
:root[data-theme="dark"] {
  --bg: #121214; --panel: #1b1b1f; --ink: #ececef; --muted: #9a9aa2; --line: #2c2c33; --grid: #26262c;
  --banker: #ef5b52; --player: #5b8cf0; --tie: #3fbf74; --accent: #ececef; --chip: #26262c;
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--ink);
  font: 15px/1.45 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
main { max-width: 1100px; margin: 0 auto; padding: 20px 16px 48px; }
h1 { font-size: 20px; margin: 0 0 4px; }
.sub { color: var(--muted); margin: 0 0 16px; font-size: 13px; }
.controls { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; background: var(--panel);
  border: 1px solid var(--line); border-radius: 12px; padding: 10px 12px; margin-bottom: 14px; }
.controls label { font-size: 13px; color: var(--muted); }
select, button { font: inherit; color: var(--ink); background: var(--chip); border: 1px solid var(--line);
  border-radius: 8px; padding: 6px 10px; cursor: pointer; }
button:hover, select:hover { border-color: var(--muted); }
input[type=range] { flex: 1 1 180px; accent-color: var(--accent); }
.pos { font-variant-numeric: tabular-nums; min-width: 92px; text-align: right; font-size: 13px; color: var(--muted); }
.layout { display: grid; grid-template-columns: 300px 1fr; gap: 14px; }
@media (max-width: 760px) { .layout { grid-template-columns: 1fr; } }
.card { background: var(--panel); border: 1px solid var(--line); border-radius: 12px; padding: 14px; min-width: 0; }
.card h2 { font-size: 13px; text-transform: uppercase; letter-spacing: .06em; color: var(--muted); margin: 0 0 8px; }
pre { margin: 0; font: 13px/1.6 ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; white-space: pre-wrap; }
.winner { display: inline-block; font-weight: 600; padding: 2px 10px; border-radius: 999px; color: #fff; margin-bottom: 10px; }
.w-B { background: var(--banker); } .w-P { background: var(--player); } .w-T { background: var(--tie); }
.hands { display: flex; gap: 10px; margin-bottom: 10px; }
.hands div { flex: 1; background: var(--chip); border-radius: 10px; padding: 8px 10px; }
.hands b { display: block; font-size: 12px; color: var(--muted); font-weight: 500; }
.hands span { font-size: 22px; font-weight: 600; font-variant-numeric: tabular-nums; }
.hands small { color: var(--muted); font-size: 13px; margin-left: 6px; }
.roads { display: grid; gap: 12px; }
.road h3 { font-size: 12px; margin: 0 0 4px; color: var(--muted); font-weight: 600; }
.scroll { overflow-x: auto; border: 1px solid var(--line); border-radius: 8px; background: var(--panel); }
svg { display: block; }
.stats { display: flex; gap: 14px; flex-wrap: wrap; font-size: 13px; color: var(--muted); margin-top: 10px; }
.stats b { color: var(--ink); }
.keys { font-size: 12px; color: var(--muted); margin-top: 10px; }
</style>
</head>
<body>
<main>
  <h1>Baccarat Shoe Viewer</h1>
  <p class="sub">Step through each shoe hand by hand. Cards are shown by baccarat value (10, J, Q, K = 0). Banker red, Player blue, Tie green.</p>
  <div class="controls">
    <label for="shoe">Shoe</label>
    <select id="shoe"></select>
    <button id="first" title="First hand">⏮</button>
    <button id="prev" title="Previous hand (←)">◀</button>
    <button id="play" title="Play / pause (space)">▶ Play</button>
    <button id="next" title="Next hand (→)">▶</button>
    <button id="last" title="Last hand">⏭</button>
    <input type="range" id="slider" min="1" value="1" aria-label="Hand">
    <span class="pos" id="pos"></span>
  </div>
  <div class="layout">
    <section class="card">
      <h2>This hand</h2>
      <div id="winner" class="winner"></div>
      <div class="hands">
        <div><b>Player</b><span id="pt"></span><small id="pc"></small></div>
        <div><b>Banker</b><span id="bt"></span><small id="bc"></small></div>
      </div>
      <pre id="log"></pre>
      <div class="stats" id="stats"></div>
      <div class="keys">Keys: ← → step, space play, Home / End</div>
    </section>
    <section class="card roads">
      <div class="road"><h3>Bead Plate</h3><div class="scroll" id="bead"></div></div>
      <div class="road"><h3>Big Road</h3><div class="scroll" id="big"></div></div>
      <div class="road"><h3>Big Eye Boy</h3><div class="scroll" id="r0"></div></div>
      <div class="road"><h3>Small Road</h3><div class="scroll" id="r1"></div></div>
      <div class="road"><h3>Cockroach Pig</h3><div class="scroll" id="r2"></div></div>
    </section>
  </div>
</main>
<script>
const DATA = /*DATA*/null;
const shoes = Object.keys(DATA);
const $ = id => document.getElementById(id);
const NAME = {P: "Player", B: "Banker", T: "Tie"};
let shoe = shoes[0], hand = 1, timer = null;

for (const s of shoes) {
  const o = document.createElement("option");
  o.value = s; o.textContent = `${String(s).padStart(6, "0")} (${DATA[s].length} hands)`;
  $("shoe").appendChild(o);
}

// Place a sequence of [key, value] into a 6-row grid: new column when key changes,
// and when a column runs out of room it turns right (a "dragon tail").
function place(seq) {
  const cells = [], used = new Set();
  let col = -1, row = 0, logical = -1, tailCol = 0, prev = null;
  for (const [key, val, ties] of seq) {
    if (key !== prev) {
      logical += 1; col = logical; row = 0;
      while (used.has(col + ",0")) col += 1;  // a tail may already occupy this column's top
      logical = col; tailCol = col;
    } else if (row < 5 && !used.has(tailCol + "," + (row + 1)) && tailCol === col) {
      row += 1;
    } else {
      tailCol += 1;  // move right along the current row
    }
    const c = key === prev ? tailCol : col;
    used.add(c + "," + row);
    cells.push({c, r: row, key, val, ties});
    prev = key;
  }
  return cells;
}

function svgGrid(cells, cols, size, draw) {
  const css = getComputedStyle(document.documentElement);
  const grid = css.getPropertyValue("--grid").trim();
  const w = Math.max(cols, 1) * size, h = 6 * size;
  let s = `<svg width="${w}" height="${h}" viewBox="0 0 ${w} ${h}" role="img">`;
  for (let x = 0; x <= w; x += size) s += `<line x1="${x}" y1="0" x2="${x}" y2="${h}" stroke="${grid}"/>`;
  for (let y = 0; y <= h; y += size) s += `<line x1="0" y1="${y}" x2="${w}" y2="${y}" stroke="${grid}"/>`;
  for (const cell of cells) s += draw(cell, size);
  return s + "</svg>";
}

const COLOR = k => `var(--${k === "B" || k === "r" ? "banker" : k === "P" || k === "b" ? "player" : "tie"})`;

function render() {
  const hands = DATA[shoe], h = hands[hand - 1];
  const [pc, bc, pt, bt, w, , lines] = h;
  $("slider").max = hands.length; $("slider").value = hand;
  $("pos").textContent = `Hand ${hand} / ${hands.length}`;
  $("winner").className = "winner w-" + w; $("winner").textContent = NAME[w] + (w === "T" ? "" : " wins");
  $("pt").textContent = pt; $("bt").textContent = bt; $("pc").textContent = pc; $("bc").textContent = bc;
  $("log").textContent = [
    `Shoe ${String(shoe).padStart(6, "0")} | Hand ${String(hand).padStart(3, "0")}`,
    `Player Cards: ${pc.split(" ").join(", ")}`, `Banker Cards: ${bc.split(" ").join(", ")}`,
    `Player Total: ${pt}`, `Banker Total: ${bt}`, `Winner: ${NAME[w]}`, "Visible board states", ...lines,
  ].join("\n");

  const shown = hands.slice(0, hand);
  const n = {P: 0, B: 0, T: 0}; shown.forEach(x => n[x[4]]++);
  $("stats").innerHTML = `<span>Banker <b>${n.B}</b></span><span>Player <b>${n.P}</b></span><span>Tie <b>${n.T}</b></span>`;

  // Bead plate: 6 rows, column by column, every result including ties
  const bs = 26, beadCols = Math.max(12, Math.ceil(hands.length / 6));
  const bead = shown.map((x, i) => ({c: Math.floor(i / 6), r: i % 6, key: x[4], cur: i === hand - 1}));
  $("bead").innerHTML = svgGrid(bead, beadCols, bs, (c, s) =>
    `<circle cx="${c.c * s + s / 2}" cy="${c.r * s + s / 2}" r="${s / 2 - 3}" fill="${COLOR(c.key)}"` +
    (c.cur ? ` stroke="var(--ink)" stroke-width="2"` : "") + `/>` +
    `<text x="${c.c * s + s / 2}" y="${c.r * s + s / 2 + 4}" text-anchor="middle" font-size="11" fill="#fff" font-weight="600">${c.key}</text>`);

  // Big road: ties are marked with a green slash on the latest cell
  const seq = []; let leadTies = 0;
  for (const x of shown) {
    if (x[4] === "T") { if (seq.length) seq[seq.length - 1][2] += 1; else leadTies += 1; }
    else seq.push([x[4], null, 0]);
  }
  const big = place(seq), bigCols = Math.max(20, ...big.map(c => c.c + 2));
  const s2 = 22;
  $("big").innerHTML = svgGrid(big, bigCols, s2, (c, s) => {
    const cx = c.c * s + s / 2, cy = c.r * s + s / 2;
    let o = `<circle cx="${cx}" cy="${cy}" r="${s / 2 - 4}" fill="none" stroke="${COLOR(c.key)}" stroke-width="3"/>`;
    if (c.ties) o += `<line x1="${cx - 6}" y1="${cy + 6}" x2="${cx + 6}" y2="${cy - 6}" stroke="var(--tie)" stroke-width="2.5"/>` +
      (c.ties > 1 ? `<text x="${cx + 7}" y="${cy - 3}" font-size="9" fill="var(--tie)" font-weight="700">${c.ties}</text>` : "");
    return o;
  }) ;

  // Derived roads from the precomputed marks
  const styles = [
    (c, s, cx, cy) => `<circle cx="${cx}" cy="${cy}" r="${s / 2 - 3}" fill="none" stroke="${COLOR(c.key)}" stroke-width="2"/>`,
    (c, s, cx, cy) => `<circle cx="${cx}" cy="${cy}" r="${s / 2 - 3}" fill="${COLOR(c.key)}"/>`,
    (c, s, cx, cy) => `<line x1="${cx - s / 2 + 3}" y1="${cy + s / 2 - 3}" x2="${cx + s / 2 - 3}" y2="${cy - s / 2 + 3}" stroke="${COLOR(c.key)}" stroke-width="2.5"/>`,
  ];
  for (let k = 0; k < 3; k++) {
    const marks = shown.map(x => x[5][k]).filter(m => m !== "-").map(m => [m, null, 0]);
    const cells = place(marks), s3 = 14, cols = Math.max(30, ...cells.map(c => c.c + 2));
    $("r" + k).innerHTML = marks.length
      ? svgGrid(cells, cols, s3, (c, s) => styles[k](c, s, c.c * s + s / 2, c.r * s + s / 2))
      : `<div style="padding:8px 10px;font-size:13px;color:var(--muted)">Not started yet</div>`;
  }
  for (const id of ["bead", "big", "r0", "r1", "r2"]) { const el = $(id); el.scrollLeft = el.scrollWidth; }
}

function go(h) { hand = Math.min(Math.max(1, h), DATA[shoe].length); render(); }
function stop() { clearInterval(timer); timer = null; $("play").textContent = "▶ Play"; }
$("shoe").onchange = e => { shoe = e.target.value; stop(); go(1); };
$("first").onclick = () => go(1);
$("last").onclick = () => go(DATA[shoe].length);
$("prev").onclick = () => go(hand - 1);
$("next").onclick = () => go(hand + 1);
$("slider").oninput = e => go(+e.target.value);
$("play").onclick = () => {
  if (timer) return stop();
  $("play").textContent = "❚❚ Pause";
  timer = setInterval(() => { if (hand >= DATA[shoe].length) stop(); else go(hand + 1); }, 600);
};
document.addEventListener("keydown", e => {
  if (e.target.tagName === "SELECT") return;
  if (e.key === "ArrowRight") go(hand + 1);
  else if (e.key === "ArrowLeft") go(hand - 1);
  else if (e.key === "Home") go(1);
  else if (e.key === "End") go(DATA[shoe].length);
  else if (e.key === " ") { e.preventDefault(); $("play").click(); }
});
matchMedia("(prefers-color-scheme: dark)").addEventListener("change", render);
render();
</script>
</body>
</html>
"""

// Rebuilds a project shoe in the browser and deals it exactly like the Python code.
// Python's random.Random is MT19937 seeded with init_by_array([seed]); random.shuffle
// uses _randbelow -> getrandbits(k) = genrand_uint32() >>> (32 - k) with rejection.
class MT {
  constructor(seed) {
    this.mt = new Uint32Array(624);
    this.initByArray([seed >>> 0]);
  }
  initGenrand(s) {
    const mt = this.mt;
    mt[0] = s >>> 0;
    for (let i = 1; i < 624; i++) {
      const x = mt[i - 1] ^ (mt[i - 1] >>> 30);
      mt[i] = (Math.imul(1812433253, x) + i) >>> 0;
    }
    this.mti = 624;
  }
  initByArray(key) {
    const mt = this.mt;
    this.initGenrand(19650218);
    let i = 1, j = 0;
    for (let k = Math.max(624, key.length); k; k--) {
      const x = mt[i - 1] ^ (mt[i - 1] >>> 30);
      mt[i] = ((mt[i] ^ Math.imul(x, 1664525)) + key[j] + j) >>> 0;
      i++; j++;
      if (i >= 624) { mt[0] = mt[623]; i = 1; }
      if (j >= key.length) j = 0;
    }
    for (let k = 623; k; k--) {
      const x = mt[i - 1] ^ (mt[i - 1] >>> 30);
      mt[i] = ((mt[i] ^ Math.imul(x, 1566083941)) - i) >>> 0;
      i++;
      if (i >= 624) { mt[0] = mt[623]; i = 1; }
    }
    mt[0] = 0x80000000;
    this.mti = 624;
  }
  twist() {
    const mt = this.mt;
    for (let kk = 0; kk < 624; kk++) {
      const y = (mt[kk] & 0x80000000) | (mt[(kk + 1) % 624] & 0x7fffffff);
      mt[kk] = mt[(kk + 397) % 624] ^ (y >>> 1) ^ (y & 1 ? 0x9908b0df : 0);
    }
    this.mti = 0;
  }
  next() {
    if (this.mti >= 624) this.twist();
    let y = this.mt[this.mti++];
    y ^= y >>> 11;
    y ^= (y << 7) & 0x9d2c5680;
    y ^= (y << 15) & 0xefc60000;
    y ^= y >>> 18;
    return y >>> 0;
  }
  skip(n) {  // discard n 32-bit words
    while (n > 0) {
      if (this.mti >= 624) this.twist();
      const take = Math.min(n, 624 - this.mti);
      this.mti += take;
      n -= take;
    }
  }
  getrandbits(k) { return k === 0 ? 0 : this.next() >>> (32 - k); }
  randbelow(n) {
    const k = 32 - Math.clz32(n);
    let r = this.getrandbits(k);
    while (r >= n) r = this.getrandbits(k);
    return r;
  }
}

const DECKS = 8, CUT_CARD = 14;

function buildShoe(seed, offset) {
  const cards = [];
  for (let v = 0; v < 10; v++) for (let n = 0; n < (v === 0 ? 16 : 4) * DECKS; n++) cards.push(v);
  const rng = new MT(seed);
  rng.skip(offset);
  for (let i = cards.length - 1; i >= 1; i--) {
    const j = rng.randbelow(i + 1);
    const t = cards[i]; cards[i] = cards[j]; cards[j] = t;
  }
  return cards;
}

function bankerDraws(bt, p3) {
  if (p3 === null) return bt <= 5;
  if (bt <= 2) return true;
  if (bt === 3) return p3 !== 8;
  if (bt === 4) return p3 >= 2 && p3 <= 7;
  if (bt === 5) return p3 >= 4 && p3 <= 7;
  if (bt === 6) return p3 === 6 || p3 === 7;
  return false;
}

const OFFSETS = [["big_eye", 1, "Big Eye Boy"], ["small", 2, "Small Road"], ["cockroach", 3, "Cockroach Pig"]];
const NAME = { P: "Player", B: "Banker", T: "Tie" };

class Board {
  constructor() { this.cols = []; this.last = null; this.beads = []; this.roads = { big_eye: [], small: [], cockroach: [] }; }
  colorIf(side, k) {
    const cols = this.cols;
    if (!cols.length) return null;
    if (side === this.last) {
      const c = cols.length - 1, r = cols[c];
      if (c - k < 0) return null;
      const n = cols[c - k];
      if (n > r) return "R";
      return n === r ? "B" : "R";
    }
    const c = cols.length;
    if (c - 1 - k < 0) return null;
    return cols[c - 1] === cols[c - 1 - k] ? "R" : "B";
  }
  add(o) {
    this.beads.push(o);
    if (o === "T") return;
    for (const [name, k] of OFFSETS) {
      const color = this.colorIf(o, k);
      if (color) this.roads[name].push(color);
    }
    if (o === this.last) this.cols[this.cols.length - 1] += 1;
    else { this.cols.push(1); this.last = o; }
  }
}

function run(items) {
  if (!items.length) return [null, 0];
  const last = items[items.length - 1];
  let n = 0;
  for (let i = items.length - 1; i >= 0 && items[i] === last; i--) n++;
  return [last, n];
}

function boardLines(board, ties) {
  const [bead, bn] = run(board.beads);
  const lines = [bead ? `Bead Plate: ${NAME[bead]} × ${bn}` : "Bead Plate: —"];
  const mark = !ties ? "" : ties === 1 ? " (tie)" : ` (tie × ${ties})`;
  lines.push(board.last === null ? `Big Road: —${mark}` : `Big Road: ${NAME[board.last]} × ${board.cols[board.cols.length - 1]}${mark}`);
  for (const [key, , label] of OFFSETS) {
    const [c, n] = run(board.roads[key]);
    lines.push(c ? `${label}: ${c === "R" ? "Red" : "Blue"} × ${n}` : `${label}: — (not started)`);
  }
  return lines;
}

const face = v => (v === 1 ? "A" : String(v));

// Deal a whole shoe. Each hand: {pc, bc, pt, bt, w, marks: [big_eye, small, cockroach] new marks or null, lines}
function dealShoe(seed, offset, lastHand) {
  const cards = buildShoe(seed, offset);
  const board = new Board();
  const hands = [];
  let ties = 0;
  const totals = { B: 0, P: 0, T: 0 };
  while (cards.length > CUT_CARD && (!lastHand || hands.length < lastHand)) {
    const p = [cards.pop()], b = [cards.pop()];
    p.push(cards.pop()); b.push(cards.pop());
    let pt = (p[0] + p[1]) % 10, bt = (b[0] + b[1]) % 10;
    if (pt < 8 && bt < 8) {
      let p3 = null;
      if (pt <= 5) { p3 = cards.pop(); p.push(p3); pt = (pt + p3) % 10; }
      if (bankerDraws(bt, p3)) { const v = cards.pop(); b.push(v); bt = (bt + v) % 10; }
    }
    const w = pt > bt ? "P" : bt > pt ? "B" : "T";
    totals[w] += 1;
    const before = OFFSETS.map(([k]) => board.roads[k].length);
    board.add(w);
    ties = w === "T" ? ties + 1 : 0;
    const marks = OFFSETS.map(([k], i) => (board.roads[k].length > before[i] ? board.roads[k][board.roads[k].length - 1] : null));
    hands.push({ pc: p.map(face), bc: b.map(face), pt, bt, w, marks, totals: { ...totals }, lines: boardLines(board, ties) });
  }
  return hands;
}

function handText(shoeNo, i, h) {
  return [
    `Shoe ${String(shoeNo).padStart(6, "0")} | Hand ${String(i + 1).padStart(3, "0")}`,
    `Player Cards: ${h.pc.join(", ")}`, `Banker Cards: ${h.bc.join(", ")}`,
    `Player Total: ${h.pt}`, `Banker Total: ${h.bt}`, `Winner: ${NAME[h.w]}`,
    `Shoe Totals: Banker ${h.totals.B} | Player ${h.totals.P} | Tie ${h.totals.T}`,
    "Visible board states", ...h.lines,
  ].join("\n");
}

if (typeof module !== "undefined") module.exports = { MT, buildShoe, dealShoe, handText };

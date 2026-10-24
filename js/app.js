// Shared helpers: data loading, dates, the workout log in localStorage, and session status.

export const STORAGE_KEY = 'vbtrainer.log.v1';
export const LOG_VERSION = 1;
const GRACE_DAYS = 2; // a session done up to 2 days late still counts as on time

// ---------- data ----------

async function getJSON(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Could not load ${url} (${res.status})`);
  return res.json();
}

export async function loadData() {
  const [program, exercises] = await Promise.all([
    getJSON('data/program.json'),
    getJSON('data/exercises.json'),
  ]);
  const exById = Object.fromEntries(exercises.map((e) => [e.id, e]));
  return { program, exercises, exById };
}

// ---------- dates (all local, midnight-based) ----------

export function parseDate(str) {
  const [y, m, d] = str.split('-').map(Number);
  return new Date(y, m - 1, d);
}

export function isoDate(date) {
  const pad = (n) => String(n).padStart(2, '0');
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`;
}

// `?today=YYYY-MM-DD` lets a parent preview any day of the program.
export function today() {
  const override = new URLSearchParams(location.search).get('today');
  if (override && /^\d{4}-\d{2}-\d{2}$/.test(override)) return parseDate(override);
  const now = new Date();
  return new Date(now.getFullYear(), now.getMonth(), now.getDate());
}

export function daysBetween(a, b) {
  return Math.round((b - a) / 86400000);
}

export function addDays(date, n) {
  return new Date(date.getFullYear(), date.getMonth(), date.getDate() + n);
}

export function fmtDate(date, opts = { weekday: 'short', month: 'short', day: 'numeric' }) {
  return date.toLocaleDateString('en-US', opts);
}

// Keep the preview date when moving between pages.
export function withToday(url) {
  const override = new URLSearchParams(location.search).get('today');
  if (!override) return url;
  return url + (url.includes('?') ? '&' : '?') + 'today=' + encodeURIComponent(override);
}

// ---------- the log ----------

export function emptyLog() {
  return { version: LOG_VERSION, sessions: {} };
}

export function loadLog() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return emptyLog();
    const data = JSON.parse(raw);
    if (!data || data.version !== LOG_VERSION || typeof data.sessions !== 'object' || data.sessions === null) {
      return emptyLog();
    }
    return data;
  } catch {
    return emptyLog();
  }
}

export function saveLog(log) {
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(log));
    return true;
  } catch {
    return false;
  }
}

export function storageWorks() {
  try {
    const k = '__vbtrainer_test__';
    localStorage.setItem(k, '1');
    localStorage.removeItem(k);
    return true;
  } catch {
    return false;
  }
}

export const sessionKey = (week, day) => `w${week}-${day}`;

// ---------- program helpers ----------

// Every scheduled session in date order.
export function allSessions(program) {
  const list = [];
  for (const wk of program.weeks) {
    for (const [day, data] of Object.entries(wk.days)) {
      list.push({
        key: sessionKey(wk.week, day),
        week: wk.week,
        day,
        date: parseDate(data.date),
        phase: program.phases[wk.phase],
        focus: program.days[day].focus,
        data,
      });
    }
  }
  return list.sort((a, b) => a.date - b.date);
}

export function swimOn(entry, logSession) {
  return logSession && typeof logSession.swimIncluded === 'boolean' ? logSession.swimIncluded : entry.data.swim;
}

// The session's blocks in order, with that day's exercises and time budget.
export function sessionBlocks(program, entry, withSwim) {
  return program.blocks
    .filter((b) => !(b.onlyWithSwim && !withSwim) && !(b.onlyWithoutSwim && withSwim))
    .map((b) => ({
      ...b,
      minutes: b.id === 'swim'
        ? program.swimPlans[entry.data.swimPlan].minutes
        : withSwim && b.minutesWithSwim ? b.minutesWithSwim : b.minutes,
      items: entry.data.exercises.filter((i) => i.block === b.id),
    }));
}

export function plannedMinutes(program, entry, withSwim) {
  return sessionBlocks(program, entry, withSwim).reduce((sum, b) => sum + b.minutes, 0);
}

const UNIT = { reps: '', s: ' s', min: ' min' };

export function prescription(item) {
  const amount = `${item.reps}${UNIT[item.unit] ?? ' ' + item.unit}`;
  const base = item.sets === 1 && item.unit === 'min' ? amount : `${item.sets} × ${amount}`;
  return item.perSide ? `${base} per side` : base;
}

export function setCounts(entry, logSession) {
  let done = 0;
  let total = 0;
  for (const item of entry.data.exercises) {
    total += item.sets;
    const sets = logSession?.exercises?.[item.exerciseId]?.sets ?? [];
    done += sets.slice(0, item.sets).filter(Boolean).length;
  }
  return { done, total };
}

export function isDone(logSession) {
  return Boolean(logSession && logSession.completedAt);
}

export function isStarted(logSession) {
  if (!logSession) return false;
  return Object.values(logSession.exercises ?? {}).some((e) => (e.sets ?? []).some(Boolean))
    || (logSession.swim?.sets ?? []).some(Boolean);
}

// done | progress | today | missed | upcoming
export function sessionStatus(entry, logSession, now) {
  if (isDone(logSession)) return 'done';
  if (isStarted(logSession)) return 'progress';
  const diff = daysBetween(entry.date, now);
  if (diff === 0) return 'today';
  if (diff > GRACE_DAYS) return 'missed';
  if (diff > 0) return 'due';
  return 'upcoming';
}

// What the dashboard should offer now.
export function currentSession(sessions, log, now) {
  const todays = sessions.find((s) => daysBetween(s.date, now) === 0);
  if (todays) return { entry: todays, kind: 'today' };
  const open = sessions.find((s) => !isDone(log.sessions[s.key]) && daysBetween(s.date, now) <= GRACE_DAYS);
  if (!open) return { entry: null, kind: 'finished' };
  return { entry: open, kind: open.date < now ? 'catch-up' : 'next' };
}

// Completed sessions in a row, counting back from the latest. A session more than
// GRACE_DAYS past its date without being finished breaks the streak.
export function streak(sessions, log, now) {
  let count = 0;
  for (const s of sessions) {
    if (isDone(log.sessions[s.key])) count += 1;
    else if (daysBetween(s.date, now) > GRACE_DAYS) count = 0;
  }
  return count;
}

// ---------- DOM ----------

// el('p', { class: 'x', onclick: fn }, 'text', childNode) — text is always set as text, never HTML.
export function el(tag, attrs = {}, ...children) {
  const node = document.createElement(tag);
  for (const [k, v] of Object.entries(attrs)) {
    if (v === null || v === undefined || v === false) continue;
    if (k.startsWith('on') && typeof v === 'function') node.addEventListener(k.slice(2), v);
    else if (k === 'class') node.className = v;
    else if (k === 'dataset') Object.assign(node.dataset, v);
    else if (v === true) node.setAttribute(k, '');
    else node.setAttribute(k, v);
  }
  for (const c of children.flat()) {
    if (c === null || c === undefined || c === false) continue;
    node.append(c instanceof Node ? c : document.createTextNode(String(c)));
  }
  return node;
}

export function showError(err) {
  const main = document.querySelector('main');
  main.replaceChildren(el('div', { class: 'card alert' },
    el('strong', {}, 'Something went wrong loading the app.'),
    el('p', {}, String(err.message || err)),
    el('p', {}, 'Check your connection and reload the page.')));
}

export function storageWarning() {
  if (storageWorks()) return null;
  return el('div', { class: 'card alert' },
    el('strong', {}, 'Your log can’t be saved in this browser.'),
    el('p', {}, 'Private browsing can block saving. Open the app in a normal tab so your workouts are kept.'));
}

export function markNav() {
  const nav = document.body.dataset.nav;
  for (const a of document.querySelectorAll('.tabbar a')) {
    if (a.dataset.nav === nav) a.setAttribute('aria-current', 'page');
    a.href = withToday(a.getAttribute('href').split('?')[0]);
  }
}

export function registerServiceWorker() {
  if ('serviceWorker' in navigator && (location.protocol === 'https:' || location.hostname === 'localhost')) {
    navigator.serviceWorker.register('sw.js').catch(() => {});
  }
}

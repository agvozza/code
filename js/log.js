import {
  loadData, loadLog, saveLog, allSessions, sessionKey, sessionStatus, setCounts, prescription, swimOn,
  today, isoDate, parseDate, fmtDate, el, showError, storageWarning, markNav, registerServiceWorker, withToday,
  isDone, LOG_VERSION,
} from './app.js';

let program;
let exercises;
let exById;
let sessions;
let log;

const PAIN_KEYS = ['knee', 'heel', 'shoulder'];

function painList(s) {
  return PAIN_KEYS.filter((k) => s?.pain?.[k]);
}

function sessionDate(entry, s) {
  return s?.dateDone ? parseDate(s.dateDone) : entry.date;
}

function logged() {
  return sessions.filter((e) => log.sessions[e.key]);
}

// ---------- summary ----------

function summary() {
  const done = sessions.filter((e) => isDone(log.sessions[e.key])).map((e) => log.sessions[e.key]);
  const minutes = done.reduce((t, s) => t + (s.minutes || 0), 0);
  const yards = done.reduce((t, s) => t + (s.swimIncluded !== false && s.swim?.yards ? s.swim.yards : 0), 0);
  const efforts = done.map((s) => s.effort).filter(Boolean);
  const avg = efforts.length ? (efforts.reduce((a, b) => a + b, 0) / efforts.length).toFixed(1) : '–';
  return el('section', { class: 'stats', 'aria-label': 'Totals' },
    el('div', { class: 'stat' }, el('b', {}, `${done.length}/${sessions.length}`), el('span', {}, 'workouts done')),
    el('div', { class: 'stat' }, el('b', {}, String(minutes)), el('span', {}, 'minutes trained')),
    el('div', { class: 'stat' }, el('b', {}, yards ? String(yards) : '0'), el('span', {}, 'yards swum')),
    el('div', { class: 'stat', style: 'grid-column: span 3' }, el('span', {}, `Average effort: ${avg} out of 5`)));
}

// ---------- history ----------

function historyCard(entry) {
  const s = log.sessions[entry.key];
  const status = sessionStatus(entry, s, today());
  const { done, total } = setCounts(entry, s);
  const pain = painList(s);
  const swim = swimOn(entry, s) && (s.swim?.yards || s.swim?.minutes);
  return el('article', { class: 'card hist' },
    el('div', { class: 'row spread' },
      el('h3', {}, `Week ${entry.week} · Day ${entry.day}`),
      el('span', { class: status === 'done' ? 'pill done' : 'pill amber' }, status === 'done' ? 'Done' : 'Not finished')),
    el('p', { class: 'muted small' },
      `${entry.focus} · ${fmtDate(sessionDate(entry, s), { weekday: 'short', month: 'short', day: 'numeric' })}`),
    el('div', { class: 'meta' },
      el('span', { class: 'pill' }, `${done}/${total} sets`),
      s.effort ? el('span', { class: 'pill' }, `Effort ${s.effort}/5`) : null,
      s.minutes ? el('span', { class: 'pill' }, `${s.minutes} min`) : null,
      swim ? el('span', { class: 'pill' }, `Swim ${s.swim.yards ? s.swim.yards + ' yd' : ''}${s.swim.yards && s.swim.minutes ? ', ' : ''}${s.swim.minutes ? s.swim.minutes + ' min' : ''}`) : null,
      pain.length ? el('span', { class: 'pill warn' }, `Pain: ${pain.join(', ')}`) : null),
    s.notes ? el('p', { style: 'margin-top:8px; white-space:pre-wrap' }, s.notes) : null,
    el('p', { class: 'small', style: 'margin-top:8px' },
      el('a', { href: withToday(`workout.html?week=${entry.week}&day=${entry.day}`) }, 'Open this workout')));
}

// ---------- per-exercise progress ----------

function exerciseProgress() {
  const rows = new Map();
  for (const entry of logged()) {
    const s = log.sessions[entry.key];
    for (const item of entry.data.exercises) {
      const ex = s.exercises?.[item.exerciseId];
      if (!ex || !((ex.sets ?? []).some(Boolean) || ex.reps || ex.weight)) continue;
      if (!rows.has(item.exerciseId)) rows.set(item.exerciseId, []);
      rows.get(item.exerciseId).push({ entry, s, item, ex });
    }
  }
  const swimRows = logged()
    .map((entry) => ({ entry, s: log.sessions[entry.key] }))
    .filter(({ entry, s }) => swimOn(entry, s) && (s.swim?.yards || s.swim?.minutes));

  if (!rows.size && !swimRows.length) return null;

  const table = (head, body) => el('table', { class: 'prog-table' },
    el('thead', {}, el('tr', {}, head.map((h) => el('th', { scope: 'col' }, h)))),
    el('tbody', {}, body));

  const blocks = exercises.filter((e) => rows.has(e.id)).map((e) => {
    const list = rows.get(e.id);
    return el('details', { class: 'ex-prog' },
      el('summary', {}, `${e.name} (${list.length})`),
      table(['Date', 'Plan', 'Sets', 'Reps / time', 'Weight'], list.map(({ entry, s, item, ex }) => el('tr', {},
        el('td', {}, fmtDate(sessionDate(entry, s), { month: 'short', day: 'numeric' })),
        el('td', {}, prescription(item)),
        el('td', {}, `${ex.sets.filter(Boolean).length}/${item.sets}`),
        el('td', {}, ex.reps || 'as planned'),
        el('td', {}, ex.weight ? `${ex.weight} lb` : '–')))));
  });

  if (swimRows.length) {
    blocks.push(el('details', { class: 'ex-prog' },
      el('summary', {}, `Swim (${swimRows.length})`),
      table(['Date', 'Minutes', 'Yards'], swimRows.map(({ entry, s }) => el('tr', {},
        el('td', {}, fmtDate(sessionDate(entry, s), { month: 'short', day: 'numeric' })),
        el('td', {}, s.swim.minutes ?? '–'),
        el('td', {}, s.swim.yards ?? '–'))))));
  }

  return el('section', { class: 'card' }, el('h2', {}, 'Progress by exercise'),
    el('p', { class: 'muted small' }, 'Tap an exercise to see every time you logged it.'), blocks);
}

// ---------- export / import ----------

function download(name, text, type) {
  const url = URL.createObjectURL(new Blob([text], { type }));
  const a = el('a', { href: url, download: name });
  document.body.append(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

function csvCell(value) {
  if (value === null || value === undefined) return '';
  let s = String(value);
  if (/^[=+\-@]/.test(s)) s = `'${s}`; // keep spreadsheets from treating text as a formula
  return /[",\r\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
}

export function buildCsv() {
  const header = ['date', 'week', 'day', 'type', 'item', 'block', 'planned', 'sets_done', 'sets_planned',
    'reps_logged', 'weight_lb', 'effort', 'minutes', 'yards', 'pain', 'notes', 'finished'];
  const rows = [header];
  for (const entry of logged()) {
    const s = log.sessions[entry.key];
    const date = isoDate(sessionDate(entry, s));
    const base = [date, entry.week, entry.day];
    const { done, total } = setCounts(entry, s);
    rows.push([...base, 'session', entry.focus, '', '', done, total, '', '', s.effort ?? '', s.minutes ?? '', '',
      painList(s).join(' '), s.notes ?? '', isDone(s) ? 'yes' : 'no']);
    for (const item of entry.data.exercises) {
      const ex = s.exercises?.[item.exerciseId];
      const name = exById[item.exerciseId]?.name ?? item.exerciseId;
      rows.push([...base, 'exercise', name, item.block, prescription(item),
        (ex?.sets ?? []).slice(0, item.sets).filter(Boolean).length, item.sets,
        ex?.reps ?? '', ex?.weight ?? '', '', '', '', '', '', '']);
    }
    if (swimOn(entry, s)) {
      const plan = program.swimPlans[entry.data.swimPlan];
      rows.push([...base, 'swim', plan.name, 'swim', plan.sets.map((x) => x.label).join(' / '),
        (s.swim?.sets ?? []).filter(Boolean).length, plan.sets.length, '', '', '',
        s.swim?.minutes ?? '', s.swim?.yards ?? '', '', '', '']);
    }
  }
  return '﻿' + rows.map((r) => r.map(csvCell).join(',')).join('\r\n') + '\r\n';
}

function exportJson() {
  const data = { app: 'vb-trainer', version: LOG_VERSION, exportedAt: new Date().toISOString(), sessions: log.sessions };
  download(`vb-trainer-log-${isoDate(today())}.json`, JSON.stringify(data, null, 2), 'application/json');
}

function exportCsv() {
  download(`vb-trainer-log-${isoDate(today())}.csv`, buildCsv(), 'text/csv;charset=utf-8');
}

function validSession(key, s) {
  return s && typeof s === 'object'
    && Number.isInteger(s.week) && (s.day === 'A' || s.day === 'B')
    && key === sessionKey(s.week, s.day)
    && sessions.some((e) => e.key === key);
}

async function importJson(file, status) {
  let data;
  try {
    data = JSON.parse(await file.text());
  } catch {
    status.textContent = 'That file isn’t a log export (it isn’t valid JSON).';
    return;
  }
  const incoming = data && typeof data.sessions === 'object' && data.sessions !== null ? data.sessions : null;
  if (!incoming || data.version !== LOG_VERSION) {
    status.textContent = 'That file isn’t a log export from this app.';
    return;
  }
  const valid = Object.entries(incoming).filter(([k, s]) => validSession(k, s));
  if (!valid.length) {
    status.textContent = 'No workouts found in that file.';
    return;
  }
  const newer = valid.filter(([k, s]) => {
    const mine = log.sessions[k];
    return !mine || !mine.updatedAt || (s.updatedAt && s.updatedAt > mine.updatedAt);
  });
  const replacing = newer.filter(([k]) => log.sessions[k]).length;
  const msg = `Import ${newer.length} of ${valid.length} workouts from this file?`
    + (replacing ? ` ${replacing} will replace older copies on this phone.` : '')
    + (valid.length > newer.length ? ` ${valid.length - newer.length} are skipped because this phone has a newer copy.` : '');
  if (!newer.length) {
    status.textContent = 'Nothing to import: this phone already has the same or newer copies of every workout.';
    return;
  }
  if (!confirm(msg)) return;
  for (const [k, s] of newer) log.sessions[k] = s;
  if (!saveLog(log)) {
    status.textContent = 'Import failed: this browser is blocking storage.';
    return;
  }
  render(`Imported ${newer.length} workouts.`);
}

function dataCard(message) {
  const status = el('p', { class: 'small', 'aria-live': 'polite', style: 'margin-top:8px' }, message ?? '');
  const fileInput = el('input', {
    type: 'file', accept: 'application/json,.json', class: 'file-input', id: 'import-file',
    onchange: (e) => {
      const f = e.target.files?.[0];
      if (f) importJson(f, status);
      e.target.value = '';
    },
  });
  return el('section', { class: 'card' },
    el('h2', {}, 'Back up or share'),
    el('p', { class: 'muted small' },
      'Your log lives on this phone only. Export it to send to a parent or to move to a new phone. CSV opens in Excel, Numbers or Google Sheets; JSON can be imported back here.'),
    el('div', { class: 'row', style: 'margin-top:10px' },
      el('button', { type: 'button', class: 'btn', onclick: exportCsv }, 'Export CSV'),
      el('button', { type: 'button', class: 'btn', onclick: exportJson }, 'Export JSON'),
      el('label', { class: 'btn', for: 'import-file' }, 'Import JSON'),
      fileInput),
    status);
}

// ---------- page ----------

function render(message) {
  const history = logged().slice().reverse();
  document.querySelector('main').replaceChildren(
    storageWarning() ?? '',
    el('header', { class: 'page-head' },
      el('h1', {}, 'Training log'),
      el('p', {}, 'Every workout you’ve logged, newest first.')),
    summary(),
    history.length
      ? el('div', {}, history.map(historyCard))
      : el('section', { class: 'card' },
        el('p', {}, 'No workouts logged yet.'),
        el('p', { class: 'muted small' }, 'Tick off sets on a workout page and they show up here.'),
        el('a', { class: 'btn primary', href: withToday('index.html'), style: 'margin-top:8px' }, 'Go to today’s workout')),
    exerciseProgress() ?? '',
    dataCard(message),
  );
}

async function main() {
  markNav();
  ({ program, exercises, exById } = await loadData());
  sessions = allSessions(program);
  log = loadLog();
  render();
  registerServiceWorker();
}

main().catch(showError);

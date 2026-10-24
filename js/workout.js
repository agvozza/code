import {
  loadData, loadLog, saveLog, allSessions, sessionBlocks, plannedMinutes, prescription, setCounts, swimOn,
  currentSession, today, isoDate, parseDate, fmtDate, el, showError, storageWarning, markNav, registerServiceWorker,
  withToday, isDone,
} from './app.js';

const EFFORT = ['Very easy', 'Easy', 'OK', 'Hard', 'Max'];
const PAIN = [
  ['knee', 'Knee (below the kneecap)'],
  ['heel', 'Heel'],
  ['shoulder', 'Shoulder'],
];

let program;
let exById;
let sessions;
let entry;
let log;
let main;

// ---------- state ----------

function current(create = false) {
  let s = log.sessions[entry.key];
  if (!s && create) {
    s = {
      week: entry.week,
      day: entry.day,
      scheduledDate: entry.data.date,
      startedAt: new Date().toISOString(),
      updatedAt: null,
      completedAt: null,
      dateDone: null,
      swimIncluded: entry.data.swim,
      exercises: {},
      effort: null,
      minutes: null,
      notes: '',
      pain: { knee: false, heel: false, shoulder: false },
      swim: { minutes: null, yards: null, yardsEdited: false, sets: [] },
    };
    log.sessions[entry.key] = s;
  }
  return s;
}

function exerciseLog(item) {
  const s = current(true);
  const ex = (s.exercises[item.exerciseId] ??= { sets: [], reps: '', weight: '' });
  ex.sets = Array.from({ length: item.sets }, (_, i) => Boolean(ex.sets[i]));
  return ex;
}

function save() {
  const s = current();
  if (s) s.updatedAt = new Date().toISOString();
  const ok = saveLog(log);
  const status = document.getElementById('saved');
  if (status) {
    status.textContent = ok ? 'Saved on this phone' : 'Not saved: this browser is blocking storage';
    status.classList.toggle('fail', !ok);
  }
  updateProgress();
}

const numberOrNull = (v) => (v === '' || Number.isNaN(Number(v)) ? null : Number(v));

// ---------- progress ----------

function counts() {
  const s = current();
  const { done, total } = setCounts(entry, s);
  if (!swimOn(entry, s)) return { done, total };
  const plan = program.swimPlans[entry.data.swimPlan];
  const swimDone = (s?.swim?.sets ?? []).slice(0, plan.sets.length).filter(Boolean).length;
  return { done: done + swimDone, total: total + plan.sets.length };
}

function updateProgress() {
  const { done, total } = counts();
  const text = document.getElementById('prog-text');
  const fill = document.getElementById('prog-fill');
  if (text) text.textContent = `${done} of ${total} sets done`;
  if (fill) fill.style.width = `${total ? Math.round((done / total) * 100) : 0}%`;
}

function painFlagged() {
  const p = current()?.pain;
  return Boolean(p && (p.knee || p.heel || p.shoulder));
}

function painAlert() {
  return el('div', { class: 'card alert', role: 'alert' },
    el('strong', {}, 'Stop and tell a parent.'),
    el('p', {}, 'Pain below the kneecap, at the heel, or in the shoulder means rest today. Don’t train through it. A parent decides when the next workout happens.'));
}

function updatePainAlert() {
  for (const id of ['pain-top', 'pain-bottom']) {
    const box = document.getElementById(id);
    if (box) box.replaceChildren(painFlagged() ? painAlert() : '');
  }
}

// ---------- pieces ----------

function header(withSwim, total) {
  const i = sessions.indexOf(entry);
  const link = (s, label) => (s
    ? el('a', { class: 'btn small', href: withToday(`workout.html?week=${s.week}&day=${s.day}`) }, label)
    : el('span'));
  const s = current();
  return el('header', { class: 'page-head' },
    el('div', { class: 'row spread' },
      link(sessions[i - 1], '‹ Previous'),
      el('a', { class: 'btn small', href: withToday('index.html') }, 'Today'),
      link(sessions[i + 1], 'Next ›')),
    el('h1', { style: 'margin-top:14px' }, `Week ${entry.week} · ${program.days[entry.day].name}`),
    el('p', {}, entry.focus),
    el('p', {}, `${entry.phase.name} phase · ${fmtDate(entry.date, { weekday: 'long', month: 'short', day: 'numeric' })} · about ${total} min`),
    el('div', { class: 'row', style: 'margin-top:6px' },
      el('span', { class: 'pill' }, withSwim ? 'Swim today' : 'No swim'),
      isDone(s) ? el('span', { class: 'pill done' }, 'Finished') : null));
}

function safetyCard() {
  return el('section', { class: 'card note' },
    el('strong', {}, 'Safety first'),
    el('ul', { class: 'rules', style: 'margin-top:6px' }, program.safety.map((r) => el('li', {}, r))));
}

function progressBar() {
  return el('div', { class: 'progress' },
    el('div', { class: 'row spread small' },
      el('span', { id: 'prog-text' }),
      el('span', { id: 'saved', class: 'saved', 'aria-live': 'polite' })),
    el('div', { class: 'bar' }, el('div', { id: 'prog-fill' })));
}

function videoHref(id) {
  return `${withToday('library.html')}#${id}`;
}

function exerciseCard(item) {
  const ex = exById[item.exerciseId];
  const saved = current()?.exercises?.[item.exerciseId];
  const isSet = (i) => Boolean(saved?.sets?.[i]);
  const card = el('article', { class: 'card ex-card' });

  const buttons = Array.from({ length: item.sets }, (_, i) => el('button', {
    type: 'button',
    class: 'set',
    'aria-pressed': String(isSet(i)),
    'aria-label': `${ex.name}: set ${i + 1} of ${item.sets}`,
  }, String(i + 1)));

  const allBtn = el('button', { type: 'button', class: 'btn small' });

  const refresh = () => {
    const sets = current()?.exercises?.[item.exerciseId]?.sets ?? [];
    const all = buttons.every((_, i) => Boolean(sets[i]));
    buttons.forEach((b, i) => b.setAttribute('aria-pressed', String(Boolean(sets[i]))));
    allBtn.textContent = all ? 'Clear' : 'All done';
    card.classList.toggle('complete', all);
  };

  buttons.forEach((b, i) => b.addEventListener('click', () => {
    const exLog = exerciseLog(item);
    exLog.sets[i] = !exLog.sets[i];
    refresh();
    save();
  }));
  allBtn.addEventListener('click', () => {
    const exLog = exerciseLog(item);
    const all = exLog.sets.every(Boolean);
    exLog.sets = exLog.sets.map(() => !all);
    refresh();
    save();
  });

  const field = (label, key, inputmode) => el('label', { class: 'field' }, label,
    el('input', {
      type: 'text',
      inputmode,
      value: saved?.[key] ?? '',
      oninput: (e) => { exerciseLog(item)[key] = e.target.value.trim(); save(); },
    }));
  const hasAdjust = Boolean(saved?.reps || saved?.weight);

  card.append(
    el('div', { class: 'ex-head' },
      el('div', {},
        el('h3', {}, el('a', { href: videoHref(ex.id) }, ex.name)),
        el('div', { class: 'rx' }, prescription(item)),
        item.note ? el('span', { class: 'pill amber' }, item.note) : null),
      el('a', { class: 'video-link', href: videoHref(ex.id) }, '▶ Video')),
    el('ul', { class: 'cues' }, ex.cues.map((c) => el('li', {}, c))),
    el('div', { class: 'sets' }, buttons, allBtn),
    el('details', { class: 'adjust', open: hasAdjust },
      el('summary', {}, 'Did something different? Log it'),
      el('div', { class: 'fields' },
        field(item.unit === 'reps' ? 'Reps done' : 'Time done', 'reps', 'text'),
        field('Weight (lb)', 'weight', 'decimal'))),
  );
  refresh();
  return card;
}

function swimCard() {
  const plan = program.swimPlans[entry.data.swimPlan];
  const s = current();
  const planned = plan.sets.reduce((sum, x) => sum + x.yards, 0);
  const yardsInput = el('input', {
    type: 'number', inputmode: 'numeric', min: '0', placeholder: String(planned),
    value: s?.swim?.yards ?? '',
    oninput: (e) => {
      const sw = current(true).swim;
      sw.yards = numberOrNull(e.target.value);
      sw.yardsEdited = e.target.value !== '';
      save();
    },
  });

  const checks = plan.sets.map((set, i) => el('label', { class: 'check' },
    el('input', {
      type: 'checkbox',
      checked: Boolean(s?.swim?.sets?.[i]),
      onchange: (e) => {
        const sw = current(true).swim;
        sw.sets = plan.sets.map((_, k) => Boolean(sw.sets[k]));
        sw.sets[i] = e.target.checked;
        if (!sw.yardsEdited) {
          const sum = plan.sets.reduce((t, x, k) => t + (sw.sets[k] ? x.yards : 0), 0);
          sw.yards = sum || null;
          yardsInput.value = sw.yards ?? '';
        }
        save();
      },
    }),
    el('span', {},
      el('b', {}, set.label), ': ', set.detail,
      set.exerciseId ? [' ', el('a', { href: videoHref(set.exerciseId) }, 'video')] : null)));

  return el('article', { class: 'card' },
    el('h3', {}, plan.name),
    el('p', { class: 'muted small' }, `${plan.note} Planned: about ${planned} yd.`),
    checks,
    el('div', { class: 'fields' },
      el('label', { class: 'field' }, 'Swim minutes',
        el('input', {
          type: 'number', inputmode: 'numeric', min: '0', placeholder: String(plan.minutes),
          value: s?.swim?.minutes ?? '',
          oninput: (e) => { current(true).swim.minutes = numberOrNull(e.target.value); save(); },
        })),
      el('label', { class: 'field' }, 'Distance (yards)', yardsInput)));
}

function blockSection(block) {
  const out = [el('div', { class: 'block-head' },
    el('h2', {}, block.name),
    el('span', { class: 'mins' }, `${block.minutes} min`))];
  const note = block.id === 'volleyball' && !block.items.length ? block.openNote : block.note;
  if (note) out.push(el('p', { class: 'block-note' }, note));
  if (block.id === 'swim') out.push(swimCard());
  out.push(...block.items.map(exerciseCard));
  return out;
}

function swimToggle(withSwim) {
  const setSwim = (on) => {
    current(true).swimIncluded = on;
    save();
    render();
  };
  if (!withSwim) {
    return el('section', { class: 'card' },
      el('p', {}, 'No swim planned for this session.'),
      el('button', { type: 'button', class: 'btn small', onclick: () => setSwim(true) }, 'Add a swim'));
  }
  return el('p', { class: 'small' },
    el('button', { type: 'button', class: 'btn small', onclick: () => setSwim(false) },
      entry.data.swim ? 'Skipping the pool today' : 'Remove the swim'));
}

function finishCard(total) {
  const s = current();
  const effortButtons = EFFORT.map((label, i) => el('button', {
    type: 'button',
    'aria-pressed': String(s?.effort === i + 1),
    onclick: (e) => {
      current(true).effort = i + 1;
      e.currentTarget.parentElement.querySelectorAll('button')
        .forEach((b, k) => b.setAttribute('aria-pressed', String(k === i)));
      save();
    },
  }, String(i + 1), el('span', {}, label)));

  const painChecks = PAIN.map(([key, label]) => el('label', { class: 'check' },
    el('input', {
      type: 'checkbox',
      checked: Boolean(s?.pain?.[key]),
      onchange: (e) => { current(true).pain[key] = e.target.checked; save(); updatePainAlert(); },
    }),
    el('span', {}, label)));

  const done = isDone(s);
  return el('section', { class: 'card', id: 'finish' },
    el('h2', {}, 'How did it go?'),
    el('p', { class: 'muted small', style: 'margin-top:8px' }, 'Effort: 1 is very easy, 5 is max'),
    el('div', { class: 'effort' }, effortButtons),
    el('div', { class: 'fields', style: 'grid-template-columns:1fr' },
      el('label', { class: 'field' }, 'Minutes trained',
        el('input', {
          type: 'number', inputmode: 'numeric', min: '0', placeholder: String(total),
          value: s?.minutes ?? '',
          oninput: (e) => { current(true).minutes = numberOrNull(e.target.value); save(); },
        })),
      el('label', { class: 'field' }, 'Notes',
        el('textarea', {
          placeholder: 'How did it feel? Anything to remember?',
          oninput: (e) => { current(true).notes = e.target.value; save(); },
        }, s?.notes ?? ''))),
    el('h3', { style: 'margin-top:18px' }, 'Pain check'),
    el('p', { class: 'muted small' }, 'Tick anything that hurt today.'),
    painChecks,
    el('div', { id: 'pain-bottom' }),
    el('button', {
      type: 'button',
      class: done ? 'btn done block' : 'btn primary block',
      style: 'margin-top:14px',
      onclick: () => {
        const cur = current(true);
        if (!cur.completedAt) {
          cur.completedAt = new Date().toISOString();
          cur.dateDone = isoDate(today());
        }
        if (cur.minutes === null) cur.minutes = total;
        save();
        render();
        document.getElementById('finish')?.scrollIntoView({ block: 'start' });
      },
    }, done ? 'Finished ✓ Save changes' : 'Finish workout'),
    done ? el('p', { class: 'small', style: 'margin-top:10px' },
      `Logged ${fmtDate(s.dateDone ? parseDate(s.dateDone) : new Date(s.completedAt))}. Nice work! `,
      el('a', { href: withToday('index.html') }, 'Back to today'),
      ' · ',
      el('a', {
        href: '#',
        onclick: (e) => {
          e.preventDefault();
          const cur = current();
          cur.completedAt = null;
          cur.dateDone = null;
          save();
          render();
        },
      }, 'Mark as not finished')) : null);
}

// ---------- page ----------

function render() {
  const s = current();
  const withSwim = swimOn(entry, s);
  const total = plannedMinutes(program, entry, withSwim);
  const blocks = sessionBlocks(program, entry, withSwim);
  main.replaceChildren(
    storageWarning() ?? '',
    header(withSwim, total),
    el('div', { id: 'pain-top' }),
    safetyCard(),
    progressBar(),
    ...blocks.flatMap(blockSection),
    swimToggle(withSwim),
    finishCard(total),
  );
  updateProgress();
  updatePainAlert();
}

async function main_() {
  markNav();
  main = document.querySelector('main');
  ({ program, exById } = await loadData());
  sessions = allSessions(program);
  log = loadLog();

  const params = new URLSearchParams(location.search);
  const week = Number(params.get('week'));
  const day = (params.get('day') || '').toUpperCase();
  entry = sessions.find((s) => s.week === week && s.day === day);
  if (!entry) {
    entry = currentSession(sessions, log, today()).entry ?? sessions[sessions.length - 1];
    history.replaceState(null, '', withToday(`workout.html?week=${entry.week}&day=${entry.day}`));
  }
  document.title = `Week ${entry.week} Day ${entry.day} · Volleyball Trainer`;
  render();
  registerServiceWorker();
}

main_().catch(showError);

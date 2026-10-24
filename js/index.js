import {
  loadData, loadLog, allSessions, currentSession, sessionStatus, streak, plannedMinutes, swimOn, setCounts,
  today, parseDate, addDays, daysBetween, fmtDate, el, showError, storageWarning, markNav, registerServiceWorker,
  withToday, isDone,
} from './app.js';

const STATUS_LABEL = {
  done: 'Done',
  progress: 'In progress',
  today: 'Today',
  due: 'Not logged yet',
  missed: 'Missed',
  upcoming: 'Planned',
};

function workoutHref(s) {
  return withToday(`workout.html?week=${s.week}&day=${s.day}`);
}

function todayCard(program, sessions, log, now) {
  const { entry, kind } = currentSession(sessions, log, now);
  const start = parseDate(program.start);

  if (!entry) {
    const doneCount = sessions.filter((s) => isDone(log.sessions[s.key])).length;
    const blockOver = now > parseDate(program.end);
    return el('section', { class: 'card hero' },
      el('p', { class: 'muted' }, 'Off-season block'),
      el('h2', {}, blockOver ? 'The off-season block is over' : 'No workouts left in this block'),
      el('p', {}, `${doneCount} of ${sessions.length} workouts logged. Rest up and get ready for the season.`),
      el('a', { class: 'btn block', href: withToday('log.html') }, 'See your log'));
  }

  const s = log.sessions[entry.key];
  const status = sessionStatus(entry, s, now);
  const minutes = plannedMinutes(program, entry, swimOn(entry, s));
  const { done, total } = setCounts(entry, s);

  let eyebrow;
  if (kind === 'today') eyebrow = 'Today';
  else if (kind === 'catch-up') eyebrow = `Catch up: planned for ${fmtDate(entry.date)}`;
  else if (now < start && entry === sessions[0]) eyebrow = `Starts ${fmtDate(entry.date, { weekday: 'long', month: 'short', day: 'numeric' })}`;
  else if (now < start) eyebrow = `Next workout ${fmtDate(entry.date)}`;
  else eyebrow = `Rest day today · next workout ${fmtDate(entry.date)}`;

  let action = 'Start workout';
  if (status === 'done') action = 'View workout';
  else if (status === 'progress') action = `Continue workout (${done}/${total} sets)`;
  else if (kind === 'next') action = 'Preview workout';

  return el('section', { class: 'card hero' },
    el('p', { class: 'muted' }, eyebrow),
    el('h2', {}, `Week ${entry.week} · ${program.days[entry.day].name}`),
    el('p', {}, entry.focus),
    el('div', { class: 'row', style: 'margin:8px 0 14px' },
      el('span', { class: 'pill' }, `${entry.phase.name} phase`),
      el('span', { class: 'pill' }, `About ${minutes} min`),
      el('span', { class: 'pill' }, swimOn(entry, s) ? 'Swim' : 'No swim'),
      status === 'done' ? el('span', { class: 'pill done' }, 'Done') : null),
    el('a', { class: status === 'done' ? 'btn done block' : 'btn primary block', href: workoutHref(entry) }, action));
}

function stats(program, sessions, log, now) {
  const toSeason = daysBetween(now, parseDate(program.seasonStart));
  const doneCount = sessions.filter((s) => isDone(log.sessions[s.key])).length;
  const seasonStat = toSeason > 0
    ? [String(toSeason), toSeason === 1 ? 'day to season' : 'days to season']
    : toSeason === 0 ? ['0', 'season starts today!'] : ['✓', 'season underway'];
  const run = streak(sessions, log, now);
  return el('section', { class: 'stats', 'aria-label': 'Progress' },
    el('div', { class: 'stat' }, el('b', {}, seasonStat[0]), el('span', {}, seasonStat[1])),
    el('div', { class: 'stat' }, el('b', {}, String(run)), el('span', {}, 'workout streak')),
    el('div', { class: 'stat' }, el('b', {}, `${doneCount}/${sessions.length}`), el('span', {}, 'workouts done')));
}

function calendar(program, sessions, log, now) {
  const start = parseDate(program.start);
  const byDate = new Map(sessions.map((s) => [s.date.getTime(), s]));
  const head = el('tr', {}, el('th', { class: 'wk', scope: 'col' }, 'Wk'),
    ['M', 'T', 'W', 'T', 'F', 'S', 'S'].map((d) => el('th', { scope: 'col' }, d)));
  const rows = program.weeks.map((wk, w) => el('tr', {},
    el('th', { class: 'wk', scope: 'row' }, String(wk.week)),
    Array.from({ length: 7 }, (_, d) => {
      const date = addDays(start, w * 7 + d);
      const s = byDate.get(date.getTime());
      const isToday = daysBetween(date, now) === 0;
      const label = date.getDate() === 1 ? fmtDate(date, { month: 'short', day: 'numeric' }) : String(date.getDate());
      if (!s) {
        return el('td', {}, el('span', { class: `day${isToday ? ' is-today' : ''}`, 'aria-label': `${fmtDate(date)}, rest day` }, label));
      }
      const status = sessionStatus(s, log.sessions[s.key], now);
      const cls = ['day', ['done', 'progress', 'missed'].includes(status) ? status : '', isToday ? 'is-today' : ''].join(' ').trim();
      return el('td', {}, el('a', {
        class: cls,
        href: workoutHref(s),
        'aria-label': `Week ${s.week} Day ${s.day}, ${fmtDate(s.date)}: ${STATUS_LABEL[status]}`,
      }, el('b', {}, s.day), label));
    })));

  const key = (color, text, extra = '') => el('span', {}, el('i', { style: `background:${color};${extra}` }), text);
  return el('section', { class: 'card' },
    el('div', { class: 'row spread' },
      el('h2', {}, '5-week plan'),
      el('span', { class: 'muted small' }, `${fmtDate(start, { month: 'short', day: 'numeric' })} – ${fmtDate(parseDate(program.end), { month: 'short', day: 'numeric' })}`)),
    el('table', { class: 'cal', style: 'margin-top:8px' }, el('thead', {}, head), el('tbody', {}, rows)),
    el('div', { class: 'legend' },
      key('var(--done)', 'Done'),
      key('var(--amber-soft)', 'Started'),
      key('var(--accent-soft)', 'Planned'),
      key('transparent', 'Missed', 'border:2px solid var(--border)'),
      key('transparent', 'Today', 'border:2px solid var(--text)')),
    el('p', { class: 'muted small', style: 'margin-top:8px' },
      'Weeks 1–2 Foundation, weeks 3–4 Build, week 5 Taper. Tap a workout to open it.'));
}

function painNotice(sessions, log) {
  const recent = sessions
    .map((s) => log.sessions[s.key])
    .filter((s) => s && s.completedAt && s.pain && (s.pain.knee || s.pain.heel || s.pain.shoulder))
    .sort((a, b) => b.completedAt.localeCompare(a.completedAt))[0];
  if (!recent) return null;
  const where = ['knee', 'heel', 'shoulder'].filter((k) => recent.pain[k]).join(', ');
  return el('section', { class: 'card alert', role: 'alert' },
    el('strong', {}, `Pain logged after Week ${recent.week} Day ${recent.day} (${where}).`),
    el('p', {}, 'Check in with a parent before the next workout. Rest until it feels fine.'));
}

async function main() {
  markNav();
  const { program } = await loadData();
  const sessions = allSessions(program);
  const log = loadLog();
  const now = today();

  document.querySelector('main').replaceChildren(
    storageWarning() ?? '',
    el('header', { class: 'page-head' },
      el('h1', {}, 'Off-season training'),
      el('p', {}, `Season starts ${fmtDate(parseDate(program.seasonStart), { weekday: 'long', month: 'long', day: 'numeric' })}`)),
    painNotice(sessions, log) ?? '',
    todayCard(program, sessions, log, now),
    stats(program, sessions, log, now),
    calendar(program, sessions, log, now),
    el('section', { class: 'card note' },
      el('h2', {}, 'Safety rules'),
      el('ul', { class: 'rules', style: 'margin-top:8px' }, program.safety.map((r) => el('li', {}, r)))),
  );
  registerServiceWorker();
}

main().catch(showError);

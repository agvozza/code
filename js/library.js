import { loadData, el, showError, markNav, registerServiceWorker, withToday } from './app.js';

const CATEGORIES = [
  ['warm-up', 'Warm-up'],
  ['landing', 'Landing'],
  ['jumps', 'Jumps'],
  ['strength', 'Strength'],
  ['core', 'Core'],
  ['volleyball', 'Volleyball'],
  ['shoulder', 'Shoulder care'],
  ['swim', 'Swim'],
];

const PLAY_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 4l15 8-15 8z"/></svg>';

function watchUrl(v) {
  return v.start ? `${v.url}&t=${v.start}s` : v.url;
}

function embedUrl(v) {
  const params = new URLSearchParams({ autoplay: '1', rel: '0', playsinline: '1', modestbranding: '1' });
  if (v.start) params.set('start', String(v.start));
  return `https://www.youtube-nocookie.com/embed/${encodeURIComponent(v.youtubeId)}?${params}`;
}

// Thumbnail first; the YouTube player only loads when tapped.
function player(ex, which) {
  const v = ex[which];
  const box = el('div', { class: 'player' });
  const img = el('img', {
    src: `https://i.ytimg.com/vi/${encodeURIComponent(v.youtubeId)}/hqdefault.jpg`,
    alt: '',
    loading: 'lazy',
    decoding: 'async',
  });
  const btn = el('button', { type: 'button', 'aria-label': `Play video: ${v.title}` }, img);
  // No thumbnail usually means a weak connection: keep the play button and point to the backup.
  img.addEventListener('error', () => {
    img.replaceWith(el('span', { class: 'fail' },
      which === 'video'
        ? 'Tap to play. If the video won’t load, try the backup below.'
        : 'Tap to play. If it won’t load, open it on YouTube.'));
    box.closest('.ex-card')?.querySelector('.backup-link')?.classList.add('pill', 'amber');
  });
  const play = el('span', { class: 'play' });
  play.innerHTML = PLAY_ICON;
  btn.append(play);
  btn.addEventListener('click', () => {
    box.replaceChildren(el('iframe', {
      src: embedUrl(v),
      title: v.title,
      allow: 'autoplay; encrypted-media; picture-in-picture; fullscreen',
      allowfullscreen: true,
      referrerpolicy: 'strict-origin-when-cross-origin',
    }));
  });
  box.append(btn);
  return box;
}

function card(ex) {
  const article = el('article', { class: 'card ex-card', id: ex.id });
  const meta = el('p', { class: 'video-meta' });
  let showing = 'video';

  const renderVideo = () => {
    const v = ex[showing];
    const playerBox = player(ex, showing);
    const current = article.querySelector('.player');
    if (current) current.replaceWith(playerBox);
    else article.insertBefore(playerBox, meta);
    meta.replaceChildren(
      showing === 'backup' ? el('span', { class: 'pill amber' }, 'Backup') : '',
      showing === 'backup' ? ' ' : '',
      `${v.title} — ${v.channel}`,
    );
    swapLink.textContent = showing === 'video' ? 'Video not working? Watch the backup' : 'Back to the main video';
    ytLink.href = watchUrl(v);
  };

  const swapLink = el('a', { href: '#', class: 'backup-link' });
  swapLink.addEventListener('click', (e) => {
    e.preventDefault();
    showing = showing === 'video' ? 'backup' : 'video';
    renderVideo();
  });
  const ytLink = el('a', { href: watchUrl(ex.video), target: '_blank', rel: 'noopener' }, 'Open on YouTube');

  article.append(
    el('h3', {}, ex.name),
    meta,
    el('div', { class: 'video-links' }, swapLink, ytLink),
    el('ul', { class: 'cues' }, ex.cues.map((c) => el('li', {}, c))),
  );
  renderVideo();
  return article;
}

function focusHash() {
  const id = decodeURIComponent(location.hash.slice(1));
  if (!id) return;
  const target = document.getElementById(id);
  if (!target) return;
  document.querySelectorAll('.highlight').forEach((n) => n.classList.remove('highlight'));
  target.classList.add('highlight');
  target.scrollIntoView({ block: 'start' });
}

async function main() {
  markNav();
  const { exercises } = await loadData();
  const main = document.querySelector('main');
  const cameFromWorkout = document.referrer.includes('workout.html');

  main.replaceChildren(
    cameFromWorkout
      ? el('button', { type: 'button', class: 'btn small', onclick: () => history.back() }, '← Back to workout')
      : '',
    el('header', { class: 'page-head' },
      el('h1', {}, 'Exercise videos'),
      el('p', {}, 'Tap a video to play it. Every exercise has a backup video if the first one doesn’t work.')),
    el('nav', { class: 'chips', 'aria-label': 'Categories' },
      CATEGORIES.filter(([c]) => exercises.some((e) => e.category === c))
        .map(([c, label]) => el('a', { href: `#cat-${c}` }, label))),
  );

  for (const [cat, label] of CATEGORIES) {
    const list = exercises.filter((e) => e.category === cat);
    if (!list.length) continue;
    main.append(el('h2', { class: 'cat-head', id: `cat-${cat}` }, label), ...list.map(card));
  }

  main.append(el('p', { class: 'muted small' },
    'Videos play through YouTube’s privacy-enhanced mode. ',
    el('a', { href: withToday('index.html') }, 'Back to today')));

  focusHash();
  window.addEventListener('hashchange', focusHash);
  registerServiceWorker();
}

main().catch(showError);

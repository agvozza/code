# Volleyball Trainer

A phone-friendly trainer and workout log for a 5-week volleyball off-season (Monday, October 26 to Sunday, November 29, 2026). Plain HTML, CSS and JavaScript: no build step, no server, no accounts. See [PROJECT_BRIEF.md](PROJECT_BRIEF.md) for the full brief.

## Pages

| Page | What it does |
| --- | --- |
| `index.html` | Today's workout, countdown to the season, workout streak, the 5-week calendar, safety rules |
| `workout.html?week=3&day=A` | One session in order with a time budget per block. Tick off sets, log different reps or weight, log the swim, rate effort, add notes and do the pain check |
| `library.html` | Every exercise grouped by category, with its video (loads only when tapped), a backup video and coaching cues. Workout pages link to `library.html#<exercise-id>` |
| `log.html` | History of every session, progress by exercise, export as CSV or JSON, import JSON |

## Publish on GitHub Pages

1. Merge this branch into `main`.
2. In the repository on GitHub, open **Settings → Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**, then branch `main` and folder `/ (root)`, and save.
4. After a minute the app is live at `https://<your-github-username>.github.io/<repository-name>/`. Open it on her phone and use **Share → Add to Home Screen** so it opens like an app.

GitHub Pages is free for public repositories; a private repository needs a paid GitHub plan for Pages.

## Preview any day

Add `?today=YYYY-MM-DD` to any page to see the app as it will look on that date, for example `index.html?today=2026-11-12`. Logging still works normally.

## Change the program

Everything the pages show comes from two files, so changing a workout never means editing page code.

- `data/program.json`: session dates, which exercises each day has (`exerciseId`, `sets`, `reps`, `unit` of `reps`, `s` or `min`, `perSide`, optional `note`), block minutes, which days include a swim (`"swim": true`), the swim plans and the safety rules. To move a workout, change its `date`.
- `data/exercises.json`: each exercise's name, cues, main video and backup video. See `data/research-notes.md` for how the videos were chosen and checked.

If you add or rename files, also bump `CACHE` in `sw.js` so phones pick up the change.

## Where the log is saved

The workout log is stored in the phone's browser (`localStorage`, key `vbtrainer.log.v1`). It survives closing the browser, but not clearing browser data or switching phones. Use **Log → Export JSON** to back it up and **Import JSON** to restore it. **Export CSV** opens in Excel, Numbers or Google Sheets.

## Run locally

```sh
python3 -m http.server 8000
```

Then open <http://localhost:8000>. Opening the HTML files directly from disk does not work, because the pages load their data with `fetch`.

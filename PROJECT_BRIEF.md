# Volleyball Trainer App — Claude Code Project Brief

Oct 24, 2026 · @Vozza

## Project overview

Build a small, phone-friendly HTML web app that acts as a personal trainer and workout log for a 13-year-old volleyball player during her 5-week off-season. It has two parts, built in this order:

1. **Video database first.** Claude Code does a deep web search and builds a structured database of demonstration videos, one entry per exercise, before any app code is written.
2. **The app second.** Daily workout pages list each exercise with sets, reps and a hyperlink to that exercise on a single Exercise Library page, where its video plays. She checks off sets, logs how it felt, and sees her progress.

The app must work without a build step or server so it can be shared as a link (GitHub Pages or similar) and opened on her phone at the gym or pool.

## Athlete and training context

She is 13, plays libero and defensive specialist, is tall, and wants to develop her serve and spike. Season starts November 30, so the off-season block runs Monday, October 26 to Sunday, November 29.

| Item | Detail |
| --- | --- |
| Schedule | 2 workouts per week (Day A and Day B, non-consecutive, e.g. Mon/Thu); when a swim is included it comes at the end of the session |
| Session length | About 90 minutes |
| Phases | Weeks 1–2 Foundation, Weeks 3–4 Build, Week 5 Taper (Thanksgiving week) |
| Equipment | Bodyweight, one light dumbbell, resistance bands, a low box or step, a volleyball, pool access |
| Priorities | Landing mechanics and knee control, hip and hamstring strength, shoulder care, approach jump, defensive movement |

Safety rules the app must surface: stick every landing, at least one full rest day per week, and stop and tell a parent if she has pain below the kneecap, at the heel, or in the shoulder.

## Phase 1: Build the video database

Claude Code searches the web and produces `data/exercises.json`, with one verified demonstration video (plus a backup) for every exercise in the next section. No app code is written until this file is reviewed.

**Selection criteria, in priority order**

1. Shows the exercise clearly, from the side or front, with correct form.
2. Short: under 3 minutes, or a timestamp pointing to the demo inside a longer video.
3. Appropriate for a teen athlete: no heavy loading, no hype, no ads-first content.
4. From a credible coach, team, or organization. Start with these sources: FIFA 11+ (official injury-prevention program), The Art of Coaching Volleyball, Project Pure Athlete (Tyler Ray, Chase Skinkis), Overtime Athletes (Chris Barnard), USA Volleyball, and physical-therapy channels for band and shoulder work.
5. Prefer female or youth athletes in the demo when quality is equal.

**Verification**

- Open every URL and confirm it is live, public, embeddable, and actually demonstrates that exercise.
- Record the video title and channel exactly as shown.
- Never invent or guess a video ID. If nothing good is found, set `status` to `needs_review` and leave a note.

**Schema for each entry**

```json
{
  "id": "split-squat",
  "name": "Split Squat",
  "category": "strength",
  "cues": ["Front knee over toes", "Back knee drops straight down", "Tall chest"],
  "video": {"youtubeId": "", "start": 0, "title": "", "channel": "", "url": ""},
  "backup": {"youtubeId": "", "start": 0, "title": "", "channel": "", "url": ""},
  "status": "verified",
  "notes": ""
}
```

Also output a short `data/research-notes.md` listing every source considered and why it was chosen or rejected.

## Exercise list

These 26 exercises need a video. The `id` column is the anchor the app links to (`library.html#split-squat`).

| id | Exercise | Category | Search hint |
| --- | --- | --- | --- |
| fifa-11-warmup | FIFA 11+ warm-up (Part 1 running drills) | Warm-up | Official FIFA 11+ videos |
| snap-down | Snap-downs | Landing | Snap down drill landing mechanics |
| box-step-down-stick | Step off box and stick landing | Landing | Drop landing, stick, knee alignment |
| approach-footwork | Volleyball approach footwork (3- and 4-step) | Volleyball | Art of Coaching Volleyball approach |
| approach-jump | Approach jump with arm swing | Jumps | Tyler Ray volleyball approach jump |
| squat-jump | Squat jump | Jumps | Squat jump stick landing |
| pogo-hops | Pogo hops | Jumps | Ankle pogo hops plyometric |
| lateral-bound | Lateral bounds with stick | Jumps | Lateral bound skater stick |
| bodyweight-squat | Bodyweight squat | Strength | Bodyweight squat form youth |
| goblet-squat | Goblet squat | Strength | Dumbbell goblet squat form |
| split-squat | Split squat | Strength | Split squat form |
| rfe-split-squat | Rear-foot elevated split squat | Strength | Bulgarian split squat beginner |
| glute-bridge | Glute bridge | Strength | Glute bridge form |
| single-leg-glute-bridge | Single-leg glute bridge | Strength | Single leg glute bridge |
| single-leg-rdl | Single-leg RDL (bodyweight and dumbbell) | Strength | Single leg Romanian deadlift |
| calf-raise | Calf raises | Strength | Calf raise form |
| plank | Plank | Core | Plank form |
| side-plank | Side plank | Core | Side plank form |
| shuffle-to-dig | Shuffle-to-dig drill | Volleyball | Libero defensive footwork drill |
| reaction-drill | Defensive reaction drill (partner point or toss) | Volleyball | Volleyball reaction drill at home |
| serving | Serving practice (float serve) | Volleyball | Art of Coaching Volleyball float serve |
| band-external-rotation | Band external rotation | Shoulder | Band shoulder external rotation |
| band-ytw | Y-T-W raises | Shoulder | YTW shoulder exercise |
| band-scap-retraction | Band scap retraction (pull-apart) | Shoulder | Band pull-apart scapular retraction |
| swim-kick-set | Kick sets with kickboard | Swim | Freestyle kick drill kickboard |
| backstroke | Backstroke technique | Swim | Backstroke technique beginner |

## Training program

Each session runs about 90 minutes in the order below. Jump and strength volume stays as listed in the tables; the extra time goes to volleyball skills, full rest between sets, and swimming, which always comes last.

| Block | Minutes | Content |
| --- | --- | --- |
| Warm-up | 10 | FIFA 11+ Part 1 running drills, then snap-downs 2×5 |
| Jumps | 15 | That day's jump exercises, 60–90 s rest between sets |
| Strength and core | 20 | That day's strength and core exercises |
| Volleyball skills | 15 with swim, 35 without | Serving, passing, approach footwork, defensive drills |
| Shoulder care | 5 | Band external rotations, Y-T-W raises, scap retractions, 2×12 each |
| Swim (when scheduled) | 25–30 | Always the final block; see below |
| Cool-down (no-swim days) | 5 | Easy walk and stretching |

A blank cell in the tables below means the exercise is not done that phase.

**Day A: jumps and leg strength**

| Exercise | Weeks 1–2 | Weeks 3–4 | Week 5 |
| --- | --- | --- | --- |
| Approach footwork (half speed) | 3×4 |  |  |
| Approach jump (full effort) |  | 4×3 | 3×3 |
| Squat jump | 3×4 |  |  |
| Lateral bound |  | 2×4 per side |  |
| Bodyweight squat | 3×10 |  |  |
| Goblet squat |  | 3×8 | 2×6 |
| Split squat | 3×8 per leg |  | 2×6 per leg |
| Rear-foot elevated split squat |  | 3×6 per leg |  |
| Glute bridge | 3×12 |  |  |
| Single-leg glute bridge |  | 2×10 per leg |  |
| Side plank | 2×20 s per side |  |  |

**Day B: volleyball movement and posterior chain**

| Exercise | Weeks 1–2 | Weeks 3–4 | Week 5 |
| --- | --- | --- | --- |
| Pogo hops | 2×10 | 2×12 | 2×10 |
| Shuffle-to-dig | 4×20 s |  |  |
| Lateral bound |  | 3×4 per side |  |
| Defensive reaction drill |  | 5×15 s | 4×15 s |
| Single-leg RDL | 2×8 per leg (bodyweight) | 3×8 per leg (dumbbell) | 2×6 per leg |
| Calf raise | 2×15 |  |  |
| Plank | 3×30 s |  |  |
| Serving practice | 15 min | 15 min | 15 min |

**Swim (end of session, on 1 or both workouts per week):** 25–30 minutes, always after the dryland work so jumps and lifts are done fresh. Mostly easy freestyle with kick sets and backstroke. In weeks 3–4, add 6–8 × 50 yards at a strong pace with 30 seconds rest. On days with a lot of serving, keep the swim easy and kick-heavy to spare the shoulder. Week 5: easy swimming only.

## Phase 2: Build the app

Plain HTML, CSS and JavaScript with no framework or build step. The program and the video database live in JSON files, so changing a workout never means editing page code.

**Pages**

| Page | Purpose |
| --- | --- |
| `index.html` | Dashboard: today's workout, the 5-week calendar with completed days marked, a countdown to November 30, and a streak count |
| `workout.html?week=3&day=A` | One day's 90-minute session in order: warm-up, jumps, strength, volleyball skills, shoulder routine, then swim when scheduled, with a time budget per block. Each exercise shows sets, reps, cues, and a link to its video |
| `library.html` | All exercises grouped by category, each with an `id` anchor, its video, and coaching cues. Videos load only when tapped (thumbnail first) so the page stays fast |
| `log.html` | History of every session, per-exercise progress, and export/import buttons |

**Logging features**

- A checkbox per set, plus optional reps or weight when they differ from the plan.
- After each session: effort rating 1–5, minutes, and a notes field.
- Pain check: knee, heel, or shoulder. If any is ticked, show a clear message to rest and tell a parent.
- A separate swim log: minutes, distance in yards, and which sets were done.
- Export the full log as JSON and CSV, and import it back. This covers phone changes and lets a parent review it.

**Data files**

- `data/exercises.json` from Phase 1.
- `data/program.json` holds weeks 1–5, Day A and Day B, each a list of `{exerciseId, sets, reps, unit, perSide}`, plus the session blocks with their minutes, which sessions include a swim, and the swim plan.
- The workout log is saved in the browser's localStorage under one versioned key. Reads and writes are wrapped in try/catch, and the app works with an empty log.

**Design and tech rules**

- Mobile-first, large tap targets, readable at arm's length, light and dark mode.
- Video embeds use `youtube-nocookie.com` with the `start` time from the database. If a video fails, show the backup link.
- Works offline after first load if practical (a simple service worker is a stretch goal).
- Hosted free on GitHub Pages so it can be shared as a link.

## Milestones and kickoff

The app should be in her hands by Monday, October 26, the first training day, even if the log page comes a few days later.

- [ ] Phase 1: `exercises.json` complete, every entry `verified` or flagged, research notes written
- [ ] Parent review: watch each video and swap any that are not right
- [ ] `program.json` written from the Training program tables
- [ ] Workout and library pages working, links jump to the right video
- [ ] Logging, pain check, and export/import working
- [ ] Published to GitHub Pages and tested on her phone

**Done means:** every exercise on every workout page links to a working video; a full session can be logged on a phone in under 2 minutes of tapping; the log survives closing the browser; and an export opens cleanly in a spreadsheet.

**Kickoff prompt for Claude Code**

Save this document as `PROJECT_BRIEF.md` in an empty project folder, then paste:

```markdown
Read PROJECT_BRIEF.md. Start with Phase 1 only.
Search the web and build data/exercises.json for every exercise in the Exercise list, following the selection criteria, verification rules and schema exactly.
Open and check every video before adding it. Never guess a video ID.
Write data/research-notes.md as you go.
When finished, stop and give me a summary table of each exercise, the chosen video, its channel, and its status so I can review before we build the app.
```

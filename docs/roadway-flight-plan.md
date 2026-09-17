# Roadway Inspection — Shoulder Flight Plan

Manual flight plan for documenting a roadway. Flight lines run **along the
shoulders**, parallel to the roadway. No grid.

Method and reasoning: [roadway-uas-flight.md](roadway-uas-flight.md) ·
Terms: [glossary.md](glossary.md)

---

## 1. Terminology used throughout

| Term | Meaning |
|---|---|
| **Side 1** | One side of the roadway. Fix which one at the start of the job and keep it for the whole project — it goes in the file names. |
| **Side 2** | The opposite side. |
| **Rotate drone parallel to roadway** | Nose pointed up-station or down-station, along the centerline. Flight direction. |
| **Rotate drone perpendicular to roadway** | Nose pointed across the roadway, 90° to the centerline. Used to translate between sides and for crossings. |
| **Up-station / down-station** | Direction of travel along the roadway. Pick a start end and call it station 0. |
| **Shoulder separation** | Across-track distance between the Side 1 line and the Side 2 line. Governs everything in §2. |

**All gimbal angles below are as the DJI controller displays them** — negative,
where **−90° is straight down**.

| DJI display | Looking |
|---|---|
| **−90°** | Straight down (nadir) |
| **−55°** | Calibration oblique — 35° off nadir |
| **−45°** | Detail oblique |
| **−30°** | Vertical faces: barrier, guardrail, sign structures |

---

## 2. The constraint that shoulder flying imposes

Flying the shoulders fixes your line separation at the road width. You cannot
adjust it. **That means altitude — not line spacing — is what sets your side
overlap**, and there is a hard floor below which two shoulder lines stop
overlapping usefully.

Measure your shoulder separation, then read the floor off this table:

| Shoulder separation | Min. altitude for 60% side overlap | For 70% |
|---|---|---|
| 40 ft | 71 ft | 95 ft |
| 60 ft | 107 ft | 142 ft |
| **80 ft** (typical 2-lane + shoulders) | **142 ft** | **189 ft** |
| 100 ft | 178 ft | 237 ft |
| 120 ft (divided) | 213 ft | 284 ft |

**The rule: minimum altitude ≈ 1.8 × your shoulder separation.** For 70%
overlap, 2.4 ×.

At an 80 ft separation, two shoulder lines give you:

| AGL | Frame width | Side overlap | Verdict |
|---|---|---|---|
| 200 ft | 282 ft | 72% | Good |
| 150 ft | 211 ft | 62% | Adequate |
| 120 ft | 169 ft | 53% | **Add a centre pass** |
| 100 ft | 141 ft | 43% | **Add a centre pass** |
| 80 ft | 113 ft | 29% | **Add a centre pass** |
| 60 ft | 84 ft | 5% | **Add a centre pass** |

### The consequence

**Below ~1.8 × separation, add a third pass down the centre of the roadway.**
That halves the effective separation and restores overlap:

| AGL | 2 shoulder lines | + centre pass |
|---|---|---|
| 120 ft | 53% ✗ | **76%** ✓ |
| 100 ft | 43% ✗ | **72%** ✓ |
| 80 ft | 29% ✗ | **64%** ✓ |

This is not a grid. It is one more parallel pass down the middle, flown exactly
like the shoulder passes.

Run it for your own road width:

```sh
tools/flight-calc.py --alt-ft 200 150 120 100 80 --front 90 --line-sep 80
```

---

## 3. Altitude tiers and shot spacing

Forward overlap of **90%** throughout — hand-flown spacing is irregular, so 90%
nominal keeps the worst interval above the 85% corridor minimum.

| AGL | GSD | Frame length | **Shot every** | Max speed @ 2 s |
|---|---|---|---|---|
| 200 ft | 1.63 cm (0.64 in) | 211 ft | **21 ft** | 3.2 m/s |
| 150 ft | 1.22 cm (0.48 in) | 158 ft | **16 ft** | 2.4 m/s |
| **120 ft** | **0.98 cm (0.38 in)** | 127 ft | **13 ft** | 1.9 m/s |
| 100 ft | 0.81 cm (0.32 in) | 105 ft | **11 ft** | 1.6 m/s |
| 80 ft | 0.65 cm (0.26 in) | 84 ft | **8 ft** | 1.3 m/s |
| 60 ft | 0.49 cm (0.19 in) | 63 ft | **6 ft** | 1.0 m/s |

**Max speed is the fastest you can fly and still hold overlap at a 2 s
interval.** Flying faster silently thins it. If you are shooting DNG, the RAW
interval is longer — halve these speeds for a 5 s interval.

**Judge spacing by the frame, not by ground distance:** at 90% forward overlap
you advance one tenth of a frame per shot. Pick a feature at the leading edge
of the screen; when it has travelled one tenth of the way down, shoot.

---

## 4. Pass sequence

Six passes per tier at the primary altitude, fewer at the others. Each pass is
a single parallel run — out on one side, back on the other.

Throughout: **stop, wait for traffic to clear, shoot, advance.** Never coast
while waiting — overlap is a function of distance, not time, so hovering costs
you nothing geometrically while coasting opens a gap exactly as long as your
patience.

### Pass 1 — Side 1, nadir, outbound

1. [ ] Take off from the Side 1 shoulder at station 0
2. [ ] Climb to tier altitude
3. [ ] **Rotate drone parallel to roadway**, nose down-station
4. [ ] Set gimbal **−90°**
5. [ ] Position over the **Side 1** shoulder
6. [ ] Fly down-station at the tier's shot spacing, holding the shoulder line
       by keeping the pavement edge at a constant position in frame

### Pass 2 — Side 2, nadir, return

7. [ ] At the end station, **rotate drone perpendicular to roadway**
8. [ ] Translate across to the **Side 2** shoulder
9. [ ] **Rotate drone parallel to roadway**, nose up-station
10. [ ] Gimbal stays **−90°**
11. [ ] Fly up-station at the same spacing, back to station 0

### Pass 3 — Centre, nadir *(only below 1.8 × separation — see §2)*

12. [ ] **Rotate drone perpendicular to roadway**, translate to the centerline
13. [ ] **Rotate drone parallel to roadway**, nose down-station
14. [ ] Gimbal **−90°**, fly the full length

### Pass 4 — Side 1, oblique, looking across at Side 2

15. [ ] Return to the **Side 1** shoulder, **rotate drone parallel to roadway**
16. [ ] Set gimbal **−55°**, camera looking **across the roadway toward Side 2**
17. [ ] Fly the full length at the tier's shot spacing

> **This is the pass that prevents doming.** With no grid and no crosshatch,
> the obliques are doing all the work of breaking the focal-length/altitude
> correlation. On a shoulder-only plan they are not optional.

### Pass 5 — Side 2, oblique, looking across at Side 1

18. [ ] **Rotate drone perpendicular to roadway**, translate to **Side 2**
19. [ ] **Rotate drone parallel to roadway**
20. [ ] Gimbal **−55°**, camera looking **across the roadway toward Side 1**
21. [ ] Fly the full length

> Passes 4 and 5 together give every vertical face — barrier, guardrail, sign
> back, curb, cut slope — two opposing viewpoints. A single oblique pass leaves
> one face of everything unobserved.

### Pass 6 — Perpendicular crossings

22. [ ] Every **1000–1600 ft** along the roadway, stop
23. [ ] **Rotate drone perpendicular to roadway**, gimbal **−90°**
24. [ ] Cross the full width, past the shoulder on both sides, shooting
25. [ ] **Rotate drone parallel to roadway** and resume

> A handful of frames each. These tie the Side 1 and Side 2 lines together at
> intervals instead of only at the ends, and they are the main defence against
> the corridor bending along its length. *(Spacing here is my engineering
> judgment, not a sourced figure.)*

### Pass 7 — Altitude profiles

26. [ ] At **both ends and the middle** of the run, hold position laterally
27. [ ] Climb or descend in **~25 ft steps**, shooting at each step
28. [ ] **Alternate gimbal −90° → −55° → −90°** as you go

> Varying height decouples focal length from flying height in the solve. This
> is the one thing a grid-flown mission usually lacks and you already do.
> *(Step size is judgment, not sourced.)*

### Pass 8 — Detail, AOI only

29. [ ] Drop to 60 ft or lower over the specific area of interest
30. [ ] **Rotate drone parallel to roadway**, gimbal **−90°**, fly Side 1,
        centre, Side 2 — three short passes
31. [ ] Repeat at gimbal **−45°** for pavement texture, joints, edges, distress
32. [ ] Gimbal **−30°** for barrier faces, guardrail, sign structures
33. [ ] Two orbits around any structure, camera held on it — one each direction

---

## 5. Tier plan

| Tier | Passes | Purpose |
|---|---|---|
| **200 ft** | 1, 2 (nadir only) | Overview, context, good side overlap from shoulders alone |
| **120 ft** ★ | 1, 2, 3, 4, 5, 6 | **Primary deliverable tier** — 0.98 cm GSD |
| 60 ft and below | 8 | AOI detail only |
| Between tiers | 7 | Altitude profiles |

★ If the day gets cut short, the 120 ft tier — nadir passes plus obliques — is
what you protect. Everything else strengthens or refines it.

---

## 6. Ground control

Because the flight lines are collinear with the roadway, **control must not
be.** A straight line of GCPs down the centerline leaves the block free to roll
about that axis, and shoulder-only flying gives the solve little else to resist
it with.

- [ ] **Zigzag: alternate Side 1 and Side 2**, every 400–500 ft
- [ ] **A pair at each end** of the run — both ends
- [ ] **Vary the height** where terrain allows: embankment top and bottom, on
      structures. This decorrelates focal length from altitude, the same
      mechanism the obliques and profiles address
- [ ] **Check points interleaved**, roughly every third position, withheld from
      the solve — your only real accuracy measure
- [ ] Targets **50–60 cm**; confirm each is visible in **≥8–10 frames**

The Mavic 3 Classic has no RTK, so this is mandatory, not optional.

---

## 7. Naming

Side designation goes in the file name so it survives into processing:

```
<SITE>_<YYYYMMDD>_UAS_S1N_0001.JPG     Side 1, nadir
<SITE>_<YYYYMMDD>_UAS_S2N_0001.JPG     Side 2, nadir
<SITE>_<YYYYMMDD>_UAS_S1O_0001.JPG     Side 1, oblique
<SITE>_<YYYYMMDD>_UAS_CTR_0001.JPG     Centre pass
<SITE>_<YYYYMMDD>_UAS_XNG_0001.JPG     Perpendicular crossings
<SITE>_<YYYYMMDD>_UAS_PRF_0001.JPG     Altitude profiles
```

```sh
tools/rename-uas-images.sh SITE 20260917 S1N <src> <dest>
```

See [naming-convention.md](naming-convention.md).

---

## 8. Processing

- **Import every pass into one project.** The altitude spread across tiers and
  profiles is what calibrates the lens — splitting tiers into separate projects
  throws that away
- **Enable rolling shutter correction** (linear) — the Mavic 3 Classic is
  electronic-shutter only
- Ortho from **Pix4D** (use PIX4Dmatic for a long run), dense cloud and mesh
  from **RealityCapture**
- Mark GCPs in ≥8–10 images each; set point accuracy to your survey accuracy,
  not the GNSS default
- Import check points but **exclude them from the solve**
- Target check point RMSE ≤ 2–3× GSD — at 120 ft that is **≤ 2–3 cm**
- Mask any vehicles you could not avoid, before ortho generation

---

## 9. What a shoulder-only plan gives up, and how it is covered

Honest accounting, since dropping the grid removes redundancy:

| Lost | Covered by |
|---|---|
| Crosshatch geometry | Passes 4–5 obliques + Pass 6 crossings |
| Wide side overlap at low altitude | Pass 3 centre line below 1.8 × separation |
| Coverage outside the ROW | Accepted — the roadway is the deliverable |
| Redundant viewpoints per point | 90% forward overlap, and the oblique pair |

The residual risk is **longitudinal bending on a long run**. Passes 6 and 7 and
the zigzag control are what hold it. On a run longer than about a mile, add
crossings more often rather than less.

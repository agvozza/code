# Worked Flight Plan — Roadway Site (Manual Flight)

A concrete, step-by-step manual flight for a compact roadway site: a ~450 × 400 ft
scan region containing a smaller area of interest on the pavement.

Method and reasoning: [roadway-uas-flight.md](roadway-uas-flight.md).
Unfamiliar terms: [glossary.md](glossary.md).

---

## 0. Where these numbers come from

Every distance, count and speed below is produced by
[`tools/flight-calc.py`](../tools/flight-calc.py) from the Mavic 3 Classic's
published sensor geometry (17.3 mm sensor across 5280 px, 12.29 mm focal
length), at a stated overlap. Re-run it and the numbers change with your
inputs:

```sh
tools/flight-calc.py --alt-ft 200 120 80 --front 90 --side 70 \
                     --site-along 450 --site-across 400
```

Overlap figures (85% forward / 60% side for corridors) come from Pix4D's
published acquisition specification. The oblique angle comes from the overlap of
two independent studies. **Two numbers in the previous document were my
engineering judgment rather than sourced**: cross-tie spacing of 1000–1600 ft
and altitude-profile steps of 25–50 ft. They are reasonable, but treat them as
judgment. Everything else traces to a source or to the calculator.

**Site dimensions below are estimated from your screenshot** by scaling off the
roadway width (~60 ft of pavement) and vehicles in the salvage lot (~15 ft).
That puts the yellow polygon at roughly **320 ft along the road × 270 ft deep**,
and the image at roughly 0.75 ft per pixel. **Verify this before flying** — measure
the polygon in Google Earth or your mapping app. If your real dimensions differ
by more than ~25%, re-run the calculator; the altitudes hold but the line and
image counts scale.

The flight block is sized at **450 × 400 ft**, deliberately larger than the
polygon. Coverage and control must extend past the area of interest, or the
edges of your deliverable are extrapolated and distort.

---

## 1. Two corrections before anything else

### 1.1 "1/3 overlap" will fail

This is the most important line in this document.

Read as *"consecutive images share about a third of their content"* → **33%
overlap**. Read as *"advance a third of a frame each shot"* → **67% overlap**.
Both are too low, and the first is far too low.

Photogrammetry works by finding the same feature in **many** overlapping images.
At 33% overlap a given point appears in two frames at best, often one. There is
no redundancy, the **bundle adjustment** has nothing to work with, and the usual
result is either a failed alignment or a model that aligns and is quietly wrong.
Low overlap also *amplifies* **doming**, because weak **tie point** geometry is
exactly what lets lens distortion go unconstrained.

| Overlap | Result |
|---|---|
| 33% | Alignment failure or garbage |
| 60% | Absolute floor, general mapping only |
| 75–80% | Standard area mapping |
| **85% fwd / 60% side** | **Pix4D's corridor specification** |
| **90% fwd / 70% side** | **Use this — manual-flight margin** |

At 90% forward overlap you advance **one tenth of a frame** per shot, not one
third. That is the single biggest change to make.

The cost is only storage. The benefit is a model that solves.

### 1.2 400 ft is not a mapping altitude for this site

At 400 ft AGL a single frame covers **563 × 422 ft** — larger than your entire
scan region. A "grid" at that height over this site is 4 lines and ~48 images:
that is a snapshot, not a photogrammetric block.

| AGL | GSD | Frame | Lines | Images (grid + crosshatch) |
|---|---|---|---|---|
| 400 ft | 3.25 cm | 563 × 422 ft | 4 | 48 → 92 — *too coarse, too few* |
| **200 ft** | **1.63 cm** | 282 × 211 ft | 6 | **138 → 278** |
| **120 ft** | **0.98 cm** | 169 × 127 ft | 9 | **333 → 663** |
| 80 ft | 0.65 cm | 113 × 84 ft | 13 | 715 → 1450 — *reserve for AOI* |

Your 400/200/100 ladder is right for a long corridor. **For a site this size,
compress it to 200 / 120, with 80 ft and below reserved for the AOI only.** Fly
400 ft if you want a context photo or for recon — just don't count it as a
mapping tier.

---

## 2. Gimbal convention

You wrote "gimbal at 90°" for straight down. DJI Fly displays that as **−90°**.
Both appear below so there is no ambiguity:

| Looking | Your convention | DJI display | Off nadir |
|---|---|---|---|
| Straight down (**nadir**) | 90° | **−90°** | 0° |
| **Calibration oblique** | **55–60°** | **−55° to −60°** | **30–35°** |
| Detail oblique | 45° | −45° | 45° |
| Asset / vertical faces | 20–30° | −20° to −30° | 60–70° |

**Your example used 80° (−80°), which is only 10° off nadir.** That is too
shallow to do anything useful — it is effectively still a nadir image and does
not break the focal-length/height correlation. The calibration oblique needs to
be **55–60°**.

---

## 3. Site-specific notes from your image

- **Active traffic.** Vehicles are visible on the roadway. Your shot-timing
  method matters here — see [§3.1](roadway-uas-flight.md#31-the-one-rule-that-makes-traffic-timing-free-hover-dont-coast):
  stop, wait, shoot, advance. Never coast while waiting.
- **Parked cars in the salvage lot are fine.** Stationary objects reconstruct
  correctly. Only *motion between frames* corrupts. Don't wait on them.
- **The fuel canopy** at lower left is a tall obstruction and casts a hard
  shadow. Note its height before descending, and prefer overcast or high sun.
- **Trees at lower right move in wind** — the same matching problem as vehicles,
  and unavoidable. Fly the treed edge on a calm day if you can.
- **Railroad along the top edge** — outside the scan region, but confirm it
  doesn't affect your airspace or standoff.
- **Check for overhead utility lines** along the roadway before descending
  below ~80 ft. They are hard to see in imagery and hard to see in flight.

---

## 4. Ground control — place before you fly

For a block this size: **6 control points + 3 check points.**

1. [ ] `GCP01`–`GCP06`: **zigzag alternating sides of the roadway**, roughly
       every 120–150 ft along it, plus one at each far corner of the polygon.
       Never collinear down the centerline.
2. [ ] At least **two at different elevations** if terrain allows — the
       embankment down toward the trees, or the raised lot edge. Varied height
       is what decorrelates focal length from altitude.
3. [ ] `CHK01`–`CHK03`: interleaved, **withheld from the solve**. These are
       your only real accuracy measure.
4. [ ] Targets **50–60 cm**, per the ≥5× GSD rule.
5. [ ] Photograph each in place with its ID visible.

Your Mavic 3 Classic has no **RTK**, so this is mandatory, not optional.

---

## 5. Step-by-step flight

Gimbal values are given in your convention (90° = down) with DJI display in
parentheses. **Throughout: stop, wait for traffic to clear, shoot, advance.**

### Pre-flight

1. [ ] Verify site dimensions against the estimate in §0
2. [ ] Check airspace; confirm **VLOS** from your launch point covers the block
3. [ ] Walk the site; note the canopy height, any overhead lines, launch point
4. [ ] Place GCPs per §4
5. [ ] Camera: **manual exposure**, manual white balance, focus at infinity,
       no CPL, **JPEG + DNG**, **single-shot mode — not timed interval**
6. [ ] Write on your card: *200 ft → shot every 21 ft; 120 ft → every 13 ft;
       80 ft → every 8 ft*

### Warm-up

7. [ ] Take off, climb to 200 ft over the site centre
8. [ ] **Hover 2–3 minutes.** Lens distortion parameters shift with
       temperature; a cold first frame is calibrated differently from a warm
       last one. Do not skip this — it costs one battery-minute.

### Flight 1 — 200 ft overview block · gimbal 90° (−90°)

9. [ ] Position at a corner of the 450 × 400 ft block
10. [ ] Orient the aircraft to fly **parallel to the roadway** (along the
        polygon's long axis)
11. [ ] Fly line 1 with a **shot every 21 ft** — one tenth of a frame length.
        Judge it by watching a feature travel one tenth of the way down your
        screen, not by estimating ground distance
12. [ ] At the end of the line, step **84 ft sideways**, reverse, fly line 2
13. [ ] Repeat for **6 lines total** (~23 shots each, ~138 images)

### Flight 2 — 200 ft crosshatch · gimbal 90° (−90°)

14. [ ] Turn 90°: fly the same block with lines **perpendicular to the roadway**
15. [ ] Same 21 ft spacing, 84 ft line step, ~6 lines (~140 images)

This is the "turn the drone 90°" step in your example, and your instinct is
right — it is a **crosshatch**, and it materially strengthens the block.

### Flight 3 — 200 → 120 ft altitude profile

16. [ ] Move to the site centre, hold position laterally
17. [ ] Descend in **~25 ft steps**, shooting at each step
18. [ ] **Alternate gimbal: 90°, then 55°, then 90°…** as you descend. A
        pure-nadir stack shares the same degenerate geometry as everything
        else; alternating makes the profile a calibration asset
19. [ ] Repeat at **two more locations** — opposite ends of the block. Three
        profiles, ~4 frames each

### Flight 4 — 120 ft primary mapping block · gimbal 90° (−90°)

This is your workhorse tier: **0.98 cm GSD**, sub-centimetre.

20. [ ] Lines **parallel to the roadway**, **shot every 13 ft**, line step
        **51 ft**, **9 lines** (~37 shots each, ~333 images)

### Flight 5 — 120 ft crosshatch · gimbal 90° (−90°)

21. [ ] Perpendicular lines, same spacing (~330 images)

### Flight 6 — 120 ft calibration obliques · gimbal 55–60° (−55° to −60°)

**The pass currently missing from your method, and the one that prevents doming.**

22. [ ] Set gimbal to **55–60°** and leave it — it holds position, so this is no
        harder to hand-fly than nadir
23. [ ] Fly a pass down **one side** of the block, camera pointed **inward** at
        the roadway, shot every 13 ft
24. [ ] Fly the return pass down **the other side**, again pointed **inward**
25. [ ] Every vertical face — guardrail, signage, embankment, the canopy — is
        now seen from two opposing directions. A single oblique pass leaves one
        face of everything unobserved

### Flight 7 — 80 ft AOI block · gimbal 90° (−90°)

Tighten to roughly **150 × 100 ft** around the blue AOI.

26. [ ] Nadir grid: **shot every 8 ft**, line step 34 ft, ~4 lines (~76 images)
27. [ ] Crosshatch the same area (~78 images)

### Flight 8 — 50 ft AOI detail · gimbal 90° and 45°

28. [ ] Nadir grid at **0.41 cm GSD**: shot every 5 ft, ~6 lines (~180 images)
29. [ ] Second pass at gimbal **45° (−45°)** over the same area for pavement
        texture, edges, joints and any distress detail
30. [ ] **Two orbits** around the AOI at 50 ft, gimbal 45°, camera held on the
        AOI centre — one clockwise, one counter-clockwise

### Before leaving

31. [ ] Frame counts compared against the expected totals below
32. [ ] Every GCP confirmed visible in **≥8–10 frames** — if in doubt, fly back
        over it and take a few more
33. [ ] Cards backed up before anything is formatted
34. [ ] Rename per flight:
        `tools/rename-uas-images.sh SITE 20260917 F01 <src> <dest>`

---

## 6. Expected totals

| Flight | Tier | Gimbal | Images |
|---|---|---|---|
| 1–2 | 200 ft grid + crosshatch | 90° | ~278 |
| 3 | Altitude profiles ×3 | 90°/55° alt. | ~40 |
| 4–5 | 120 ft grid + crosshatch | 90° | ~663 |
| 6 | 120 ft obliques, both sides | 55–60° | ~150 |
| 7 | 80 ft AOI + crosshatch | 90° | ~154 |
| 8 | 50 ft AOI + oblique + orbits | 90°/45° | ~350 |
| | | **Total** | **~1,600** |

**Batteries: plan 5–6.** Manual flight with traffic waits typically loses
30–50% of airtime to hovering, so budget well above the flight-time arithmetic.
Overlap consecutive battery segments by several frames, and resume a few frames
*behind* where you stopped.

If the day is cut short, the tiers to protect in order are: **120 ft nadir grid
→ 120 ft obliques → 200 ft block → AOI detail.** The 120 ft pair is the
deliverable; everything else strengthens or refines it.

---

## 7. Processing

Per [workflow.md](workflow.md): ortho from Pix4D, dense cloud and mesh from
RealityCapture.

- Enable **rolling shutter correction** (linear) — the Mavic 3 Classic is
  electronic-shutter-only
- Import all tiers into **one project**. The altitude spread is what calibrates
  the lens; splitting tiers into separate projects throws that away
- Mark GCPs in ≥8–10 images each; set point accuracy to your survey accuracy,
  not the GNSS default
- Import check points but **exclude them from the solve**
- Target check point RMSE ≤ 2–3× GSD. At the 120 ft tier's 0.98 cm GSD that is
  **≤ 2–3 cm**
- Mask any vehicles you could not avoid, before ortho generation

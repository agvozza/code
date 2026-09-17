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

## 2. The constraint: aircraft stays off the roadway

**14 CFR 107.145** prohibits operating a small UA over a moving vehicle. The
aircraft stays over the shoulder for the whole job. That is a hard constraint,
and it drives every geometric decision below.

The camera, however, does not have to be above what it photographs. **Tilt the
gimbal instead of moving the aircraft.**

### 2.1 Why nadir alone fails at low altitude

Flying the shoulders fixes your line separation at the road width — you cannot
respace it. So altitude, not line spacing, sets side overlap between the Side 1
and Side 2 nadir passes:

| Shoulder separation | Min AGL for 60% overlap | For 70% |
|---|---|---|
| 40 ft | 71 ft | 95 ft |
| 60 ft | 107 ft | 142 ft |
| **80 ft** (2-lane + shoulders) | **142 ft** | **189 ft** |
| 100 ft | 178 ft | 237 ft |
| 120 ft (divided) | 213 ft | 284 ft |

**Rule: minimum altitude for nadir ≈ 1.8 × shoulder separation.**

Below that floor the two nadir frames barely reach past the centerline — at
80 ft separation and 120 ft AGL they share only 53%, and the middle of the
roadway ends up with the thinnest geometry on the whole job. Previously the fix
was a third pass down the centre. **That is not available**, so the fix is
different:

### 2.2 The fix: cross-aimed oblique passes

Keep the aircraft over the shoulder, **rotate it perpendicular to the roadway**
so the nose points across, tilt the gimbal to put the roadway in frame, and
translate sideways along the shoulder.

The gimbal angle that aims at the centerline depends on altitude, because the
lateral offset is fixed and the height is not. For a **40 ft offset** —
shoulder to centerline on a typical 2-lane:

| AGL | Gimbal (DJI) | Off nadir | GSD at aim point | Shot every |
|---|---|---|---|---|
| 150 ft | **−75°** | 15° | 1.26 / 1.31 cm | 22 ft |
| 120 ft | **−72°** | 18° | 1.03 / 1.08 cm | 18 ft |
| 100 ft | **−68°** | 22° | 0.88 / 0.94 cm | 15 ft |
| **80 ft** | **−63°** | 27° | **0.73 / 0.81 cm** | 13 ft |
| 60 ft | **−56°** | 34° | 0.59 / 0.70 cm | 10 ft |

Compute it for your own offset:

```sh
tools/flight-calc.py --alt-ft 120 100 80 60 --front 90 --offset 40
```

**Three things worth noticing:**

1. **The GSD cost is small.** At 80 ft AGL, aiming across at the centerline
   gives 0.73 cm instead of 0.65 cm nadir — about 12%. You are not giving up
   meaningful resolution to stay legal.
2. **Shot spacing gets *wider*, not tighter.** Yawing the aircraft across the
   roadway puts the sensor's long axis (5280 px) along the flight path, so at
   80 ft you advance 13 ft between shots instead of the 8 ft a nadir pass
   needs. Fewer frames for the same coverage.
3. **GSD is quoted across-look / along-look.** An oblique frame is foreshortened
   in the direction it looks, so the along figure is what limits what you can
   resolve. At these angles the difference is minor.

### 2.3 The resulting rule

| Altitude | How to cover the roadway |
|---|---|
| **≥ 1.8 × separation** | Nadir passes from both shoulders, gimbal −90° |
| **< 1.8 × separation** | **Cross-aimed obliques** from both shoulders — not nadir |

Cross-aiming from Side 1 and Side 2 also gives you two opposing, convergent
look directions on every point of the roadway. That is strong photogrammetric
geometry, and it does the anti-doming work the crosshatch used to do — so on
this plan the cross-aimed passes are doing double duty and there is no separate
calibration oblique to fly.

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

### Pass 3 — Side 1, cross-aimed oblique

*Use at any altitude; **mandatory** below 1.8 × separation, where nadir is not
enough on its own.*

12. [ ] Return to the **Side 1** shoulder
13. [ ] **Rotate drone perpendicular to roadway** — nose pointed across toward
        Side 2
14. [ ] Set the gimbal to the angle for your altitude and offset (§2.2) —
        e.g. **−63°** at 80 ft AGL over a 40 ft offset
15. [ ] Translate **sideways along the Side 1 shoulder**, down-station, at the
        cross-aim shot spacing

> The Mavic's gimbal pitches but does not yaw independently, so looking across
> the roadway means yawing the aircraft. You are flying laterally with the nose
> held across the road. Slower than a nose-forward pass, and worth practising
> before the job.

### Pass 4 — Side 2, cross-aimed oblique

16. [ ] **Rotate drone perpendicular to roadway**, translate across to the
        **Side 2** shoulder *(only across a roadway confirmed clear of moving
        vehicles — see Pass 5)*
17. [ ] Nose pointed across toward **Side 1**, same gimbal angle
18. [ ] Translate sideways along the **Side 2** shoulder, up-station

> Passes 3 and 4 give every point on the roadway **two opposing look
> directions**, and every vertical face — barrier, guardrail, sign back, curb,
> cut slope — two viewpoints. This pair replaces both the old centre pass and
> the separate calibration obliques.

### Pass 5 — Perpendicular crossings

19. [ ] Every **1000–1600 ft** along the roadway, stop
20. [ ] **Confirm the roadway beneath is clear of moving vehicles** — 107.145
        is about vehicles in motion, so a crossing during a confirmed gap is a
        different case from a sustained pass down the centerline. This is the
        same gap you are already waiting for to keep traffic out of frame
21. [ ] **Rotate drone perpendicular to roadway**, gimbal **−90°**
22. [ ] Cross the full width, past the shoulder on both sides, shooting
23. [ ] **Rotate drone parallel to roadway** and resume

> If your operating authority or a local restriction rules out crossing at all,
> drop this pass and lean harder on Passes 3–4 and the profiles — but add
> crossings back wherever a median, overpass or closure legitimately lets you.

> A handful of frames each. These tie the Side 1 and Side 2 lines together at
> intervals instead of only at the ends, and they are the main defence against
> the corridor bending along its length. *(Spacing here is my engineering
> judgment, not a sourced figure.)*

### Pass 6 — Altitude profiles

24. [ ] At **both ends and the middle** of the run, hold position laterally
25. [ ] Climb or descend in **~25 ft steps**, shooting at each step
26. [ ] **Alternate gimbal −90° → −55° → −90°** as you go

> Varying height decouples focal length from flying height in the solve. This
> is the one thing a grid-flown mission usually lacks and you already do.
> *(Step size is judgment, not sourced.)*

### Pass 7 — Detail, AOI only

27. [ ] Drop to 60 ft or lower over the specific area of interest
28. [ ] **Rotate drone perpendicular to roadway** and cross-aim from each
        shoulder in turn — at 60 ft over a 40 ft offset that is gimbal **−56°**.
        Nadir from the shoulders gives only 5% overlap at this height
29. [ ] Repeat at gimbal **−45°** for pavement texture, joints, edges, distress
30. [ ] Gimbal **−30°** for barrier faces, guardrail, sign structures
31. [ ] Two orbits around any structure, camera held on it — one each direction

---

## 5. Tier plan

| Tier | Passes | Purpose |
|---|---|---|
| **200 ft** | 1, 2 — nadir | Overview. Above the 1.8 × floor, so shoulder nadir works |
| **150 ft** | 1, 2, 5 | Nadir still viable at 80 ft separation (62% overlap) |
| **80–120 ft** ★ | 3, 4, 5 — **cross-aimed** | **Primary deliverable tier.** Below the nadir floor, so obliques carry it |
| 60 ft and below | 7 | AOI detail, cross-aimed only |
| Between tiers | 6 | Altitude profiles |

★ If the day gets cut short, the cross-aimed pair at 80–120 ft is what you
protect. It carries both the resolution and the geometry.

**Note the inversion from a grid-flown job:** normally nadir is the backbone and
obliques are supplementary. Under a no-overflight constraint it is the other way
round — nadir works only from high up, and the detail tiers are oblique.

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

## 9. What this plan gives up, and what covers it

Honest accounting, since both the grid and the centre pass are unavailable:

| Lost | Covered by |
|---|---|
| Crosshatch geometry | Passes 3–4 cross-aimed obliques give two opposing look directions on every point |
| Centre pass at low altitude | Cross-aiming — tilt replaces translation |
| Nadir coverage below 1.8 × separation | Accepted: the low tiers are oblique by design |
| True-nadir pixels on the pavement | The high nadir tier (200 ft), plus obliques at ≤27° off nadir, which is close to nadir |
| Coverage outside the ROW | Accepted — the roadway is the deliverable |

**Residual risks, in order:**

1. **Longitudinal bending on a long run.** Passes 5 and 6 and the zigzag control
   hold it. On a run longer than about a mile, add crossings more often rather
   than less. If crossings are ruled out entirely, tighten GCP spacing to
   250–300 ft instead of 400–500.
2. **Oblique-only coverage of the far lane.** The far side of the roadway sits
   at the foreshortened end of each frame. The opposing pass covers it at the
   near end, which is exactly why both Passes 3 and 4 are mandatory — flying
   only one side leaves half the roadway documented at its worst.
3. **Flying sideways is slower and more demanding.** Budget more airtime than a
   nose-forward pass, and practise the lateral translation before the job.

---

## 10. Regulatory note

This plan assumes **14 CFR 107.145** — no operation over a moving vehicle — and
keeps the aircraft over the shoulder throughout. It is written around that
constraint, not as legal advice: verify against your own operating authority,
any waivers you hold, and local restrictions before you fly. Where a closure,
median or overpass legitimately permits overflight, the geometry gets easier,
not harder.

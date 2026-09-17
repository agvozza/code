# Roadway Corridor — UAS Flight Workflow (Manual Flight)

Flight-side workflow for documenting a roadway with a DJI Mavic 3 Classic,
flown **manually** (no automated grid), targeting an orthomosaic **and** a dense
point cloud, processed in RealityCapture and/or Pix4D.

A roadway is a **corridor**, and corridors are their own problem. Most drone
mapping advice assumes a squarish block flown by mission-planning software;
little of it survives contact with a 2-mile strip 120 ft wide flown by hand.
This document is specific to both.

New to the vocabulary? → [glossary.md](glossary.md)

Companions: [field-capture.md](field-capture.md) (general site practice) ·
[workflow.md](workflow.md) (processing) ·
[naming-convention.md](naming-convention.md)

---

## 1. Assessment of the method you're flying now

Your current pattern: manual flight throughout, shots timed to avoid vehicles,
400 / 200 / 100 ft plus a low AOI pass, nadir throughout, nadir frames every
10 ft during altitude transitions, coverage shrinking as you descend, high to
low.

### 1.1 Timing shots around traffic is correct, and the reason is structural

This is not a workaround. It is the single highest-value thing you are doing,
and it is worth understanding exactly why so you know when to spend time on it.

Photogrammetry reconstructs a point by finding the same physical thing in
several overlapping images and intersecting the rays. That requires the thing to
**stay put between exposures**. As the photogrammetry literature puts it, pixels
of objects that move between captures *cannot be matched, because the pixels in
that location show a different object than the pixels of another image mapping
the same region.*

So a moving vehicle does three distinct kinds of damage:

1. **It cannot triangulate.** It appears at a different place in each frame, so
   the matcher either produces a smeared blob of garbage geometry or fails and
   leaves a hole.
2. **It ghosts the orthomosaic.** Moving cars come out duplicated and
   translucent, with the pavement markings showing through them.
3. **It destroys the data you actually came for.** Pavement under a vehicle is
   simply not observed. For a roadway inspection documenting surface condition,
   cracking and rutting, an occluded lane is missing deliverable, not cosmetic
   damage.

There is an entire research literature on detecting and masking moving vehicles
out of true orthos after the fact, using CNNs and depth filtering. **Not
capturing them is strictly better than removing them**, and an automated grid
cannot do it — it fires on a timer and takes whatever traffic is there. Your
method sidesteps a problem other people pay to solve badly.

One clarifying distinction worth holding onto: **stationary vehicles are fine.**
A parked car, or traffic stopped at a signal for the whole time you are
overhead, is a consistent object and reconstructs correctly as a car. It
occludes pavement, but it does not corrupt anything. The poison is specifically
*motion between frames*. That means traffic stopped at a red light is an
opportunity, not a problem.

### 1.2 What else is already right

- **The altitude ladder is genuinely good practice, for a better reason than
  "more detail."** In a flat corridor, focal length is highly correlated with
  camera height in the bundle adjustment — the solver cannot tell a long lens
  high up from a short lens low down, and the resulting distortion error bends
  the whole model. The published fix is to *"decouple the flying height and the
  principal distance"* by taking oblique images and/or introducing significant
  height variation. Your ladder is the height-variation half of that fix, and
  your transition captures are a legitimate self-calibration device.
- **Manual flight helps here too**, incidentally. Hand-flown altitude wanders a
  little, and mild altitude variation *improves* the calibration geometry for
  exactly the reason above. An auto grid's rigidly constant height is
  marginally worse for self-calibration. Keep the wander under about ±10% so
  GSD stays consistent, but do not chase perfection.
- **Shrinking the footprint as you descend** is the right economy.
- **High-to-low ordering** works: the 400 ft pass doubles as recon.
- **400 ft is the Part 107 ceiling**, so your top tier is already at the legal
  maximum.

### 1.3 What is missing — one item is serious

1. **Everything is nadir. This is the big gap.** Nadir-only capture over a
   corridor is the textbook degenerate case for self-calibration: a lawnmower
   pattern is excellent at horizontal overlap and *geometrically degenerate* for
   solving lens distortion. Nadir images cannot prevent camera poses from
   drifting to compensate for an erroneous focal length; obliques fix it —
   measured at ~50% DEM error reduction in one field comparison and one to two
   orders of magnitude in simulation. **§5 is the main change recommended here.**
2. **Flight line count per altitude is unstated.** If any tier is a single line
   down the centerline, that tier is structurally weak. Pix4D calls
   single-track corridor acquisition *"NOT RECOMMENDED."* At 400 ft your frame
   is 563 ft wide, so one pass *covers* a typical roadway — which is the trap.
   Coverage is not geometry (§4.1).
3. **No cross-ties.** A corridor with only longitudinal lines accumulates error
   along its length and bends — the "banana" (§4.2).
4. **Transition profiles are probably at one location**, so their calibration
   value is local (§6).
5. **Manual flight needs a wider overlap margin than spec.** Hand-flown spacing
   is irregular, so shooting to the 85% minimum means some intervals land below
   it (§3.2).

---

## 2. Set the GSD target first

Everything below is sized by the coarsest acceptable GSD. Computed with
[`tools/flight-calc.py`](../tools/flight-calc.py):

| AGL | GSD | Frame width | Frame length |
|---|---|---|---|
| 400 ft / 122 m | 3.25 cm (1.28 in) | 563 ft | 422 ft |
| 200 ft / 61 m | 1.63 cm (0.64 in) | 282 ft | 211 ft |
| 100 ft / 30 m | 0.81 cm (0.32 in) | 141 ft | 105 ft |
| 50 ft / 15 m | 0.41 cm (0.16 in) | 70 ft | 53 ft |

State DOT digital orthophotography specs land around 0.083 ft (2.54 cm) GSD, so
your **200 ft tier at 1.63 cm already exceeds typical design-grade ortho
requirements. 200 ft is your ortho workhorse**, not 400. Protect that tier if
weather or battery cuts the day short.

---

## 3. Flying it manually

### 3.1 The one rule that makes traffic-timing free: hover, don't coast

**Overlap is a function of distance, not time.** This is the single most
important operational consequence of hand-flying.

If you see a vehicle coming and delay the shutter *while continuing forward*,
you have opened a gap in your overlap — and the gap is exactly as long as your
patience. Do it twice on the same line and you have a hole no processing can
close.

If instead you **stop forward motion, hold position, let the vehicle clear, and
resume from where you stopped**, the delay costs you nothing geometrically. You
spent battery, not coverage.

So the discipline is: *stop, wait, shoot, advance.* Never *coast and wait.*

This one habit converts your traffic-timing from a risk into a free win.

### 3.2 Hold a wider overlap margin than the spec

Auto grids hit their spacing exactly. You will not, and irregular spacing means
some intervals land short of target. Fly to a **nominal 90% forward / 70% side**
so the worst hand-flown interval still clears the 85/60 corridor minimum:

| AGL | Shot every (90% fwd) | Line offset from centerline (70% side) | Max speed @ 2 s |
|---|---|---|---|
| 400 ft | **42 ft** | ±85 ft | 6.4 m/s |
| 200 ft | **21 ft** | ±42 ft | 3.2 m/s |
| 100 ft | **11 ft** | ±21 ft | 1.6 m/s |
| 50 ft | **5 ft** | ±11 ft | 0.8 m/s |

Regenerate for any altitude:

```sh
tools/flight-calc.py --alt-ft 200 --front 90 --side 70
```

**Err short.** An extra frame costs a few megabytes; a gap costs a re-flight.

### 3.3 Shoot single-frame, not timed interval

Timed interval and manual flight fight each other — the interval fires while you
are hovering for traffic, giving you fifty frames of the same spot, and it fires
too far apart when you speed up. Use the shutter button and advance a fixed
distance between shots.

To judge that distance without a grid:

- **Use the frame itself.** At 90% forward overlap you advance one-tenth of a
  frame length per shot. Pick a feature at the leading edge of the frame; when
  it has moved one-tenth of the way down the screen, shoot. This is more
  reliable than estimating ground distance and needs no instruments.
- **Use the distance-to-home readout** as an odometer on a straight run.
- **Count.** From the table, 200 ft covers a mile in ~250 frames per line. If
  you land a segment with half that, you know before you leave site.

### 3.4 Hold the line by eye

- **Keep a fixed reference at a constant position in the frame** — the edge
  line, the centerline stripe, the shoulder break. Watching the frame beats
  watching the aircraft for holding a consistent offset.
- **Fly out on one offset, back on the other.** Out-and-back naturally gives
  you the two longitudinal lines §4.1 requires, at no extra battery. The
  sources describe corridor dual-track exactly this way.
- **Keep the nose along the road.** Crabbing rotates the footprint and eats
  your effective side overlap.

### 3.5 VLOS is the binding constraint on a corridor

Part 107 requires visual line of sight. A corridor will run you out of it faster
than any other job type, and manual out-and-back flying makes it more acute
because you are not simply following a planned route home.

Plan **leapfrog launch points** along the corridor, or work with a visual
observer. Segment the corridor by what you can legally see, then check that
each segment also fits a battery — with traffic waits, it often will not, so
size segments by the tighter of the two.

### 3.6 Battery and staging

Waiting for traffic gaps burns battery with no coverage gained. Budget for it:

- Plan segments **shorter than you would for an auto grid** — assume 30–50% of
  airtime goes to waiting on a busy corridor.
- **Overlap consecutive segments by several frames** so they tie together.
- Land, swap, and resume from a few frames *behind* where you stopped, not
  exactly at it.

### 3.7 When traffic genuinely cannot be avoided

- **Early morning, or Sunday morning.** On a busy corridor this is the real
  answer and no amount of patience substitutes for it.
- **Use signal cycles.** If the corridor has signalised intersections, a red
  light upstream delivers a clean gap on a predictable schedule. Learn the
  cycle and work with it.
- **Stopped traffic is capturable** (§1.1) — it occludes but does not corrupt.
- **Mask what you could not avoid.** Both RealityCapture and Pix4D support
  image masks; masking a few frames is far cheaper than a re-flight.

### 3.8 Optional hybrid, if you ever want it

You do not need to change what works. But if you ever consider automating one
pass: automate **the calibration oblique pass** (§5) and keep hand-flying the
nadir tiers. Those oblique frames exist to constrain lens distortion, not to
document pavement, so a few cars in them barely matter — while the nadir passes,
where clean pavement *is* the deliverable, stay under your control. That gets
you the geometric rigour of a consistent oblique pass without giving up the
thing your manual method is uniquely good at.

---

## 4. Flight line geometry — angles relative to the roadway

Convention: **gimbal pitch where −90° is straight down**, and line bearing
relative to the roadway centerline.

### 4.1 Longitudinal lines (0° — parallel to centerline)

**Minimum two per altitude tier.** Offset them symmetrically about the
centerline per §3.2 — at 200 ft, two lines at **±42 ft** from centerline.
Out-and-back gives you this for free.

For a divided highway or anything wider than ~half a frame, go to three or four
lines at the same spacing.

Corridor overlap spec, from Pix4D — note 85% forward is materially higher than
the 75–80% used for area blocks:

| | Forward | Side |
|---|---|---|
| **Dual-track (use this)** | ≥85% | ≥60% |
| Single-track (avoid) | ≥85% | requires zigzag GCPs |

### 4.2 Cross-ties (90° — perpendicular)

Short perpendicular runs across the corridor **every 1000–1600 ft**, each
extending past the ROW on both sides. Manually this is trivial — at the station,
turn, cross the road, turn, cross back, resume. A handful of frames each.

They are the single most effective structural defence against longitudinal
drift, because they tie the two longitudinal lines together at intervals rather
than only at the ends.

### 4.3 End blocks

At **each end of the corridor**, fly a small area block — a short crosshatch a
few hundred feet square — rather than simply stopping the lines. Corridor ends
are where drift is worst and least constrained. Pair with GCPs at each end (§7).

### 4.4 Summary pattern

```
   end        cross-tie          cross-tie          cross-tie        end
  block          |                   |                  |          block
 ┌─────┐    ─────┼─────         ─────┼─────        ─────┼─────    ┌─────┐
 │ ╳╳╳ │         |                   |                  |         │ ╳╳╳ │
 ├─────┼─────────┼───────────────────┼──────────────────┼─────────┼─────┤  outbound (+offset)
 │·····│·········|···················|··················|·········│·····│  ← centerline
 ├─────┼─────────┼───────────────────┼──────────────────┼─────────┼─────┤  return (−offset)
 └─────┘         |                   |                  |         └─────┘
            ←──────── 1000–1600 ft ────────→
```

---

## 5. Gimbal angles

This is the section that changes your current method most.

| Pass | Gimbal | Purpose |
|---|---|---|
| **Nadir** | **−90°** | Orthomosaic base, pavement surface |
| **Calibration oblique** | **−55° to −60°** | Kills doming/banana. The critical one. |
| **Detail oblique** | **−45°** | Guardrail, barrier, sign faces, slopes, drainage |
| **Asset oblique** | **−30° to −20°** | Bridge piers, retaining walls, sign structures |

### 5.1 Why −55° to −60°

Published guidance is given in degrees *off nadir* and clusters at 20–45°.
[MDPI's study](https://doi.org/10.3390/drones8110662) found **20–35° off nadir**
optimal with a crosshatch block; AeroCartwright recommends **30–45°**. The
overlap of both is **30–35° off nadir** = gimbal **−55° to −60°**.

This pass is not about seeing anything new. It breaks the focal-length/altitude
correlation so the bundle adjustment cannot bend the model. Skipping it is why
nadir-only corridors come out banana-shaped.

Practical note for manual flight: gimbal pitch is set on the controller and
**stays where you put it**, so an oblique pass is no harder to hand-fly than a
nadir one. Set it once at the start of the pass.

### 5.2 Two oblique passes, one from each side

Fly the calibration obliques as **two longitudinal passes, each looking inward
at the corridor from opposite sides** — which again falls out of out-and-back
naturally. Every vertical face (guardrail, barrier, sign back, cut slope) then
gets seen from two opposing directions. A single oblique pass leaves one face of
every vertical feature unobserved, which shows up as smeared or missing geometry
in the dense cloud.

### 5.3 Where each pass belongs in the ladder

Published roadway practice is nadir at higher altitude, camera inclined toward
the pavement at lower altitude — which fits your shrinking ladder:

| Tier | Nadir | Calibration oblique (−55°) | Detail oblique (−45°) |
|---|---|---|---|
| 400 ft | ✔ full corridor | — | — |
| 200 ft | ✔ full corridor | ✔ full corridor | — |
| 100 ft | ✔ AOI | ✔ AOI | ✔ AOI |
| 50 ft and below | ✔ AOI | — | ✔ AOI, orbits |

---

## 6. Altitude transition profiles — refined

Keep the technique, change the execution:

1. **Multiple locations.** Both ends, the middle, ideally every 1000–2000 ft. A
   profile at one location calibrates locally; spread along the corridor it
   constrains the whole block.
2. **25–50 ft intervals, not 10 ft.** The calibration value is in the *spread*
   of heights, not the sample count. 400→100 ft at 30 ft steps is ~10 frames
   instead of 30.
3. **Include obliques in the stack.** Alternate nadir and −55° as you descend. A
   pure-nadir vertical stack shares the degenerate geometry of everything else.
4. **Hold position laterally.** Drifting during the profile turns a clean scale
   series into an ambiguous one. Easy to do manually — pick a mark and hold it
   centred.

---

## 7. Ground control for a corridor

- **Alternate sides of the centerline in a zigzag**, every **400–500 ft**. A
  study of roadway projects found 9–11 GCPs *"distributed alternatively on both
  sides of the road in an offset or zigzagging pattern"* optimal.
- **A pair at each end of the corridor.** Both ends. Ends drift.
- **Never a straight line down the centerline.** Collinear control lets the
  block roll about that axis.
- **Vary the height** where terrain allows — embankment tops and bottoms, on
  structures.
- **Check points interleaved**, roughly every third position, withheld from the
  solve.
- **Confirm each GCP is visible in ≥8–10 frames.** Easy to verify manually:
  when you pass over one, deliberately take a few extra frames.

Your Mavic 3 Classic has **no RTK**, so this is mandatory, not optional — see
[workflow.md](workflow.md#why-control-and-not-just-icp).

---

## 8. Software — RealityCapture and Pix4D

Good at different halves of the job. Fly once, use both.

| | Pix4D | RealityCapture |
|---|---|---|
| Orthomosaic | **Stronger** | Workable, not its focus |
| Dense cloud / mesh detail | Good | **Stronger** |
| Long corridors | **PIX4Dmatic** built for linear projects | Fragments into components |
| Mixed altitudes/angles | Handled | **Handled well** |
| Irregular hand-flown spacing | Handled | **More tolerant** |
| Rolling shutter | Explicit correction options | Less explicit |

**Recommended split: ortho from Pix4D, dense cloud and mesh from
RealityCapture.**

### 8.1 Pix4D

- **Use PIX4Dmatic, not Mapper, for a long corridor.**
- **Enable rolling shutter correction** — the Mavic 3 Classic is
  electronic-shutter-only, and Pix4D names rolling shutter as a direct cause of
  warped models. Use the **linear rolling shutter** algorithm.
- For a model that still comes out curved, Pix4D's documented remedy is **"All
  prior" camera optimization plus the linear rolling shutter algorithm**.
- Process **one battery segment at a time**, QC each, then merge.
- Mask any vehicles you could not avoid before ortho generation.

### 8.2 RealityCapture

- **Component fragmentation is the corridor failure mode.** Long thin datasets
  split into components that must be linked with manual control points. Your
  cross-ties (§4.2) and end blocks (§4.3) are the structural prevention.
- **Cull blurry frames before alignment** — more relevant to manual flight,
  since hand-flown stop-and-go produces occasional soft frames during
  acceleration. Shoot after the aircraft settles, not during the stop.
- **Asphalt is low-texture** and is the hardest surface in this job for feature
  matching. Raise detector sensitivity, keep overlap high, avoid midday specular
  glare off fresh pavement — overcast genuinely helps.
- Lock white balance and keep ISO low; channel shifts across a corridor produce
  visible seams.

---

## 9. Methodical flight sequence

### Pre-flight
1. [ ] Airspace checked; 400 ft ceiling confirmed
2. [ ] **VLOS segments planned**, leapfrog launch points chosen (§3.5)
3. [ ] GSD target agreed → altitude ladder set (§2)
4. [ ] `flight-calc.py --front 90 --side 70` run; **shot spacing and max speed
       per tier written on the card** (§3.2)
5. [ ] Cross-tie and profile stations identified at 1000–1600 ft
6. [ ] GCPs placed zigzag, pair at each end, check points interleaved (§7)
7. [ ] Camera: manual exposure, manual WB, focus at infinity, no CPL,
       **single-shot mode, not timed interval** (§3.3)
8. [ ] Traffic plan: time of day, signal cycles noted (§3.7)

### On station
9. [ ] **Hover 2–3 min at altitude before the first pass** — lens distortion
       shifts with temperature, and a cold first frame is calibrated
       differently from a warm last one

### Capture — high to low, out-and-back each tier
10. [ ] **400 ft nadir**, out on +offset / back on −offset — recon + overview
11. [ ] **200 ft nadir**, out-and-back — *primary ortho tier*
12. [ ] **200 ft oblique −55°**, out-and-back looking inward — *anti-doming pass*
13. [ ] **Cross-ties** at stations, nadir, full width past ROW
14. [ ] **End blocks** at both ends
15. [ ] **Altitude profiles** at stations, 25–50 ft steps, alternating nadir/−55°
16. [ ] **100 ft nadir + −55° + −45°** over AOIs
17. [ ] **50 ft and below** over AOIs: nadir + −45°, orbits around structures
18. [ ] Bridges / overhead sign structures: §107.51(b) structure exception

Throughout: **stop, wait, shoot, advance** (§3.1). Never coast while waiting.

### Before leaving
19. [ ] Frame counts per segment compared against expected (§3.3)
20. [ ] All GCPs confirmed overflown and visible in ≥8–10 frames
21. [ ] Segments confirmed to overlap each other by several frames
22. [ ] Cards backed up before anything is formatted
23. [ ] Rename per flight: `tools/rename-uas-images.sh SITE DATE F01 src dest`

---

## 10. Summary

Keep manual flight and keep timing shots around traffic — that is a real quality
advantage over an automated grid, not a compromise, and moving vehicles are the
one defect class that processing genuinely cannot repair. Keep the altitude
ladder and the high-to-low order.

**Change four things:**

1. **Hover while waiting, never coast** — makes traffic-timing geometrically free.
2. **Add obliques at −55° to −60°**, two passes looking inward.
3. **Two longitudinal lines per tier** (out-and-back) plus **cross-ties every
   1000–1600 ft** and **end blocks**.
4. **Shoot to 90/70, not 85/60**, to absorb hand-flown spacing variance.

That converts a structurally weak nadir corridor into a well-conditioned block
while keeping the clean, vehicle-free pavement that makes your product better
than a grid-flown one.

---

## Sources

- [Pix4D — Selecting the Image Acquisition Plan Type (corridor specs)](https://support.pix4d.com/hc/en-us/articles/202557459)
- [Pix4D — Warped or curved model](https://support.pix4d.com/hc/en-us/articles/8962104582301)
- [Universität Stuttgart IFP — Improving True Ortho quality by removing moving vehicles](https://www.ifp.uni-stuttgart.de/lehre/masterarbeiten/630-Nuebel/)
- [Geavis — Why ghosting and motion blur occur in photogrammetry](https://www.geavis.si/en/2017/12/ghosting-and-motion-blur-in-photogrammetry/)
- [Aerotas — Linear Mission Planning](https://aerotas.com/resources/mission-planning-data-collection/linear-mission-planning/)
- [Propeller — Quality Drone Data Part 4: Long Corridors](https://www.propelleraero.com/blog/quality-drone-data-part-4-long-corridors/)
- [DroneDeploy — Corridor Best Practices](https://help.dronedeploy.com/hc/en-us/articles/21721735901975-Corridor-Best-Practices)
- [RealityScan — Alignment Settings](https://rshelp.capturingreality.com/en-US/appbasics/alignsettings.htm)
- [Remote Sensing — Camera Self-Calibration for Weakly Structured Long Corridor UAV Images](https://www.mdpi.com/2072-4292/13/21/4222)
- [Drones (MDPI) — Influence of the Inclusion of Off-Nadir Images](https://doi.org/10.3390/drones8110662)
- [AeroCartwright — The Doming Effect Explained](https://aerocartwright.com/library/drone-map-doming-effect/)
- [FAA — 14 CFR §107.51 operating limitations](https://www.faa.gov/air_traffic/publications/atpubs/aim_html/chap11_section_4.html)
- [SCDOT Preconstruction Survey Manual 2023](https://www.scdot.org/content/dam/scdot-legacy/business/pdf/surveys/current_manual/2023%20SCDOT%20Preconstruction%20Survey%20Manual.pdf?v=2)

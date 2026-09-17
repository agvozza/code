# Roadway Corridor — UAS Flight Workflow

Flight-side workflow for documenting a roadway with a DJI Mavic 3 Classic,
targeting an orthomosaic **and** a dense point cloud, processed in
RealityCapture and/or Pix4D.

A roadway is a **corridor**, and corridors are their own problem. Most drone
mapping advice assumes a squarish block; almost none of it survives contact
with a 2-mile strip 120 ft wide. This document is corridor-specific.

Companions: [field-capture.md](field-capture.md) (general site practice) ·
[workflow.md](workflow.md) (processing) ·
[naming-convention.md](naming-convention.md)

---

## 1. Assessment of the method you're flying now

Your current pattern: 400 / 200 / 100 ft plus a low AOI pass, nadir throughout,
nadir frames every 10 ft during altitude transitions, coverage shrinking as you
descend, high to low.

**What's already right — keep these:**

- **The altitude ladder is genuinely good practice, and for a better reason
  than "more detail."** In a flat corridor, focal length is highly correlated
  with camera height in the bundle adjustment — the solver cannot tell a long
  lens high up from a short lens low down, and the resulting distortion error
  bends the whole model. The published fix is to *"decouple the flying height
  and the principal distance"* by taking oblique images and/or introducing
  significant height variation. Your ladder is the height-variation half of
  that fix, and your 10-ft transition captures are a legitimate
  self-calibration device. Most people never do this.
- **Shrinking the footprint as you descend** is the right economy. Full-corridor
  coverage at 50 ft would be thousands of frames for detail you only need at
  specific locations.
- **High-to-low ordering** works: the 400 ft pass doubles as recon, and you
  spot hazards, obstructions and access before you're flying close.
- **400 ft is the Part 107 ceiling**, so your top tier is already at the legal
  maximum. §107.51(b)'s structure exception — within a 400 ft radius of a
  structure, up to 400 ft above its uppermost limit — is available around
  bridges and overhead sign structures, but not over open roadway.

**What's missing — and one of these is serious:**

1. **Everything is nadir. This is the big gap.** Nadir-only capture over a
   corridor is the textbook degenerate case for self-calibration: a lawnmower
   grid is excellent at horizontal overlap and *geometrically degenerate* for
   solving lens distortion. The literature is blunt that nadir images cannot
   prevent camera poses from drifting to compensate for an erroneous focal
   length, whereas obliques fix it — measured at a 50% DEM error reduction in
   one field comparison and one to two orders of magnitude in simulation. Your
   altitude ladder is doing half the job; obliques are the other half and the
   stronger half. **§4 is the main change this document recommends.**
2. **Flight line count per altitude is unstated.** If any tier is a single line
   down the centerline, that tier is structurally weak. Pix4D's own
   documentation calls single-track corridor acquisition *"NOT RECOMMENDED"*
   and requires at least two flight lines. At 400 ft your frame is 563 ft wide,
   so one pass *covers* a typical roadway — which is exactly the trap. Coverage
   is not geometry. Fly two lines anyway (§3).
3. **No cross-ties.** A corridor with only longitudinal lines accumulates error
   along its length and bends — the "banana." Periodic perpendicular runs are
   what stop it (§4.3).
4. **Transition captures are probably at one location.** Their calibration
   value is local. Spread them along the corridor (§5).
5. **10 ft intervals are finer than needed.** What buys you calibration is the
   *spread* of heights, not the number of samples. 25–50 ft is plenty; the
   ladder from 400→100 ft becomes ~8–12 frames instead of 30.

---

## 2. Set the GSD target first

Everything below is sized by the coarsest acceptable GSD. Computed with
[`tools/flight-calc.py`](../tools/flight-calc.py):

```
tools/flight-calc.py --alt-ft 400 200 100 50
```

| AGL | GSD | Frame width | Line spacing @60% | Shot every @85% | Max speed @2 s |
|---|---|---|---|---|---|
| 400 ft / 122 m | 3.25 cm (1.28 in) | 563 ft | 225 ft | 63 ft | 9.6 m/s |
| 200 ft / 61 m | 1.63 cm (0.64 in) | 282 ft | 113 ft | 32 ft | 4.8 m/s |
| 100 ft / 30 m | 0.81 cm (0.32 in) | 141 ft | 56 ft | 16 ft | 2.4 m/s |
| 50 ft / 15 m | 0.41 cm (0.16 in) | 70 ft | 28 ft | 8 ft | 1.2 m/s |

**Read the max-speed column before you fly.** At 100 ft on a 2 s interval you
cannot exceed 2.4 m/s without silently thinning forward overlap below 85%. This
is the most common way a corridor mission quietly fails: the pilot flies a
comfortable 8 m/s at low altitude and lands with 50% overlap.

If you capture DNG, the RAW interval limit is longer than JPEG's — at 100 ft on
a 5 s interval the ceiling drops to **1.0 m/s**. Check your firmware's actual
interval and set speed from it.

For reference, state DOT digital orthophotography specs land around 0.083 ft
(2.54 cm) GSD, so your 200 ft tier at 1.63 cm already exceeds typical
design-grade ortho requirements. **200 ft is your ortho workhorse**, not 400.

---

## 3. Flight line geometry — angles relative to the roadway

Convention below: **gimbal pitch where −90° is straight down**, and line
bearing relative to the roadway centerline.

### 3.1 Longitudinal lines (0° — parallel to centerline)

**Minimum two per altitude tier.** Not one. Offset them symmetrically about the
centerline at the line spacing from §2 — at 200 ft, two lines at **±56 ft**
from centerline gives 60% side overlap.

For a divided highway or anything wider than ~half a frame, go to three or four
lines and keep the same spacing.

Overlap spec for corridors, from Pix4D:

| | Forward | Side |
|---|---|---|
| **Dual-track (use this)** | ≥85% | ≥60% |
| Single-track (avoid) | ≥85% | n/a — requires zigzag GCPs |

Note 85% forward is materially higher than the 75–80% used for area blocks.
Corridors need it.

### 3.2 Cross-ties (90° — perpendicular)

Short perpendicular runs across the corridor, **every 1000–1600 ft**, each
extending past the ROW on both sides. These are cheap — a few frames each — and
they are the single most effective structural defence against longitudinal
drift, because they tie the two longitudinal lines together at intervals
instead of only at the ends.

### 3.3 End blocks

At **each end of the corridor**, fly a small area block (a short crosshatch, a
few hundred feet square) rather than simply terminating the lines. Corridor ends
are where drift is worst and least constrained. This pairs with putting a pair
of GCPs at each end (§6).

### 3.4 Summary pattern

```
   end        cross-tie          cross-tie          cross-tie        end
  block          |                   |                  |          block
 ┌─────┐    ─────┼─────         ─────┼─────        ─────┼─────    ┌─────┐
 │ ╳╳╳ │         |                   |                  |         │ ╳╳╳ │
 ├─────┼─────────┼───────────────────┼──────────────────┼─────────┼─────┤  line 1  (+offset)
 │·····│·········|···················|··················|·········│·····│  ← centerline
 ├─────┼─────────┼───────────────────┼──────────────────┼─────────┼─────┤  line 2  (−offset)
 └─────┘         |                   |                  |         └─────┘
            ←──────── 1000–1600 ft ────────→
```

---

## 4. Gimbal angles

This is the section that changes your current method most.

| Pass | Gimbal | Purpose |
|---|---|---|
| **Nadir** | **−90°** | Orthomosaic base, pavement surface |
| **Calibration oblique** | **−55° to −60°** | Kills doming/banana. The critical one. |
| **Detail oblique** | **−45°** | Guardrail, barrier, sign faces, slopes, drainage |
| **Asset oblique** | **−30° to −20°** | Bridge piers, retaining walls, sign structures, only where needed |

### 4.1 Why −55° to −60°

Published guidance on oblique angle is given as degrees *off nadir* and
clusters at 20–45°. [MDPI's study](https://doi.org/10.3390/drones8110662) found
**20–35° off nadir** optimal when combined with a crosshatch block; AeroCartwright
recommends **30–45°**. The overlap of both is **30–35° off nadir**, which is a
gimbal pitch of **−55° to −60°**. Use that unless you have a specific reason.

This pass is not about seeing anything new. It is about breaking the
focal-length/altitude correlation so the bundle adjustment cannot bend the
model. Skipping it is why nadir-only corridors come out banana-shaped.

### 4.2 Two oblique passes, one from each side

Fly the calibration obliques as **two longitudinal passes, each looking inward
at the corridor from opposite sides**. Every vertical face — guardrail, barrier,
sign back, cut slope — then gets seen from two opposing directions. A single
oblique pass leaves one face of every vertical feature unobserved, which shows
up as smeared or missing geometry in the dense cloud.

### 4.3 Where each pass belongs in the ladder

Published roadway practice is to fly **nadir at higher altitude and incline the
camera obliquely toward the pavement at lower altitude** — which fits your
shrinking-footprint ladder neatly:

| Tier | Nadir | Calibration oblique (−55°) | Detail oblique (−45°) |
|---|---|---|---|
| 400 ft | ✔ full corridor | — | — |
| 200 ft | ✔ full corridor | ✔ full corridor | — |
| 100 ft | ✔ AOI | ✔ AOI | ✔ AOI |
| 50 ft and below | ✔ AOI | — | ✔ AOI, orbits |

The 200 ft tier carries both the ortho and the calibration obliques, which is
why it is the tier to protect if weather or battery cuts the day short.

---

## 5. Altitude transition profiles — refined

Keep the technique, change the execution:

1. **Multiple locations.** Both ends, the middle, and ideally every 1000–2000
   ft. A profile at a single location calibrates locally; spread along the
   corridor it constrains the whole block.
2. **25–50 ft intervals, not 10 ft.** The calibration value is in the spread of
   heights, not the sample count. 400→100 ft at 30 ft intervals is ~10 frames.
3. **Include obliques in the stack.** Alternate nadir and −55° as you climb or
   descend. A pure-nadir vertical stack shares the degenerate geometry of
   everything else; mixing angles makes each profile a calibration asset.
4. **Hold position.** Drifting laterally during the profile turns a clean scale
   series into an ambiguous one.

---

## 6. Ground control for a corridor

Corridor GCP layout differs from area layout and the sources converge on it:

- **Alternate sides of the centerline in a zigzag**, every **400–500 ft**. Pix4D
  explicitly prescribes a zigzag for single-track work; a study of roadway
  projects found 9–11 GCPs *"distributed alternatively on both sides of the road
  in an offset or zigzagging pattern"* optimal.
- **A pair at each end of the corridor.** Both ends. Non-negotiable — ends drift.
- **Never a straight line down the centerline.** Collinear control lets the
  block roll about that axis, and on a corridor that failure mode is right
  there waiting.
- **Vary the height** where the terrain allows — top and bottom of embankments,
  on structures. Same decorrelation argument as §1.
- **Check points interleaved**, roughly every third position, withheld from the
  solve. Without them you have no accuracy number.

Your Mavic 3 Classic has **no RTK**, so this is mandatory rather than
optional — see [workflow.md](workflow.md#why-control-and-not-just-icp).

---

## 7. Software — RealityCapture and Pix4D

They are good at different halves of this job. The efficient answer is to fly
once and use both.

| | Pix4D | RealityCapture |
|---|---|---|
| Orthomosaic | **Stronger** — purpose-built, true-ortho handling | Workable, not its focus |
| Dense cloud / mesh detail | Good | **Stronger** |
| Long corridors | **PIX4Dmatic** is built for linear projects | Fragments into components; needs management |
| Mixed altitudes/angles | Handled | **Handled well** |
| Rolling shutter | Explicit correction options | Less explicit |

**Recommended split: ortho from Pix4D, dense cloud and mesh from RealityCapture.**

### 7.1 Pix4D specifics

- **Use PIX4Dmatic, not Mapper, for a long corridor.** Mapper has practical
  dataset limits that corridors blow through; Matic is built for linear
  projects.
- **Enable rolling shutter correction.** The Mavic 3 Classic is
  electronic-shutter-only, and Pix4D names rolling shutter as a direct cause of
  warped models. Use the **linear rolling shutter** algorithm.
- For a model that still comes out curved, Pix4D's documented remedy is **"All
  prior" camera optimization combined with the linear rolling shutter
  algorithm**.
- Plan each flight block to **one battery cycle** so blocks can be processed and
  QC'd individually, then merged.

### 7.2 RealityCapture specifics

- **Component fragmentation is the corridor failure mode.** Long thin datasets
  split into multiple components that must be linked with manual control points.
  Your cross-ties (§3.2) and end blocks (§3.3) are the structural fix; control
  points are the repair.
- **Cull blurry frames before alignment.** They slow processing and degrade
  accuracy.
- **Asphalt is low-texture** and is the hardest surface in this whole job for
  feature matching. Raise detector sensitivity, keep overlap high, and avoid
  midday specular glare off fresh pavement — overcast genuinely helps here.
- Lock white balance to daylight and keep ISO low; channel shifts across a
  corridor produce visible seams.

---

## 8. Methodical flight sequence

Ordered as flown.

### Pre-flight
1. [ ] Airspace checked; 400 ft ceiling confirmed for the corridor
2. [ ] GSD target agreed → altitude ladder set (§2)
3. [ ] `tools/flight-calc.py` run; **max speed per tier written on the card**
4. [ ] Line offsets computed per tier (§3.1)
5. [ ] Cross-tie and profile stations marked at 1000–1600 ft intervals
6. [ ] GCPs placed in zigzag, pair at each end, check points interleaved (§6)
7. [ ] Camera: manual exposure, manual WB, focus at infinity, no CPL
8. [ ] Shoot JPEG+DNG; confirm interval limit for whichever drives your speed

### On station
9. [ ] **Hover 2–3 min at altitude before the first grid** — lens distortion
       parameters shift with temperature, and a cold first frame is calibrated
       differently from a warm last one

### Capture — high to low
10. [ ] **400 ft nadir**, 2 lines, full corridor — recon + overview ortho
11. [ ] **200 ft nadir**, 2 lines, full corridor — *primary ortho tier*
12. [ ] **200 ft oblique −55°**, 2 lines from opposite sides — *the anti-doming pass*
13. [ ] **Cross-ties** at 1000–1600 ft, nadir, full width
14. [ ] **End blocks** at both ends
15. [ ] **Altitude profiles** at stations, 25–50 ft steps, alternating nadir/−55° (§5)
16. [ ] **100 ft nadir + −55° + −45°** over AOIs
17. [ ] **50 ft and below** over AOIs: nadir + −45°, orbits around structures
18. [ ] Bridges/sign structures: §107.51(b) structure exception if needed

### Before leaving
19. [ ] Image counts logged per flight
20. [ ] All GCPs confirmed overflown and visible in ≥8–10 frames each
21. [ ] Cards backed up before anything is formatted
22. [ ] Rename per flight: `tools/rename-uas-images.sh SITE DATE F01 src dest`

---

## 9. The one-line summary

Keep your altitude ladder and your high-to-low order — both are sound, and the
ladder is doing real calibration work most pilots skip. **Add obliques at −55°
to −60°, fly at least two longitudinal lines per tier, add perpendicular
cross-ties every 1000–1600 ft, and put your GCPs in a zigzag with a pair at each
end.** That converts a structurally weak nadir corridor into a well-conditioned
block, and it is the difference between a model that measures and a model that
merely looks right.

---

## Sources

- [Pix4D — Selecting the Image Acquisition Plan Type (corridor specs)](https://support.pix4d.com/hc/en-us/articles/202557459)
- [Pix4D — Warped or curved model](https://support.pix4d.com/hc/en-us/articles/8962104582301)
- [Pix4D Community — Long Roadway Corridor](https://community.pix4d.com/t/long-roadway-corridor-question/30923)
- [Aerotas — Linear Mission Planning](https://aerotas.com/resources/mission-planning-data-collection/linear-mission-planning/)
- [Propeller — Quality Drone Data Part 4: Long Corridors](https://www.propelleraero.com/blog/quality-drone-data-part-4-long-corridors/)
- [DroneDeploy — Corridor Best Practices](https://help.dronedeploy.com/hc/en-us/articles/21721735901975-Corridor-Best-Practices)
- [RealityScan — Alignment Settings](https://rshelp.capturingreality.com/en-US/appbasics/alignsettings.htm)
- [RealityCapture alignment tips](https://wizardofaz.medium.com/reality-capture-alignment-tips-fixes-d49371ee6643)
- [Remote Sensing — Camera Self-Calibration with GNSS Constrained Bundle Adjustment for Weakly Structured Long Corridor UAV Images](https://www.mdpi.com/2072-4292/13/21/4222)
- [Drones (MDPI) — Influence of the Inclusion of Off-Nadir Images](https://doi.org/10.3390/drones8110662)
- [AeroCartwright — The Doming Effect Explained](https://aerocartwright.com/library/drone-map-doming-effect/)
- [Sensors — Flight Path Setting and Data Quality for UAV Bridge Deck Documentation](https://pmc.ncbi.nlm.nih.gov/articles/PMC10459964/)
- [FAA — 14 CFR §107.51 operating limitations](https://www.faa.gov/air_traffic/publications/atpubs/aim_html/chap11_section_4.html)
- [SCDOT Preconstruction Survey Manual 2023](https://www.scdot.org/content/dam/scdot-legacy/business/pdf/surveys/current_manual/2023%20SCDOT%20Preconstruction%20Survey%20Manual.pdf?v=2)

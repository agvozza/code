# Field Capture — On-Site Best Practices

Everything here is a site-day decision. Almost nothing on this page can be
fixed in the office, which is why it is separated from the processing steps in
[workflow.md](workflow.md).

The single most important sentence on this page: **capture the scans, the
drone flights and the control on the same day, in the same conditions.** Cars
move, vegetation grows, spoil piles get graded. Datasets captured a week apart
disagree in ways that look like registration error and waste days of
troubleshooting.

---

## 1. Specify the accuracy target before anything else

Decide what the deliverable has to be worth *before* choosing scan resolution,
control density or flight altitude. Everything downstream is sized by this one
number, and "as accurate as possible" is not a specification.

The industry framework is the **USIBD Level of Accuracy (LOA)**, which gives
you five tiers to quote against
([USIBD](https://usibd.org/level-of-accuracy/),
[Guide C120](https://cdn.ymaws.com/www.nysapls.org/resource/resmgr/2019_conference/handouts/hale-g_bim_loa_guide_c120_v2.pdf)):

| Level | Tolerance | Typical use |
|---|---|---|
| LOA10 | ~50 mm (2 in) | Rough space planning, feasibility |
| LOA20 | ~15 mm (1/2 in) | General architectural documentation |
| LOA30 | ~5 mm (3/16 in) | Construction documentation, MEP coordination |
| LOA40 | ~1 mm (1/32 in) | Precision renovation, heritage |
| LOA50 | ~0.1 mm | Monument documentation, forensics |

Two things about LOA that matter in practice:

- **It is a 2σ (95% confidence) range**, not a best case. Quote it that way.
- USIBD separates **measured** accuracy (what your instrument achieved) from
  **represented** accuracy (what the delivered model actually holds). A model
  simplified for delivery can be a full tier worse than the cloud it came from.

Exact tier values have shifted between LOA specification versions — check the
current C120 document before writing a number into a contract.

**Where this bites on a fused project:** the drone data is the weak link.
Scans sit comfortably at LOA30 or better; a non-RTK photogrammetric block
controlled by GCPs realistically lands around 3–5 cm, which is **LOA10**. You
cannot quote a single LOA for the fused product. Quote per region — scanned
surfaces at one tier, drone-only surfaces (roofs, canopy) at another — or
quote the whole thing at the weaker tier. Be explicit about which.

For heritage work, Historic England's
[Geospatial Survey Specifications for Cultural Heritage](https://historicengland.org.uk/images-books/publications/geospatial-survey-specifications-cultural-heritage/)
(HEAG317) is the nationally recognised specification and covers TLS, SfM
photogrammetry and low-level UAV imagery together.

---

## 2. Before you leave

- [ ] Accuracy target agreed and written down (§1)
- [ ] Site code assigned, matching [naming-convention.md](naming-convention.md)
- [ ] Airspace checked; authorisation in hand if controlled
- [ ] Control design sketched on a site plan — target positions chosen in the
      office, not improvised on the tailgate
- [ ] Scan positions sketched on the same plan (§4)
- [ ] Targets counted and packed: control + check + spares (they get run over)
- [ ] Batteries charged: scanner, drone (all of them), controller, GNSS rover
- [ ] SD cards **formatted in the device**, not on a laptop
- [ ] Sun path checked for the day — see §6

---

## 3. Control design (do this first, on paper)

Control is what splices the two datasets together, so it gets designed before
either sensor is planned.

**How many.** Four is the theoretical minimum for a non-RTK block; five —
four corners plus centre — is the practical minimum; 8–12 well-distributed
points is the working number for a typical site. Published scaling guidance
varies by roughly an order of magnitude, from one additional point per 25–30
acres to one per 50–200 acres, depending on how broken the terrain is
([AeroCartwright](https://aerocartwright.com/library/drone-map-doming-effect/),
[DroneDeploy](https://help.dronedeploy.com/hc/en-us/articles/11138616177047-Best-Practices-for-Ground-Control-Points-GCPs-and-Checkpoints)).
Use the dense end for broken ground and the sparse end for flat open sites.

**Then add 3–5 check points on top.** Check points are withheld from the
solve. Without them you have no accuracy number — only residuals, which measure
how well the solve fit the data it was handed, not whether it is right.

**Where.**

- Spread across the whole area, including **outside** the area of interest.
  Anything beyond the control envelope extrapolates and distorts.
- **One near the site centre**, not corners only. A ring of perimeter control
  with a hollow middle is the classic doming setup.
- Never in a straight line. A linear arrangement leaves the block free to
  rotate about that line.
- **Vary the height.** Put points on a roof, a mound, a ridge line, the top and
  bottom of a slope. The mechanism is specific: control at differing heights
  decorrelates focal length from exterior orientation in the bundle
  adjustment, which is exactly the correlation that produces doming.
  Control that is all on one flat plane constrains X and Y and barely
  constrains Z.
- Clear sky view. Not under canopy, not tight against a building face — both
  for the drone's line of sight and for a GNSS receiver if you are occupying
  them.
- On stable ground you will not drive over, and where the scanner can also see
  them from at least two setups.

**Important caveat on control density:** adding more GCPs does *not* fix
doming. Simulation work is explicit that oblique imagery is the key requisite
on flat terrain while ground control density is not — throwing points at a
nadir-only block buys much less than flying obliques does. Design the control
for georeferencing and verification; design the *flight* (§7) to kill the
systematic error.

**Target size.** The rule is ≥5× GSD, with 10× comfortable. For the Mavic 3
Classic (§7) a 50–60 cm checkerboard suits flights at 50–80 m; 30 cm is the
floor and only works low. A 60 cm target at 60 m AGL is ~37 px across — plenty
to pick a centre confidently.

**Make each target dual-purpose.** This is the crux of the whole splice:

1. Drive a nail or mark a paint cross — this is the physical point, and it is
   what the ID in the naming convention refers to.
2. Lay the aerial target centred on that mark, for the drone.
3. Set a FARO checkerboard or sphere target **concentric over the same mark**
   for the scanner, because Scene detects those automatically to a millimetre
   or two, whereas picking the centre of a flat painted board out of a point
   cloud by eye is worth maybe a centimetre on a good day.
4. Photograph the target in place, with its written ID visible in frame.

That last step costs ten seconds and resolves every "which one was GCP07?"
argument that would otherwise happen three days later.

---

## 4. Laser scanning (FARO Focus)

### Instrument reality

Current Focus models (Core, Premium, Premium Max — which differ mainly in
range) share roughly: **±1 mm ranging error, ~2 mm 3D accuracy at 10 m, ~3.5 mm
at 25 m, 19 arcsec angular accuracy**. Angular resolution is configurable from
0.009° to 0.288°, which is **1.5 mm to 49.1 mm point spacing at 10 m**
([FARO tech sheet](https://knowledge.faro.com/Hardware/Focus/Focus/Technical_Specification_Sheet_for_the_Focus_Laser_Scanner)).

Note the shape of those numbers: accuracy degrades with range, so a surface
captured at 40 m is materially worse than the same surface at 10 m. Range
discipline is an accuracy decision, not just a coverage one.

### Settings

From FARO's own guidance
([FARO KB](https://knowledge.faro.com/Hardware/Focus/Focus/Laser_Scanner_Best_Practices)):

| Setting | Use |
|---|---|
| Resolution 1/1–1/2 | Objects and small areas |
| Resolution 1/4–1/5 | Outdoors and large indoor spaces |
| Resolution 1/8–1/10 | Indoors and small outdoor spaces |
| Quality 2x | Good conditions, time-constrained |
| Quality 3x | Indoors, or overcast outdoors |
| Quality 4x | Bright sun, or poor weather |

Outdoors on a typical site, **1/4 at 3x–4x** is the workhorse. For a standard
measured building survey, **6–10 mm point spacing at 10 m** is the usual
target. Going finer multiplies scan time without adding usable detail at range,
because past roughly 20 m the limit is beam divergence, not point spacing.

Quality is the setting people under-use. It averages multiple measurements per
point, so it buys noise reduction rather than density — which is what you
actually want in sun, rain or on dark surfaces.

### Scan position planning

**Too few setups is the single most consistent cause of unusable scan data**
([KOREC](https://www.korecgroup.com/guides/common-laser-scanning-survey-mistakes/)).
The temptation is always to minimise setups to work faster; the result is
coverage gaps, surfaces captured at excessive range where accuracy suffers, and
blind spots behind objects that only surface during registration — by which
time you have left.

Rules of thumb:

- **Every room needs at least two positions.** Complex spaces with columns,
  alcoves or split levels need more.
- Plan positions conservatively on the site sketch, then go through each one
  and ask whether it genuinely covers every surface you need. Add, don't trim.
- Twelve fast scans that see each other beat six slow ones that don't.
  Overlapping coverage outranks individual scan quality.

### Setup discipline

- Every scan must overlap at least one other. Plan the route so this is
  automatic, and scan through transition points — doorways, gates, corners —
  because those are where the registration will actually latch.
- Keep the scanner within ±5° of level so the inclinometer stays in its good
  range; it contributes to registration.
- Don't put the scan's start/stop seam on the thing you care about.
- At least three targets shared between any two setups, and vary their
  **height and spacing** so the pattern is unique in three dimensions —
  symmetric target layouts give the matcher ambiguous solutions.
- Do not move a target mid-project. If one gets bumped, it is a new ID.
- Walk a consistent, logical order and log each setup number against the
  sketch as you go.
- Wind: drop the tripod height, hang 8–10 lb of sandbag. Heat: above 40 °C use
  the cover. Rain: drop resolution, raise quality.

**Before leaving site:** run the on-site or cloud-to-cloud pre-registration if
your scanner supports it. Finding a hole while the tripod is still in the truck
is the difference between a ten-minute fix and a return trip.

---

## 5. Validate targets before you leave

Confirm each detected target corresponds to one you actually placed, and delete
false detections. Reflective signs, wheel hubs, window frames and bollards all
get picked up as spheres. Checking this on site costs minutes; an error here
cascades silently through registration, control extraction and the entire
photogrammetric solve.

---

## 6. Light and conditions

- **Overcast is ideal** for both sensors. Diffuse light gives even texture and
  no hard shadows, and hard shadows both hide geometry and bake into the mesh
  texture permanently.
- If it must be sunny, fly within ~2 hours of solar noon so shadows are short
  and, more importantly, **consistent across the flight**. A 90-minute capture
  spanning a big sun-angle change produces texture that visibly seams.
- Wet surfaces kill scanner returns and blow out drone highlights. Let it dry.
- Avoid capturing during active site work if you can. People and moving
  equipment become ghost geometry.

---

## 7. Drone capture — DJI Mavic 3 Classic

**The relevant fact about this airframe: it has no RTK.** The Mavic 3
Enterprise takes an RTK module; the Classic does not. Its geotags come from
standalone GNSS — roughly 1–3 m horizontally, and worse vertically, because
altitude is barometric relative to the takeoff point. That accuracy is
irrelevant to your scan data, which is good to millimetres. **GCPs are not
optional for this aircraft.**

### GSD

4/3 sensor, 5280 × 3956 px, 17.3 mm wide → 3.28 µm pixels, 12.29 mm focal
length. So GSD ≈ 2.67 cm per 100 m of altitude:

| AGL | GSD | Footprint |
|---|---|---|
| 30 m | 0.80 cm | 42 × 32 m |
| 40 m | 1.07 cm | 56 × 42 m |
| 50 m | 1.33 cm | 70 × 53 m |
| 60 m | 1.60 cm | 85 × 63 m |
| 80 m | 2.13 cm | 113 × 84 m |
| 100 m | 2.67 cm | 141 × 106 m |

Fly the lowest altitude that safely covers the site in the batteries you have.

### The doming problem, and the three things that fix it

This deserves its own treatment because it is the dominant error mode on a
non-RTK survey and it is invisible until you check.

**Mechanism.** In a nadir-only block, the bundle adjustment cannot separate
radial lens distortion from altitude — the two parameters trade off against
each other. The solver finds a solution that fits the tie points beautifully
while bending the whole reconstruction into a dome or bowl. As one write-up
puts it, a standard lawnmower grid *"is excellent at producing horizontal
overlap. It is geometrically degenerate for self-calibration."* The error is
systematic and vertical, and it peaks in the middle of the site — often tens of
centimetres on a model whose reported residuals look fine.

**Fix 1 — obliques.** This is the big one. Measured results: oblique-inclusive
DEMs averaged 5.7 in of error against 11.6 in for nadir-only on the same site,
and simulation work puts the improvement at one to two orders of magnitude.
On angle, published guidance clusters at **20–45° off nadir**, with
[MDPI's study](https://doi.org/10.3390/drones8110662) finding 20–35° optimal
when combined with a crosshatch AGL block and AeroCartwright recommending
30–45°. **30–35° satisfies both** — use that unless you have a reason not to.

**Fix 2 — crosshatch.** A second grid perpendicular to the first. It helps by
diversifying camera angles, but the sources are consistent that it is *not
sufficient alone*. Do it as well as obliques, not instead.

**Fix 3 — varied-height control**, per §3. Decorrelates focal length from
exterior orientation.

**Bonus fix — let the camera warm up.** Lens distortion parameters shift with
temperature, so **hover 2–3 minutes at altitude before starting the grid.**
The first frames of a cold-camera flight are calibrated differently from the
last, and the solver has no way to know. This costs one battery-minute and is
the cheapest item on this page.

For survey-grade work, a **pre-calibrated camera** beats self-calibration
substantially on nadir-heavy blocks. If you fly the same aircraft repeatedly,
building a calibration is worth the afternoon.

### Flight pattern — all three passes

1. **Nadir grid.** 80% front / 70% side. Published minimums are 75% front /
   65% side, and dropping below them *directly increases dome amplitude* by
   degrading tie point quality. Overlap is free; re-flights are not.
2. **Crosshatch** — second grid, perpendicular.
3. **Obliques at 30–35°**, perimeter passes plus orbits around any structure
   you care about.

### Camera settings

- **Manual exposure, locked.** Fix ISO and shutter before launch. Auto exposure
  varying frame to frame makes texture blending visibly patchy.
- **Manual white balance**, not auto, for the same reason.
- **Focus at infinity**, locked.
- **No polarising filter.** A CPL's effect changes with aircraft heading, so
  the same surface looks different on opposing flight lines — poison for both
  matching and texture. A plain ND to hold shutter speed down is fine.
- Shutter ≥ 1/1000 s where light allows. The Classic has an **electronic
  shutter only** (the Mavic 3E is the one with a mechanical shutter), so
  rolling-shutter smear is a real error source — fly slower and enable rolling
  shutter compensation in processing.

### File type

**Shoot JPEG + DNG.** Process alignment from the JPEGs — the EXIF is clean,
they load faster, and extra bit depth does nothing for feature matching.
Archive the DNGs; pull them out only if you need to rescue highlights for the
final texture pass.

One catch worth the arithmetic: the RAW interval limit is longer than the JPEG
one. At 60 m with 80% front overlap you need a shot every 12.7 m, so at 5 m/s
that is every 2.5 s — fine for JPEG. If your firmware's RAW interval is 5 s,
you must slow to ~2.5 m/s to hold the same overlap. Check the interval your
firmware actually offers and set speed from it, rather than discovering thin
overlap in processing.

### Mission planning

DJI Fly's Waypoint mode will fly a route with set gimbal angles but is tedious
for a grid. Third-party planners (Dronelink, Litchi) handle grids, crosshatches
and terrain-follow properly — verify current Mavic 3 Classic support before you
depend on one. On sloped ground terrain follow matters: a constant-altitude
flight over a 30 m elevation change swings GSD by half, and with it your
effective target size and accuracy.

---

## 8. Before you leave site

- [ ] All targets photographed in place with visible IDs
- [ ] Targets validated against the field log; false detections deleted (§5)
- [ ] Field log complete — every point ID, control vs. check, description
- [ ] Scanner: on-site registration run, no gaps
- [ ] Drone: all three passes flown, image counts recorded per flight
- [ ] Cards backed up to a second device **before** anything is formatted
- [ ] Targets collected (leave them if a return visit is likely — a surviving
      target is a free tie point next time)

---

## Sources

- [FARO — Laser Scanner Best Practices](https://knowledge.faro.com/Hardware/Focus/Focus/Laser_Scanner_Best_Practices)
- [FARO — Technical Specification Sheet for the Focus Laser Scanner](https://knowledge.faro.com/Hardware/Focus/Focus/Technical_Specification_Sheet_for_the_Focus_Laser_Scanner)
- [KOREC — Common Laser Scanning Survey Mistakes](https://www.korecgroup.com/guides/common-laser-scanning-survey-mistakes/)
- [USIBD — Level of Accuracy](https://usibd.org/level-of-accuracy/) · [LOA Guide C120](https://cdn.ymaws.com/www.nysapls.org/resource/resmgr/2019_conference/handouts/hale-g_bim_loa_guide_c120_v2.pdf) · [Lidar News on LOA v3.1](https://lidarnews.com/leveraging-the-usibd-level-of-accuracy-loa-v3-1-to-enhance-laser-scanning-project-specifications/)
- [Historic England — Geospatial Survey Specifications for Cultural Heritage](https://historicengland.org.uk/images-books/publications/geospatial-survey-specifications-cultural-heritage/)
- [DroneDeploy — Best Practices for GCPs and Checkpoints](https://help.dronedeploy.com/hc/en-us/articles/11138616177047-Best-Practices-for-Ground-Control-Points-GCPs-and-Checkpoints)
- [AeroCartwright — Why Your Drone Map Looks Warped: The Doming Effect Explained](https://aerocartwright.com/library/drone-map-doming-effect/)
- [Drones (MDPI) — Influence of the Inclusion of Off-Nadir Images on UAV-Photogrammetry Projects](https://doi.org/10.3390/drones8110662)
- [Remote Sensing (MDPI) — Simulation and Analysis of Photogrammetric UAV Image Blocks: Influence of Camera Calibration Error](https://www.doi.org/10.3390/rs12010022)
- [Sensors — UAV Block Geometry Design and Camera Calibration: A Simulation Study](https://pmc.ncbi.nlm.nih.gov/articles/PMC8473092/)
- [Emlid — Why you need ground control points for drone mapping](https://blog.emlid.com/why-you-need-to-use-ground-control-points-gcp-for-drone-mapping/)

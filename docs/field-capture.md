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

## 1. Before you leave

- [ ] Site code assigned, matching `docs/naming-convention.md`
- [ ] Airspace checked; authorisation in hand if controlled
- [ ] Control design sketched on a site plan — target positions chosen in the
      office, not improvised on the tailgate
- [ ] Targets counted and packed: control + check + spares (they get run over)
- [ ] Batteries charged: scanner, drone (all of them), controller, GNSS rover
- [ ] SD cards **formatted in the device**, not on a laptop
- [ ] Sun path checked for the day — see §4

---

## 2. Control design (do this first, on paper)

Control is what splices the two datasets together, so it gets designed before
either sensor is planned.

**How many.** Four is the theoretical minimum for a non-RTK block; five —
four corners plus centre — is the practical minimum, and 8–12 well-distributed
points is the working number for a typical site. Add roughly one per 50–200
acres beyond that depending on how broken the terrain is.
([DroneDeploy](https://help.dronedeploy.com/hc/en-us/articles/11138616177047-Best-Practices-for-Ground-Control-Points-GCPs-and-Checkpoints),
[Emlid](https://blog.emlid.com/why-you-need-to-use-ground-control-points-gcp-for-drone-mapping/))

**Then add 3–5 check points on top.** Check points are withheld from the
solve. Without them you have no accuracy number — only residuals, which measure
how well the solve fit the data it was handed, not whether it is right.

**Where.**

- Spread across the whole area, including **outside** the area of interest.
  Anything beyond the control envelope extrapolates and distorts.
- Never in a straight line. A linear arrangement leaves the block free to
  rotate about that line.
- **Vary the height.** This is the one people skip. Put points on a roof, a
  mound, the top and bottom of a slope. Control that is all on one flat plane
  constrains X and Y and barely constrains Z, and the vertical is where a
  non-RTK block fails — that is the "doming"/"bowl" error, and varied-Z control
  plus oblique imagery is what kills it.
- Clear sky view. Not under canopy, not tight against a building face — both
  for the drone's line of sight and, if you are occupying them with GNSS, for
  the receiver.
- On stable ground you will not drive over, and where the scanner can also see
  them from at least two setups.

**Target size.** The rule is ≥5× GSD, with 10× comfortable. For the Mavic 3
Classic (§5) a 50–60 cm checkerboard is right for flights at 50–80 m; 30 cm is
the floor and only works low. A 60 cm target at 60 m AGL is ~37 px across —
plenty to pick a centre confidently.

**Make each target dual-purpose.** This is the crux of the whole splice:

1. Drive a nail or mark a paint cross — this is the physical point, and it is
   what the ID in the naming convention refers to.
2. Lay the aerial target centred on that mark, for the drone.
3. Set a FARO checkerboard or sphere target **concentric over the same mark**
   for the scanner, because Scene detects those automatically to a
   millimetre or two, whereas picking the centre of a flat painted board out
   of a point cloud by eye is worth maybe a centimetre on a good day.
4. Photograph the target in place, with its written ID visible in frame.

That last step costs ten seconds and resolves every "which one was GCP07?"
argument that would otherwise happen three days later.

---

## 3. Laser scanning (FARO Focus)

Settings, from FARO's own guidance
([FARO KB](https://knowledge.faro.com/Hardware/Focus/Focus/Laser_Scanner_Best_Practices)):

| Setting | Use |
|---|---|
| Resolution 1/1–1/2 | Objects and small areas |
| Resolution 1/4–1/5 | Outdoors and large indoor spaces |
| Resolution 1/8–1/10 | Indoors and small outdoor spaces |
| Quality 2x | Good conditions, time-constrained |
| Quality 3x | Indoors, or overcast outdoors |
| Quality 4x | Bright sun, or poor weather |

Outdoors on a typical site, **1/4 at 3x–4x** is the workhorse. Going finer
multiplies scan time without adding usable detail at range, because beam
divergence — not point spacing — is the limit past about 20 m.

**Setup discipline:**

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
  the cover.

**Density rule of thumb:** overlapping coverage beats individual scan quality.
Twelve fast scans that see each other register better and cover more than six
slow ones that don't.

**Before leaving site:** run the on-site/cloud-to-cloud pre-registration if
your scanner supports it. Finding a hole while the tripod is still in the truck
is the difference between a ten-minute fix and a return trip.

---

## 4. Light and conditions

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

## 5. Drone capture — DJI Mavic 3 Classic

**The relevant fact about this airframe: it has no RTK.** The Mavic 3
Enterprise takes an RTK module; the Classic does not. Its geotags come from
standalone GNSS — roughly 1–3 m horizontally, and worse vertically, because
altitude is barometric relative to the takeoff point. That accuracy is
irrelevant to your scan data, which is good to millimetres. **GCPs are not
optional for this aircraft.** They are the only mechanism that puts the
imagery into the scanner's coordinate frame at a matching accuracy.

**GSD.** 4/3 sensor, 5280 × 3956 px, 17.3 mm wide → 3.28 µm pixels, 12.29 mm
focal length. So GSD ≈ 2.67 cm per 100 m of altitude:

| AGL | GSD | Footprint |
|---|---|---|
| 30 m | 0.80 cm | 42 × 32 m |
| 40 m | 1.07 cm | 56 × 42 m |
| 50 m | 1.33 cm | 70 × 53 m |
| 60 m | 1.60 cm | 85 × 63 m |
| 80 m | 2.13 cm | 113 × 84 m |
| 100 m | 2.67 cm | 141 × 106 m |

Fly the lowest altitude that safely covers the site in the batteries you have.

**Flight pattern — three passes, and all three matter:**

1. **Nadir grid**, 80% front / 70% side overlap. 70/70 is the usual published
   minimum; go higher, because overlap is free and re-flights are not.
2. **Crosshatch** (second grid, perpendicular). Cheap insurance against
   systematic error in one direction.
3. **Obliques at 20–35° off nadir.** Research on off-nadir inclusion found
   20–35° gave the best accuracy and precision when combined with a crosshatch
   AGL block ([Drones, MDPI 2024](https://doi.org/10.3390/drones8110662)) —
   note that is gentler than the 45° often quoted. Obliques capture facades
   the nadir pass never sees, and they are the main structural defence against
   doming. Add orbits around any structure you care about.

**Camera settings:**

- **Manual exposure, locked.** Fix ISO and shutter before launch. Auto
  exposure varying frame to frame makes texture blending visibly patchy.
- **Manual white balance**, not auto, for the same reason.
- **Focus at infinity**, locked.
- **No polarising filter.** A CPL's effect changes with aircraft heading, so
  the same surface looks different on opposing flight lines — poison for both
  photogrammetry matching and texture. A plain ND to hold shutter speed down
  is fine.
- Shutter ≥ 1/1000 s if you can afford it. The Classic has an **electronic
  shutter only** (the Mavic 3E is the one with a mechanical shutter), so
  rolling-shutter smear is a real error source — fly slower and enable rolling
  shutter compensation in your processing software.

**File type: shoot JPEG + DNG.** Process alignment from the JPEGs — the EXIF
is clean, they load faster, and the extra bit depth does nothing for feature
matching. Archive the DNGs; pull them out only if you need to rescue
highlights for the final texture pass.

One catch worth doing the arithmetic on: the RAW interval limit is longer than
the JPEG one. At 60 m with 80% front overlap you need a shot every 12.7 m, so
at 5 m/s that is every 2.5 s — fine for JPEG. If your firmware's RAW interval
is 5 s, you must slow to ~2.5 m/s to hold the same overlap. Check the interval
your firmware actually offers and set the speed from it, rather than
discovering thin overlap in processing.

**Mission planning.** DJI Fly's Waypoint mode will fly a route with set gimbal
angles, but it is tedious for a grid. Third-party planners (Dronelink, Litchi)
handle grids, crosshatches and terrain-follow properly — verify current Mavic 3
Classic support before you depend on one. On sloped ground, terrain follow
matters: a constant-altitude flight over a 30 m elevation change swings GSD by
half.

---

## 6. Before you leave site

- [ ] All targets photographed in place with visible IDs
- [ ] Field log complete — every point ID, control vs. check, description
- [ ] Scanner: on-site registration run, no gaps
- [ ] Drone: all three passes flown, image counts recorded per flight
- [ ] Cards backed up to a second device **before** anything is formatted
- [ ] Targets collected (leave them if a return visit is likely — a surviving
      target is a free tie point next time)

---

## Sources

- [FARO — Laser Scanner Best Practices](https://knowledge.faro.com/Hardware/Focus/Focus/Laser_Scanner_Best_Practices)
- [DroneDeploy — Best Practices for GCPs and Checkpoints](https://help.dronedeploy.com/hc/en-us/articles/11138616177047-Best-Practices-for-Ground-Control-Points-GCPs-and-Checkpoints)
- [Emlid — Why you need ground control points for drone mapping](https://blog.emlid.com/why-you-need-to-use-ground-control-points-gcp-for-drone-mapping/)
- [Drones (MDPI) — Influence of the Inclusion of Off-Nadir Images on UAV-Photogrammetry Projects](https://doi.org/10.3390/drones8110662)
- [JOUAV — Guide to Using Ground Control Points](https://www.jouav.com/blog/ground-control-points.html)

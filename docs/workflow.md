# Reality Capture Workflow — FARO Scene TLS + DJI Mavic 3 Classic

End-to-end workflow for fusing registered terrestrial scans with drone imagery
into a single measurable, photoreal deliverable.

**Companion documents:**
[field-capture.md](field-capture.md) (on-site practice) ·
[naming-convention.md](naming-convention.md) (names and IDs)

---

## The three questions, answered up front

**1. Which file type should I export from FARO Scene?**
**Structured E57**, exported as *Scans – Ordered*, one multi-scan file. Keep a
decimated **LAZ** as the secondary. Details in §4.

**2. Should I capture ground control points in Scene to splice the drone data?**
**Yes — and on this aircraft it is mandatory, not a refinement.** The Mavic 3
Classic has no RTK, so its geotags are standalone GNSS: metres of horizontal
error and worse vertically. Without control you cannot place that imagery into
a scan project that is accurate to millimetres. Details in §2 and §3.

**3. What produces the best visualisation?**
A single fused mesh — scanner geometry, drone texture — built in
RealityCapture, then split into three deliverables: a Nanite mesh in Unreal for
the hero visual, 3D Tiles or Potree for the measurable web version, and
optionally a Gaussian splat trained on the *same solved camera poses* so it
lands in the same coordinate frame. Details in §9.

---

## Why control, and not just ICP

It is tempting to skip targets and align the drone cloud to the scan cloud
afterwards with ICP in CloudCompare. That does work, to a point, and §8 keeps
it as a fallback. But it can only apply a **rigid transform** — 6 degrees of
freedom, plus scale if you let it.

A non-RTK photogrammetric block does not fail rigidly. It fails by *deforming*:
the classic dome or bowl, where radial lens distortion trades off against
altitude in the bundle adjustment and bends the whole reconstruction, tens of
centimetres of vertical error in the middle of an otherwise convincing model.
No rigid transform removes that. ICP will simply spread the deformation around
and give you a plausible-looking average error.

Control points fix it properly, because they enter the bundle adjustment
itself: position, orientation, scale **and internal deformation**, solved
together. That is the difference, and it is why targets go down before either
sensor comes out of the case.

---

## Phase 0 — Plan

Assign the site code. Design the control layout on a site plan — see
[field-capture.md §2](field-capture.md#2-control-design-do-this-first-on-paper)
for counts, distribution and the vertical-spread rule.

**Pick your coordinate frame now.** Two options:

| | Local (scan project is master) | Georeferenced |
|---|---|---|
| Needs | Nothing beyond the scanner | Survey-grade GNSS/RTK rover or total station |
| Accuracy | Best *relative* accuracy — mm across the site | Relative accuracy plus real-world tie |
| Use when | Standalone visualisation, as-built, volumes | Must tie to site plans, GIS, other surveys |

**If you do not have a survey-grade GNSS rover, go local.** The scan project
becomes the master frame, control coordinates are read straight out of Scene,
and you get full relative accuracy with no extra equipment. This is the honest
recommendation for a Mavic 3 Classic workflow, and it loses you nothing unless
the deliverable must sit on a real-world grid.

If you go georeferenced, occupy each target with the rover, record the CRS and
geoid, and set the offset per
[naming-convention.md §4](naming-convention.md#4-coordinates-and-the-offset-trap).

## Phase 1 — Field capture

Per [field-capture.md](field-capture.md). Targets first, then scans, then
flights, all the same day.

## Phase 2 — Register in FARO Scene

1. Import scans, process (colourise if captured, apply the dark-scatter and
   edge-artifact filters).
2. Register. Target-based where you have targets; cloud-to-cloud to fill in.
   Automatic registration alone will not carry a large project.
3. **Verify targets one by one.** Confirm each detected target matches one you
   actually placed, and delete false detections — reflective signs, wheel
   hubs and window frames all get picked up as spheres. An error here
   cascades through everything downstream, and it is much cheaper to catch now.
4. Read the registration report before exporting anything:

   | Metric | Target |
   |---|---|
   | Mean target tension | ≤ 3 mm |
   | Scan point error / mean C2C distance | ≤ 5 mm |
   | Overlap between linked scans | ≥ 30–40% |

   Scene's own green/amber flags are the first filter; these are the numbers
   to hold yourself to on a controlled site. Anything red gets fixed now.
5. **Clean before export.** Remove people, vehicles, stray points and
   atmospheric noise. Every point you leave in becomes mesh blobs later, and
   cleaning a point cloud is far easier than cleaning a mesh.

## Phase 3 — Name and extract control in Scene

**This phase is the splice.** Everything else is ordinary processing.

1. **Promote control targets to project level.** A target detected inside a
   single scan has only that scan's local coordinates. You need the
   project-level object, which carries one registered coordinate in project
   space.

2. **Rename every control target to its field ID** — `GCP01`, `CHK03` — per
   [naming-convention.md §2](naming-convention.md#2-point-ids-the-part-that-must-match-across-software).
   Scene's defaults (`Target1`, `Sphere4`) are per-scan artefacts and are
   meaningless downstream. Cross-check every rename against the field log and
   the target photos.

   Rename **before** export. Renaming after you have started marking images in
   photogrammetry software orphans the picks.

3. **Export the target/object list** to CSV or TXT. Scene reads and writes
   control points in `.cor` and `.csv`, in the format
   `PointID X Y Z Accuracy` (`0` where accuracy is unknown) — the same format
   it accepts on import, which makes round-tripping easy.

   Menu paths move between Scene versions, so navigate by what you are after —
   the project-level object list, exported as text — rather than by a
   remembered click path.

4. **Sanity-check the export before you trust it.** Two things go wrong here,
   both silently:
   - **Units.** Confirm metres, not millimetres or feet.
   - **Axis convention.** Take a target you know is high — one on a roof —
     and confirm it has the larger Z. A flipped or swapped axis produces a
     solve that converges to something confidently wrong.

5. Write the hand-off file to `30_control/<SITE>_<DATE>_GCP_MEAS.csv`:

   ```csv
   name,x,y,z,type,acc_xy_m,acc_z_m,notes
   GCP01,1042.336,2018.774,31.209,control,0.003,0.005,nail in kerb NE corner
   GCP02,1098.115,2021.902,30.884,control,0.003,0.005,painted cross, car park
   CHK01,1070.441,2045.117,33.760,check,0.003,0.005,roof slab, W building
   ```

   Keep `control` and `check` rows in one file, flagged by `type`, so the split
   is documented in one place. Strip to bare `name,x,y,z` if your importer is
   fussy. Template: [`templates/gcp_field_log.csv`](../templates/gcp_field_log.csv).

## Phase 4 — Export point clouds from Scene

### Recommended: structured E57

Right-click **Scans → Export → Scans → Scans – Ordered**. "Ordered" is the
setting that matters — it preserves each scan's grid structure and setup
position rather than flattening everything to a single anonymous blob. Export
**all stations into one multi-scan E57** rather than one file per station;
it performs better downstream.

Structure is worth preserving because it gives downstream tools real
information: correct normal estimation from the scan grid, occlusion reasoning
from known setup positions, and — the reason it matters here — RealityCapture
and Metashape can use scan positions directly when aligning imagery against
scans. Flatten it and you throw all of that away.

E57 is ASTM E2807, open and vendor-neutral, carries RGB and intensity, and is
read by ReCap, Cyclone, RealWorks, CloudCompare and every photogrammetry
package worth using.

### Secondary: LAZ

A decimated LAZ (1–2 cm) for GIS hand-off, web viewers and anything that needs
to move over a network. LAS 1.4 point format 7 keeps RGB. It loses scan
structure, which is exactly why it is the secondary and not the primary. If
your Scene version has no native LAZ, export LAS and compress with LASzip.

### Format comparison

| Format | Verdict |
|---|---|
| **E57 (ordered)** | **Primary.** Structured, per-scan poses, RGB + intensity, open standard |
| **LAZ / LAS 1.4** | **Secondary.** Compact, universal, georeferenced; loses structure |
| RCP / RCS | Only if feeding Autodesk (Navisworks, Revit, Civil 3D). Via ReCap importing your E57 |
| PTX | Keeps structure and transform, but ASCII and enormous. Only for tools that demand it |
| PTS | Unstructured ASCII. No advantage over E57 |
| POD | Only for Bentley pipelines |
| XYZ | Avoid. Loses structure, intensity and metadata |
| FLS / LSPROJ | Native. Archive them, but not an interchange format |

Export full resolution to `10_tls/export/` for archival, plus a decimated
working copy — a 200-scan project at full density will not open interactively
in most downstream tools, and you do not want to be re-exporting at 11 pm.

## Phase 5 — Ingest drone imagery

```sh
tools/rename-uas-images.sh HRBR01 20260420 F01 \
  projects/HRBR01/20_uas/raw/F01 projects/HRBR01/20_uas/renamed/F01
```

Run it per flight. DJI restarts its counter at `DJI_0001` every flight, so
without this two flights collide the moment they share a folder. The script
copies rather than moves (originals stay pristine, EXIF untouched), keeps each
JPEG and its DNG on the same index, and writes a manifest mapping new names
back to originals.

Feed the **JPEGs** to photogrammetry. Keep the DNGs archived.

## Phase 6 — Solve the photogrammetry block with control

In RealityCapture, Metashape or Pix4D:

1. Import the renamed JPEGs. Enable **rolling shutter compensation** — the
   Classic's electronic shutter needs it.
2. Align / build the sparse block. Check it came out as **one component**.
   Multiple components mean insufficient overlap; fix that before proceeding.
3. **Import `<SITE>_<DATE>_GCP_MEAS.csv`** as control points, and set point
   accuracy to match the scanner (a few millimetres) rather than leaving the
   default GNSS-grade value — otherwise the solver under-weights precisely the
   measurements you want it to trust.
4. **Mark each control point in at least 8–10 images**, spread across
   different flight lines and both nadir and oblique passes. A point marked in
   three adjacent nadir frames constrains almost nothing. This is the tedious
   part and it is where the accuracy actually comes from.
5. **Import check points but exclude them from the solve.**
6. Re-run the bundle adjustment with control enabled.
7. **Read the residuals.** At 1.6 cm GSD:

   | Measure | Target | Investigate above |
   |---|---|---|
   | Control point RMSE | ≈ 1–2× GSD (1.5–3 cm) | 3× GSD |
   | **Check point RMSE** | ≤ 2–3× GSD (3–5 cm) | 4× GSD |
   | Reprojection error | < 1 px | 1.5 px |

   **The check point RMSE is your real accuracy number.** Control residuals
   only report how well the solve fit points it was given.

   One control point with residuals far above the rest is almost always a
   mis-pick or a mistyped coordinate, not a bad measurement. Re-examine it
   before you consider disabling it — and if you do disable it, say so in the
   QC record.

8. Build the dense cloud. The block is now in scan project coordinates.

## Phase 7 — Fuse

### Recommended: single-project fusion in RealityCapture

RealityCapture (shipping as RealityScan 2.x, free below $1M annual revenue)
ingests photos and laser scans in one project — E57, LAS, PTX, even FLS —
aligns them together and meshes and textures from both.

1. Import the ordered E57 **and** the drone imagery into one project.
2. Import control points; the scans are already in that frame, and the imagery
   gets brought in by the control from Phase 6.
3. Align. Verify a single component.
4. Mesh from the combined data — scanner geometry where it exists, photogram-
   metric geometry for roofs, canopy and everything the tripod could not see.
5. **Texture from the drone imagery**, not from scanner colour. Focus-series
   colour is serviceable for orientation and poor for presentation; 20 MP
   Hasselblad frames are dramatically better. This single choice is the largest
   visible quality difference in the final product.

Metashape 2.2+ is the alternative and now handles TLS properly — import E57/PTX
laser scans, combine with imagery for hybrid meshing, and there is a
`laser_scans_workflow.py` batch script in Agisoft's scripts repository.

### What each sensor contributes

Play to their strengths rather than averaging them:

| | Scans | Drone |
|---|---|---|
| Ground-level geometry, facades, interiors | **Authoritative** | Supplementary |
| Roofs, canopy, wide-area coverage | Occluded | **Authoritative** |
| Texture quality | Poor | **Authoritative** |
| Noise | ~2–6 mm | ~1–3 cm |

The scans are roughly 5–10× finer than 1.6 cm-GSD imagery, so where both see a
surface, the scan wins. Weight accordingly, or mask the photogrammetric
geometry out of scanned areas entirely.

## Phase 8 — QC

1. **Cloud-to-cloud comparison** in CloudCompare: drone dense cloud against
   scan cloud, on hard flat surfaces only — not vegetation, not water. Expect
   2–5 cm agreement. Use **M3C2** rather than plain C2C for a signed,
   statistically meaningful distance with confidence intervals.
2. **Look for a spatial pattern in the residuals.** A random scatter is noise
   and is fine. A smooth radial gradient — good at the edges, drifting in the
   middle — is residual doming, and means your control was too flat or too
   sparse in Z. Go back to Phase 6 before you mesh.
3. Check the check-point RMSE against Phase 6 targets.
4. Record it all in `60_qc/`, including the numbers you did not like. A
   deliverable whose accuracy is documented is worth considerably more than one
   that is merely asserted.

### Fallback: no usable control

If control was never placed, or the targets were destroyed:

1. Coarse-align with 4+ manual point pairs in CloudCompare.
2. Refine with ICP on overlapping hard surfaces.
3. **Report the result as an approximate alignment.** Expect centimetres to
   decimetres, with doming intact and unmeasurable.

Acceptable for visualisation. Not acceptable for measurement. Say which one
you are delivering.

## Phase 9 — Visualisation deliverables

Three outputs from one fused model, because no single format is good at
everything:

### a. Hero visual — Unreal Engine 5 + Nanite

Export the high-density fused mesh from RealityCapture and let Nanite handle
the triangle count rather than decimating first. Twinmotion is the quicker
route to a client-facing walkthrough from the same source. This is where the
drone-textured mesh pays off.

### b. Measurable web deliverable — 3D Tiles or Potree

Tile the decimated LAZ for Cesium (3D Tiles) or Potree. Point clouds remain
measurable in-browser, load progressively, and need no plugin. This is the
deliverable stakeholders actually open.

### c. Photoreal layer — 3D Gaussian splatting (optional)

For pure visual fidelity, splats currently beat meshes — no texture seams, and
they handle vegetation and thin structures that wreck mesh reconstruction.

**Train from the camera poses your photogrammetry already solved**, rather than
re-solving from scratch. Postshot imports RealityCapture alignments directly.
Because those poses are in scan coordinates, the resulting splat lands in the
same frame as everything else and overlays the mesh and point cloud without
further registration. That alignment is the whole trick, and it is free if you
export poses rather than starting over.

**Splats are for looking at, not measuring.** Ship them alongside the mesh and
point cloud, never instead of them.

### Choosing

| Need | Deliverable |
|---|---|
| Measurement, volumes, as-built | Point cloud (LAZ) + mesh |
| Client walkthrough, cinematic | UE5 / Twinmotion Nanite mesh |
| Share with non-technical stakeholders | Potree / Cesium in-browser |
| Maximum visual realism | Gaussian splat, over the mesh |
| Archive | Structured E57 + raw imagery + control CSV + this workflow |

---

## Sources

- [FARO — Laser Scanner Best Practices](https://knowledge.faro.com/Hardware/Focus/Focus/Laser_Scanner_Best_Practices)
- [FARO — File Format to Import Control Points into SCENE](https://knowledge.faro.com/Software/FARO_SCENE/SCENE/File_Format_to_Import_a_Series_of_Control_Points_into_SCENE)
- [FARO — Export Scan Settings in SCENE](https://knowledge.faro.com/Software/FARO_SCENE/SCENE/Export_Scan_Settings_in_SCENE)
- [Cintoo — Generate a Structured E57 Using FARO Scene](https://help.cintoo.com/en/support/solutions/articles/101000457037-generate-a-structured-e57-using-faro-scene)
- [DroneDeploy — Best Practices for GCPs and Checkpoints](https://help.dronedeploy.com/hc/en-us/articles/11138616177047-Best-Practices-for-Ground-Control-Points-GCPs-and-Checkpoints)
- [Drones (MDPI) — Influence of the Inclusion of Off-Nadir Images on UAV-Photogrammetry Projects](https://doi.org/10.3390/drones8110662)
- [Agisoft — Terrestrial laser scans processing in Metashape 2.2/2.3](https://agisoft.freshdesk.com/support/solutions/articles/31000168474-terrestrial-laser-scans-processing-in-metashape-2-2)
- [Drones (MDPI) — Fusion of UAV and Terrestrial Photogrammetry with Laser Scanning](https://www.mdpi.com/2504-446X/4/3/53)
- [ASTM E2807 / E57 format overview](https://www.cadinterop.com/en/formats/cloud-point/e57.html)

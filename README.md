# Reality Capture

Workflow and tooling for fusing **FARO Scene** terrestrial laser scans with
**DJI Mavic 3 Classic** drone imagery into a single measurable, photoreal model.

## Documentation

| Document | What it covers |
|---|---|
| [docs/workflow.md](docs/workflow.md) | End-to-end pipeline, Phase 0 → 9: planning, Scene registration and export, control extraction, photogrammetry, fusion, QC, visualisation deliverables |
| [docs/field-capture.md](docs/field-capture.md) | On-site practice: control design, scanner settings, flight planning, camera settings, checklists |
| [docs/roadway-uas-flight.md](docs/roadway-uas-flight.md) | Corridor-specific drone flight workflow: altitude ladder, gimbal angles, flight line geometry, cross-ties, corridor GCP layout, RealityCapture vs Pix4D |
| [docs/naming-convention.md](docs/naming-convention.md) | File names, point IDs, directory layout, coordinate offsets |

## Short answers

**Export format from FARO Scene** — structured E57 (*Scans – Ordered*), all
stations in one file, plus a decimated LAZ as secondary.
([why](docs/workflow.md#phase-4--export-point-clouds-from-scene))

**Ground control points** — yes, mandatory. The Mavic 3 Classic has no RTK, so
control is the only way to put its imagery into the scanner's coordinate frame
at matching accuracy, and the only thing that removes photogrammetric doming.
([why](docs/workflow.md#why-control-and-not-just-icp))

**Best visualisation** — one fused mesh in RealityCapture (scanner geometry,
drone texture), delivered three ways: Nanite mesh in Unreal for the hero
visual, 3D Tiles/Potree for the measurable web version, and optionally a
Gaussian splat trained on the same solved camera poses.
([how](docs/workflow.md#phase-9--visualisation-deliverables))

## Tooling

```sh
# Flight parameters: GSD, footprint, line spacing, trigger distance, max speed
tools/flight-calc.py --alt-ft 400 200 100 50

# Apply the naming convention to a card dump, one flight at a time
tools/rename-uas-images.sh HRBR01 20260420 F01 \
  projects/HRBR01/20_uas/raw/F01 \
  projects/HRBR01/20_uas/renamed/F01
```

`flight-calc.py` sizes a mission from an overlap spec — the max-speed column is
the one that matters, since flying faster than it silently thins your forward
overlap. `rename-uas-images.sh` copies rather than moves, keeps each JPEG and
its DNG on the same index, and writes a manifest back to the original
`DJI_nnnn` names.

## Templates

[`templates/gcp_field_log.csv`](templates/gcp_field_log.csv) — control point
field log, filled on site and completed from the Scene target export.

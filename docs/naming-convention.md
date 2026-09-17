# Naming Convention

One convention across every sensor, every file and every point ID. The whole
reason this document exists is the hand-off in
[the workflow](workflow.md): a control point measured in FARO Scene has to
carry **the exact same label** into RealityCapture or Metashape, or the
photogrammetry block cannot be tied to the scan data.

## 1. The general pattern

```
<SITE>_<YYYYMMDD>_<SENSOR>_<SUBSET>[_<INDEX>][_<VARIANT>].<ext>
```

| Field | Rule | Examples |
|---|---|---|
| `SITE` | 3–6 chars, `A–Z` and `0–9` only. Assigned once, never changes. | `HRBR01`, `MILL`, `BR27` |
| `YYYYMMDD` | **Acquisition** date, never the processing date. Sorts chronologically. | `20260420` |
| `SENSOR` | `TLS`, `UAS`, `GNSS`, `TS` (total station), `FUSE` (derived/merged) | `TLS` |
| `SUBSET` | Role-specific: scan station `S001`, flight `F01`, or a role word | `S007`, `F02`, `REG` |
| `INDEX` | Zero-padded to 4 | `0137` |
| `VARIANT` | Optional. Resolution, content or version. | `FULL`, `DEC01`, `V03` |

`VARIANT` vocabulary: `FULL` (source resolution), `DEC<nn>` (decimated to nn mm,
so `DEC01` = 1 cm), `RGB`, `INT` (intensity only), `DRAFT`, `V01`–`V99`.

### Examples

```
HRBR01_20260420_TLS_S007.fls            scan station 7, raw off the card
HRBR01_20260420_TLS_REG_FULL.e57        registered project, structured export
HRBR01_20260420_TLS_REG_DEC01.laz       same, decimated to 1 cm, for GIS
HRBR01_20260420_UAS_F02_0137.JPG        drone frame 137 of flight 2
HRBR01_20260420_UAS_F02_0137.DNG        its RAW sibling - same index
HRBR01_20260420_GNSS_GCP_MEAS.csv       measured control coordinates
HRBR01_20260420_FUSE_MESH_V03.obj       fused mesh, third iteration
```

## 2. Point IDs (the part that must match across software)

File names are for humans. **Point IDs live inside files and get parsed by
four different programs**, so they are deliberately shorter and dumber:
uppercase, alphanumeric, no separators, ≤5 characters.

| Role | Pattern | Range |
|---|---|---|
| Control point (used to solve the block) | `GCPnn` | `GCP01`–`GCP99` |
| Check point (**withheld** from the solve, used to measure accuracy) | `CHKnn` | `CHK01`–`CHK99` |
| Scale bar endpoints | `SBnnA` / `SBnnB` | `SB01A`, `SB01B` |
| Scanner station reference | `Snnn` | `S001`–`S999` |

No underscores, no spaces, no lowercase. Some importers truncate, some are
case-sensitive, some treat `_` as a delimiter — this pattern survives all of
them.

### Three rules that are not negotiable

1. **A point ID is bound to a physical location, permanently.** Never reuse
   `GCP04` for a different nail, on a different date, on a different site. If
   a target is destroyed, retire the number; don't recycle it.
2. **Never renumber after marking has started.** Once you have picked `GCP07`
   in forty drone images, renaming it orphans all forty picks.
3. **Decide control vs. check in the field, and write it on the field log.**
   Promoting a check point to control later invalidates your accuracy number,
   because you can't grade a solve using a point the solve already saw.

## 3. Directory layout

```
projects/HRBR01/
├── 00_field/                    field notes, photos of each target in place
│   └── HRBR01_20260420_GCP_FIELD.csv
├── 10_tls/
│   ├── raw/                     .fls straight off the card - READ ONLY
│   ├── scene/                   the .lsproj working project
│   ├── export/                  .e57 / .laz exports
│   └── reports/                 Scene registration report (PDF + values)
├── 20_uas/
│   ├── raw/                     untouched card dump, one dir per flight
│   ├── renamed/F01/ F02/        output of tools/rename-uas-images.sh
│   └── reports/                 flight logs
├── 30_control/
│   ├── HRBR01_20260420_GCP_MEAS.csv    name,x,y,z - the hand-off file
│   └── HRBR01_georef.json              CRS + the coordinate offset (§4)
├── 40_processing/               rc/ metashape/ cloudcompare/
├── 50_deliverables/             mesh/ pointcloud/ web/ splat/
└── 60_qc/                       residual reports, C2C/M3C2 comparisons
```

`raw/` directories are write-once. Everything downstream is reproducible from
them; nothing else in the tree is.

## 4. Coordinates and the offset trap

Record the coordinate reference system in `30_control/<SITE>_georef.json`
alongside the control file. If the project is georeferenced to a projected CRS,
**also record a subtracted offset**:

```json
{
  "crs_horizontal": "EPSG:6428",
  "crs_vertical": "EPSG:5703 (NAVD88, GEOID18)",
  "units": "m",
  "offset": { "x": 1042000.0, "y": 2018000.0, "z": 0.0 },
  "note": "Offset is SUBTRACTED from survey coords before import. Add it back on export."
}
```

Large coordinates — a UTM easting of 500 000 m, a State Plane northing in the
millions — get stored as 32-bit floats somewhere in almost every mesh and
game-engine pipeline, and 32-bit float has ~7 significant digits. At 2 000 000 m
that leaves you roughly 12 cm of resolution, which will shred a dataset you went
to the trouble of capturing at 5 mm. Subtract a round offset before meshing;
add it back when exporting a georeferenced product.

## 5. Enforcing it

`tools/rename-uas-images.sh` applies §1 to a card dump, keeps the JPEG and its
DNG sibling on the same index, writes a manifest mapping new names back to the
original `DJI_nnnn` names, and never touches the originals:

```sh
tools/rename-uas-images.sh HRBR01 20260420 F02 \
  projects/HRBR01/20_uas/raw/F02 \
  projects/HRBR01/20_uas/renamed/F02
```

DJI restarts its counter at `DJI_0001` and will happily produce that filename on
every flight, so renaming per flight before anything else is what keeps two
flights from colliding in one processing folder.

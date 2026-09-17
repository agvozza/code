# Templates

## `gcp_field_log.csv`

Copy to `projects/<SITE>/00_field/<SITE>_<DATE>_GCP_FIELD.csv` and fill in on
site. Leave `x,y,z` blank in the field — they get populated in Phase 3 from the
FARO Scene target export, or from the GNSS rover on a georeferenced job.

| Column | Notes |
|---|---|
| `name` | Point ID per [naming-convention.md §2](../docs/naming-convention.md#2-point-ids-the-part-that-must-match-across-software). Must match the Scene target name exactly. |
| `x,y,z` | Metres, in the project coordinate frame. Filled in Phase 3. |
| `type` | `control` or `check`. **Decide in the field** — promoting a check point later invalidates your accuracy number. |
| `acc_xy_m`, `acc_z_m` | Expected accuracy. Set these to scanner accuracy (millimetres) so the bundle adjustment weights them properly, not to a GNSS-grade default. |
| `target_size_cm` | 50–60 cm for flights at 50–80 m; ≥5× GSD is the rule. |
| `scene_target_type` | `checkerboard` or `sphere` — what Scene auto-detects over the physical mark. |
| `notes` | Physical description. Worth its weight three days later. |

The pre-filled rows are a starting layout: 8 control + 3 check. Adjust to the
site, and keep at least one control and one check point at a **different
elevation** from the rest — that is what constrains the vertical and prevents
doming.

Export the finished file, with coordinates, to
`projects/<SITE>/30_control/<SITE>_<DATE>_GCP_MEAS.csv`.

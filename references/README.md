# References — 2021 Toyota RAV4 CDR / EDR Inspection

Supporting documents for VIN **2T3A1RFV8MC233488**
(2021 RAV4 XLE Premium · A25A-FKS 2.5L gasoline · AWD · built Cambridge, Ontario).

Companion field sheet: https://claude.ai/code/artifact/cc902ac7-a7e8-49a0-8fa8-4a184e3bdd32

---

## Contents

| File | Pages / size | Source | Notes |
|---|---|---|---|
| `2021-RAV4-Owners-Manual.pdf` | 748 pp · 32 MB | Toyota (via dealereprocess CDN) | ✅ Correct vehicle and year. Fuse section pp. 616–618. **Contains no fuse name/position table** — see below. |
| `2021-RAV4-Quick-Reference-Guide.pdf` | 68 pp · 5.4 MB | Toyota CDN (`assets.sia.toyota.com`) | Toyota doc ID `00505QRG21RAV4` — RAV4-specific, MY2021. Consumer-level overview. |
| `Bosch-CDR-v24.3-Vehicle-Coverage-List.pdf` | 149 pp · 1 MB | Bosch Diagnostics | Verified: `2003 & newer · Toyota · RAV4 · ACM · Where sold`. Canada included. |
| `Toyota-ERG-general.pdf` | 116 pp · 10 MB | techinfo.toyota.com (pre-login) | ⚠ **Generic**, not vehicle-specific. Scanned printout of Toyota's first-responder e-learning deck — no text layer, no RAV4 section. Kept for general SRS handling guidance only. |
| `RAV4-XA50-fuse-tables.md` | — | Compiled | Fuse tables assembled from published sources, with source conflicts flagged. |
| `fuse-box-diagrams/` | 5 PNG | fuse-box.info | Position-grid layouts and box locations. Third-party redraws, **not** Toyota lid art. |

---

## Two findings worth knowing

**1. The owner's manual has no fuse chart.**
For this generation Toyota moved the fuse legend entirely onto the physical box lid. Page 617 reads:
*"The amperage rating can be found on the fuse box lid."* There is no name/position table anywhere in
the 748 pages. This means photographing the box lid is not merely best practice — **it is the only
authoritative source available without a TIS subscription.** Every position number in
`RAV4-XA50-fuse-tables.md` is a third-party claim.

The manual does confirm box locations and access method (pp. 616–617):
IJB at the **left side instrument panel, remove the lid**; engine-compartment boxes open by
**releasing claws A and B, then lifting**.

**2. The electrical wiring diagram is not in this folder — deliberately.**

The XA50 EWD is a Toyota copyrighted publication sold through **techinfo.toyota.com** (TIS). No
legitimate free public copy exists. Search results for it lead to pirate aggregators
(`nutrocar`, `pdfcoffee`, Scribd re-uploads) or to **wrong-generation documents** — the widely
circulated "Toyota RAV4 EWD" PDF on frankensteinmotorworks.com is a **2GR-FE V6 car**, an entirely
different platform from this XA50. Using it here would be worse than having nothing.

**Legitimate route:** a short-term TIS subscription at https://techinfo.toyota.com — reported around
**$15–25 for two-day access** (confirm current pricing at checkout; it has changed over time). That
covers electrical wiring diagrams, repair manuals, collision repair manuals, and the vehicle-specific
emergency response guide.

**The specific page to pull:** *Power Source / Power Distribution* for this VIN — it is the only
document that names which `ECU-IG1` branch feeds the forward recognition camera, and it gives you
Toyota's own fuse positions, which retires the warning above entirely.

While you are in TIS, the **vehicle-specific Emergency Response Guide** is worth pulling too — it maps
every airbag inflator and pretensioner for this exact model, which is a better squib inventory than the
generic deck in this folder.

---

## Provenance and handling

All files here were retrieved from public URLs on 2026-09-02 and are third-party copyrighted
publications retained for reference during this inspection.

The PDFs and the images in `fuse-box-diagrams/` are **gitignored** — held as a local working set
rather than redistributed through this repository. Reproduce them on a fresh checkout with:

```
bash references/fetch-sources.sh
```

Committing them instead is a deliberate decision, not a default: pushing ~48 MB of third-party
manuals to a remote is redistribution, which is separate from holding a working copy. Only
`README.md`, `RAV4-XA50-fuse-tables.md` and `fetch-sources.sh` are tracked.

Third-party fuse tables are secondary sources. Any report should cite the **on-vehicle lid
photograph** and, where available, the TIS EWD page — not these files.

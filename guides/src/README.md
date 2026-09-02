# Toyota Techstream guides — source

Three PDFs are built from this directory:

| Output | Source | Page size |
| --- | --- | --- |
| `../Toyota Techstream Imaging Guide.pdf` | `guide.html` + `img/` | US Letter |
| `../Toyota Techstream Data Acquisition Steps.pdf` | `steps.html` + `img/` | US Letter |
| `../Toyota Techstream Data Acquisition — Phone.pdf` | `steps-phone.html` + `img-phone/` | 390 × 780 pt |
| `../Toyota GTS+ Data Acquisition — Phone.pdf` | `steps-gts-phone.html` + `img-gts/` | 390 × 780 pt |

The phone edition is sized to an iPhone viewport so a page fills the screen at
1:1 with no pinch-zoom for the text. `img-phone/` holds the same screenshots
cropped to the individual control each step names, since a full application
window is unreadable at phone width.

Screenshots were extracted from the source decks in `../../files/`:

| Prefix | Source |
| --- | --- |
| Setup, retrieval, PCS Data Viewer figures | `TechStream How-to - FOR PDF.pdf` (Brad Muir, Crash Data Specialists) |
| In-Techstream VCH list and trigger event figures | `Toyota-Techstream-21-slides-by-MAIT.pdf` (E. Clarke, CHP MAIT) |

## Rebuilding

```sh
pip install pymupdf pillow
chromium --headless --disable-gpu --no-sandbox --no-pdf-header-footer \
    --print-to-pdf=guide_raw.pdf --virtual-time-budget=25000 guide.html
```

Then stamp the running footer and page numbers onto every page except the cover,
and write the document metadata, with PyMuPDF (`build_footer.py`).

## GTS+ edition

Global Techstream+ replaced Techstream, which Toyota discontinued in September 2024. The folder held
no GTS+ procedure, so the screens in `img-gts/` were cropped from Toyota documentation retrieved
from techinfo.toyota.com and techdoc-toyota.com and added to `../../files/`:

- `Techinfo TS Lite AM Installation Instructions v4.1 (GTS+).pdf` — login, VIM selection, Connect to
  Vehicle, Vehicle Connection, Main Menu, Health Check
- `GTS+ Independent User Guide (Toyota).pdf` — Stored Data, Vehicle Control History, offline limit,
  file locations
- `GTS+ Known Bugs V2023.04.003.02.pdf` — the printing workarounds
- `Techinfo TS Lite AM FAQ v4.0.pdf` — subscription and support

The `PCS FFD Retrieval` prompts are described from the Techstream sequence and practitioner reports;
no published GTS+ document illustrates them. The guide says so on the page where it matters.

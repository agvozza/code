# Toyota Techstream guides — source

Three PDFs are built from this directory:

| Output | Source | Page size |
| --- | --- | --- |
| `../Toyota Techstream Imaging Guide.pdf` | `guide.html` + `img/` | US Letter |
| `../Toyota Techstream Data Acquisition Steps.pdf` | `steps.html` + `img/` | US Letter |
| `../Toyota Techstream Data Acquisition — Phone.pdf` | `steps-phone.html` + `img-phone/` | 390 × 780 pt |

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

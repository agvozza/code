# Toyota Techstream Imaging Guide — source

`../Toyota Techstream Imaging Guide.pdf` is generated from `guide.html` and the
screenshots in `img/`.

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

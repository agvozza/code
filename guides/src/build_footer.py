"""Stamp the running footer and page numbers onto the Chromium-rendered guide."""
import os
import sys

import pymupdf

SRC = sys.argv[1] if len(sys.argv) > 1 else "guide_raw.pdf"
OUT = sys.argv[2] if len(sys.argv) > 2 else "Toyota Techstream Imaging Guide.pdf"

GREY = (0.35, 0.40, 0.45)
RULE = (0.72, 0.76, 0.80)

doc = pymupdf.open(SRC)
for i, page in enumerate(doc):
    if i == 0:  # cover carries no footer
        continue
    width, height = page.rect.width, page.rect.height
    y = height - 40
    page.draw_line((54, y), (width - 54, y), color=RULE, width=0.6)
    page.insert_text((54, y + 13), "Toyota Techstream Imaging Guide",
                     fontname="times-italic", fontsize=8.5, color=GREY)
    label = f"Page {i} of {doc.page_count - 1}"
    text_width = pymupdf.get_text_length(label, fontname="times-roman", fontsize=8.5)
    page.insert_text((width - 54 - text_width, y + 13), label,
                     fontname="times-roman", fontsize=8.5, color=GREY)

doc.set_metadata({
    "title": "Toyota Techstream Imaging Guide",
    "subject": "Vehicle Control History, PCS Freeze Frame Data and forward-facing camera image retrieval",
    "keywords": "Toyota, Lexus, Techstream, Vehicle Control History, VCH, PCS, FFD, EDR, imaging guide",
    "creator": "",
    "author": "",
})
doc.save(OUT, garbage=4, deflate=True)
print(f"wrote {OUT} ({doc.page_count} pages, {os.path.getsize(OUT)} bytes)")

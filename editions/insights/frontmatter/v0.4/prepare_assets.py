"""Rebuild local PDF assets from an external approved report and repo SVG.

No PDF, font or original report is stored in Git. See README.md for dependencies.
"""
from pathlib import Path
import argparse
import hashlib
import os
import subprocess

import fitz
from fontTools.ttLib import TTCollection

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[3]
SOURCE_SHA = "675c3490c45d5fc4b51ca0c9ae2ddd5bb330abc108f148435d7317c221579a66"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-pdf", default=os.environ.get("GOSD_2026_SOURCE_PDF"))
    parser.add_argument("--cover-font", default=os.environ.get(
        "GOSD_COVER_FONT", "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"))
    args = parser.parse_args()
    if not args.source_pdf:
        parser.error("Set GOSD_2026_SOURCE_PDF or pass --source-pdf (external 173-page mother report).")
    source = Path(args.source_pdf).expanduser().resolve()
    if not source.is_file() or hashlib.sha256(source.read_bytes()).hexdigest() != SOURCE_SHA:
        parser.error("The external mother report does not match the registered SHA-256.")
    font_path = Path(args.cover_font).expanduser().resolve()
    if not font_path.is_file():
        parser.error("Liberation Serif Bold font is missing; supply GOSD_COVER_FONT.")
    font_dir = ROOT / '.build/fonts'
    font_dir.mkdir(parents=True, exist_ok=True)
    for family in ['Sans', 'Serif']:
        for weight in ['Regular', 'Bold']:
            target = font_dir / f'Noto{family}CJKsc-{weight}.otf'
            if not target.exists():
                fonts = TTCollection(f'/usr/share/fonts/opentype/noto/Noto{family}CJK-{weight}.ttc')
                assert fonts.fonts[2]['name'].getDebugName(6) == f'Noto{family}CJKsc-{weight}'
                fonts.fonts[2].save(target)
                fonts.close()
    output = ROOT / ".build/assets"
    output.mkdir(parents=True, exist_ok=True)
    with fitz.open(source) as original, fitz.open() as cover:
        if len(original) != 173:
            parser.error("Expected a 173-page mother report.")
        cover.insert_pdf(original, from_page=0, to_page=0)
        page = cover[0]
        spans = [span for block in page.get_text("dict")["blocks"]
                 for line in block.get("lines", []) for span in line["spans"]
                 if span["text"] == "OSDGs"]
        if len(spans) != 2:
            parser.error("Expected exactly two OSDGs cover labels; refusing an ambiguous edit.")
        for span in spans:
            page.add_redact_annot(fitz.Rect(span["bbox"]), fill=False)
        page.apply_redactions(images=0, graphics=0, text=0)
        font = fitz.Font(fontfile=str(font_path))
        for span in spans:
            size = span["size"]
            x, y = span["origin"]
            if size > 20:
                x = (span["bbox"][0] + span["bbox"][2]
                     - font.text_length("GOSD", fontsize=size)) / 2
            c = span["color"]
            color = ((c >> 16 & 255) / 255, (c >> 8 & 255) / 255, (c & 255) / 255)
            page.insert_text((x, y), "GOSD", fontname="gosdcover", fontfile=str(font_path),
                             fontsize=size, color=color)
        cover.save(output / "cover2026-gosd.pdf", garbage=4, deflate=True)
    svg = REPO / "brand/osdgs/v2.0/assets/master/osdgs-symbol-compact.svg"
    subprocess.run(["inkscape", str(svg), "--export-type=pdf",
                    f"--export-filename={output / 'osdgs-compact.pdf'}"], check=True,
                   capture_output=True, text=True)
    print("Prepared two local PDF assets; neither is a repository input.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Verify the public archive, not the report's research claims or full build."""
import argparse
import ast
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
INVENTORY = "provenance/archive-file-manifest.json"
IGNORED = {"work", "local-inputs", "__pycache__"}
ALLOWED = {".md", ".tex", ".sty", ".py", ".sh", ".json", ".csv", ".txt", ".svg"}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_file(relative):
    path = PurePosixPath(relative)
    require(not path.is_absolute() and ".." not in path.parts and "\\" not in relative,
            f"Unsafe path: {relative}")
    resolved = ROOT.joinpath(*path.parts)
    require(not resolved.is_symlink(), f"Symlink is not allowed: {relative}")
    return resolved


def read_json(relative):
    return json.loads(safe_file(relative).read_text(encoding="utf-8"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference-pdf", type=Path)
    args = parser.parse_args()
    manifest = read_json(INVENTORY)
    entries = manifest["files"]
    expected = {item["path"] for item in entries}
    require(len(expected) == len(entries), "Duplicate file in inventory")
    actual = {
        p.relative_to(ROOT).as_posix() for p in ROOT.rglob("*")
        if p.is_file() and not (set(p.relative_to(ROOT).parts) & IGNORED)
        and p.relative_to(ROOT).as_posix() != INVENTORY
    }
    require(actual == expected, f"Inventory differs: missing={expected-actual}; extra={actual-expected}")
    counts = {"files": len(entries), "json": 0, "python": 0, "svg": 0}
    for item in entries:
        relative = item["path"]
        path = safe_file(relative)
        require(path.suffix.lower() in ALLOWED or path.name in {".gitignore", "SHA256SUMS", "LICENSE", "Makefile"},
                f"Unexpected file type: {relative}")
        require(not ({"source_inputs", "sources", "baseline"} & set(path.relative_to(ROOT).parts)),
                f"Private input directory in archive: {relative}")
        raw = path.read_bytes()
        require(len(raw) == item["bytes"] and digest(raw) == item["sha256"], f"Fingerprint mismatch: {relative}")
        text = raw.decode("utf-8")
        require("\x00" not in text, f"Binary content: {relative}")
        if path.suffix == ".json":
            json.loads(text)
            counts["json"] += 1
        elif path.suffix == ".py":
            ast.parse(text, filename=relative)
            counts["python"] += 1
        elif path.suffix == ".svg":
            ET.fromstring(text)
            require(not re.search(r"data:image|;base64,", text, re.I), f"Embedded raster image: {relative}")
            counts["svg"] += 1

    sources = read_json("provenance/source-manifest.json")
    for item in sources["archived_sources"]:
        raw = safe_file(item["path"]).read_bytes()
        require(len(raw) == item["bytes"] and digest(raw) == item["sha256"],
                f"Original source changed: {item['path']}")
    canonical = sources["canonical_review"]
    pages = read_json("text/pages.json")
    require(pages["source_sha256"] == canonical["sha256"], "Wrong full-report source")
    require(pages["page_count"] == len(pages["pages"]) == canonical["pages"] == 173, "Full-report page count")
    require(len(pages["bookmarks"]) == canonical["bookmarks"] == 144, "Bookmark count")
    for number, page in enumerate(pages["pages"], 1):
        require(page["page"] == number, "Page order")
        require(digest(page["text"].encode("utf-8")) == page["text_sha256"], f"Text fingerprint: page {number}")
        require(page["height_pt"] > page["width_pt"], f"Unexpected orientation: page {number}")

    ch5 = "source/chapters/05-recovered/"
    recovered = read_json(ch5 + "page-manifest.json")
    require(recovered["input_sha256"] == "d44536ae4de6be29654b6f5932e7593003ba7acc0e89d664cece358b4182dc5a", "Wrong fifth-chapter PDF")
    require(len(recovered["pages"]) == 17, "Recovered chapter page count")
    figures = read_json(ch5 + "figure-inventory.json")
    require([x["figure"] for x in figures] == [f"5-{n}" for n in range(1, 15)], "Recovered figure inventory")
    for number, page in enumerate(recovered["pages"], 1):
        require(page["page"] == number and page["full_book_page"] == number + 136, "Recovered page mapping")
        require(digest(safe_file(ch5 + page["text_file"]).read_bytes()) == page["text_utf8_sha256"],
                f"Recovered text fingerprint: page {number}")
    for line in safe_file(ch5 + "SHA256SUMS").read_text().splitlines():
        sha, relative = line.split("  ", 1)
        require(digest(safe_file(ch5 + relative).read_bytes()) == sha, f"Chapter recovery checksum: {relative}")

    parts = read_json(ch5 + "text-blocks.parts/index.json")
    chunks = []
    for part in parts["parts"]:
        raw = safe_file(ch5 + "text-blocks.parts/" + part["name"]).read_bytes()
        require(len(raw) == part["size"] and digest(raw) == part["sha256"], "Text-block part mismatch")
        raw.decode("utf-8")
        chunks.append(raw)
    restored = b"".join(chunks)
    require(len(restored) == parts["size"] and digest(restored) == parts["sha256"], "Text-block reconstruction mismatch")
    json.loads(restored)
    counts["chapter5_text_block_parts"] = len(chunks)

    if args.reference_pdf:
        import fitz
        require(digest(args.reference_pdf.read_bytes()) == canonical["sha256"], "Reference PDF fingerprint mismatch")
        with fitz.open(args.reference_pdf) as doc:
            require(len(doc) == 173 and doc.get_toc() == pages["bookmarks"], "Reference PDF structure mismatch")
            require(sum(len(page.get_links()) for page in doc) == canonical["links"], "Reference PDF link count")
            for page, saved in zip(doc, pages["pages"]):
                require(page.get_text("text", sort=False) == saved["text"], f"Reference text mismatch: {page.number + 1}")
        counts["reference_pdf_pages_matched"] = 173
    counts["original_source_files_matched"] = len(sources["archived_sources"])
    counts["chapter5_recovered_pages"] = 17
    counts["chapter5_figure_entries"] = 14
    counts["result"] = "PASS: archive integrity only; no full typesetting or research recertification"
    print(json.dumps(counts, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

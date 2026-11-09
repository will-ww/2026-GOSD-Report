"""Validate edition links, structured records and files that would enter Git."""
from pathlib import Path
from collections import Counter
import json
import hashlib
import re
import subprocess
from urllib.parse import unquote

EDITION = Path(__file__).resolve().parents[1]
REPO = EDITION.parents[1]
errors = []


def require(condition, message):
    if not condition:
        errors.append(message)


def read(relative):
    return json.loads((EDITION / relative).read_text(encoding="utf-8"))


def main():
    sources = read("evidence/sources.json")["sources"]
    source_ids = {s["id"] for s in sources}
    require(len(source_ids) == len(sources), "Duplicate source IDs")
    claims = read("data/insights.json")
    insights = claims["insights"]
    require([c["id"] for c in insights] == [f"I{n:02}" for n in range(1, 13)],
            "Expected I01–I12 exactly once")
    require(Counter(c["group"] for c in insights) == Counter(dict.fromkeys("ABCD", 3)),
            "Expected four groups of three")
    require({g["id"] for g in claims["groups"]} == set("ABCD"), "Invalid insight groups")
    insight_ids = {c["id"] for c in insights}
    known_status = {"待检验", "证据支持", "需收窄", "不支持"}
    for c in insights:
        require(c["evidence_status"] in known_status, f"Invalid status: {c['id']}")
        require(bool(c["required_evidence"] and c["counterevidence_or_limit"]),
                f"Missing evidence requirement or limit: {c['id']}")
        require(set(c["source_ids"]) <= source_ids, f"Unknown source: {c['id']}")
    ledger = read("evidence/ledger.json")["records"]
    require(len(ledger) == 12 and {r["insight_id"] for r in ledger} == insight_ids,
            "Evidence ledger must cover all twelve insights")
    for r in ledger:
        require(set(r["source_ids"]) <= source_ids, f"Unknown ledger source: {r['insight_id']}")
    for name, prefix in [("outlooks", "T"), ("recommendations", "R")]:
        records = read(f"data/{name}.json")["items"]
        require([r["id"] for r in records] == [f"{prefix}{n:02}" for n in range(1, 11)],
                f"Expected ten distinct records in {name}")
        for r in records:
            require(set(r["source_ids"]) <= source_ids, f"Unknown source: {r['id']}")
            require(set(r["insight_ids"]) <= insight_ids, f"Unknown insight: {r['id']}")
            if r["status"] != "未撰写":
                require(bool(r["title"] and r["source_ids"] and r["insight_ids"]),
                        f"Drafted record missing title or evidence: {r['id']}")
            if name == "outlooks":
                require(r["window"]["anchor"] == "actual_publication_date",
                        f"Forecast must use actual publication date: {r['id']}")
    current = read("current.json")
    require(current["main_window"] == {"start": "2025-07-01", "end": "2026-06-30"},
            "Main statistical window changed")
    require(current["pdf_in_repository"] is False, "PDF publication policy changed")
    snapshot = read("releases/frontmatter-v0.3.json")
    for name, expected in snapshot["source_file_sha256"].items():
        p = EDITION / "frontmatter/v0.3" / name
        require(p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest() == expected,
                f"Archived v0.3 source fingerprint changed: {name}")

    # Tracked and unignored prospective files only: ignored local build output is allowed.
    paths = subprocess.check_output(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"], cwd=REPO
    ).decode().split("\0")
    forbidden = {".pdf", ".ttf", ".otf", ".ttc", ".woff", ".woff2",
                 ".zip", ".7z", ".gz", ".tar"}
    selected = []
    for name in filter(None, paths):
        p = REPO / name
        if not p.is_file():
            continue
        require(p.suffix.lower() not in forbidden, f"Forbidden repository file: {name}")
        with p.open("rb") as f:
            head = f.read(8)
        require(not head.startswith((b"%PDF-", b"ttcf", b"wOFF", b"wOF2")),
                f"Disguised PDF or font: {name}")
        if p.is_relative_to(EDITION):
            selected.append(p)
    for p in selected:
        if p.suffix == ".json":
            json.loads(p.read_text(encoding="utf-8"))
        if p.suffix == ".md":
            for target in re.findall(r"\]\(([^)]+)\)", p.read_text(encoding="utf-8")):
                if re.match(r"(?:https?://|mailto:|#)", target):
                    continue
                relative = unquote(target.split("#", 1)[0])
                require((p.parent / relative).exists(),
                        f"Broken local link in {p.relative_to(REPO)}: {target}")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"PASS: {len(selected)} edition files; 12 insights, 10 outlook slots, "
          "10 recommendation slots; references and repository exclusion rules valid.")


if __name__ == "__main__":
    main()

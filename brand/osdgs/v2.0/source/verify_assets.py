#!/usr/bin/env python3
"""Verify approved SVG bytes, then emit the per-file reuse index. Never accept drift."""
from pathlib import Path
import hashlib
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]

def main():
    registry = json.loads((ROOT / 'approved-assets.json').read_text(encoding='utf-8'))
    files = sorted(p for directory in registry['folders'] for p in (ROOT / directory).glob('*.svg'))
    records = []
    problems = []
    for path in files:
        rel = path.relative_to(ROOT).as_posix()
        records.append({'path': rel, 'sha256': hashlib.sha256(path.read_bytes()).hexdigest()})
        if rel.startswith('assets/master/'):
            nodes = [el.attrib['data-dimension'] for el in ET.parse(path).iter() if 'data-dimension' in el.attrib]
            if nodes != [f'D{i:02d}' for i in range(1, 11)]:
                problems.append('invalid node order: ' + rel)
    payload = ''.join(r['path'] + '\0' + r['sha256'] + '\n' for r in records)
    aggregate = hashlib.sha256(payload.encode('utf-8')).hexdigest()
    if len(records) != registry['svg_count']:
        problems.append(f"Expected {registry['svg_count']} SVGs, found {len(records)}")
    if aggregate != registry['aggregate_sha256']:
        problems.append('SVG fingerprints differ from approved review: ' + aggregate)
    tokens = json.loads((ROOT / 'source/brand_tokens.json').read_text(encoding='utf-8'))
    expected = ['规模与密度','生态多样性','代码产出','模型开放供给','数据开放供给','代码影响力','模型影响力','数据集影响力','治理成熟度','公共福祉']
    if tokens['name_zh'] != '开源发展目标':
        problems.append('invalid Chinese name')
    if [d['name_zh'] for d in tokens['dimensions']] != expected:
        problems.append('dimension names changed')
    if sum(d['candidate_indicator_count'] for d in tokens['dimensions']) != 29:
        problems.append('candidate hierarchy changed')
    if problems:
        raise SystemExit('\n'.join(problems))
    result = {'version': '2.0.0', 'approved_on': registry['approved_on'], 'svg_count': len(records), 'aggregate_sha256': aggregate, 'assets': records}
    (ROOT / 'assets-index.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"PASS: {len(records)} exact approved SVGs; ten node identities; four-pillar/ten-dimension registry")

if __name__ == '__main__':
    main()

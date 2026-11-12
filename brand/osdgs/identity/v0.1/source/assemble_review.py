#!/usr/bin/env python3
"""Assemble six vector PDF pages, preserving embedded Chinese fonts."""
from pathlib import Path
from pypdf import PdfReader, PdfWriter

ROOT=Path(__file__).resolve().parents[1]
titles=['标识总览','四支柱与十维','图形语义','深浅底与使用尺度','五段主线与价值路径','应用与评审依据']
w=PdfWriter()
for i,title in enumerate(titles,1):
    r=PdfReader(ROOT/'pages'/f'page-{i:02}.pdf')
    assert len(r.pages)==1
    w.add_page(r.pages[0])
    w.add_outline_item(title,i-1)
w.add_metadata({
    '/Title':'OSDGs 开源发展目标：动态星座配套标识体系 v0.1',
    '/Author':'2026 全球开源发展报告项目',
    '/Subject':'四支柱与十个观察方向的配套标识设计评审稿',
    '/Keywords':'OSDGs,开源发展目标,动态星座,标识体系,评审稿',
    '/Creator':'OSDGs vector identity renderer',
})
with (ROOT/'review.pdf').open('wb') as f:w.write(f)
print('Created review.pdf: 6 vector pages, embedded fonts retained')

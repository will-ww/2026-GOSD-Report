#!/usr/bin/env python3
"""Recover the verified v0.1r PDF text layer; never emit PDF, images or fonts."""
import argparse, hashlib, json, re, subprocess
from pathlib import Path
import fitz
EXPECTED = 'd44536ae4de6be29654b6f5932e7593003ba7acc0e89d664cece358b4182dc5a'
def sha(b): return hashlib.sha256(b).hexdigest()
def dump(path, obj): path.write_text(json.dumps(obj, ensure_ascii=False, indent=2)+'\n',encoding='utf-8')
def section(n):
    return 'cover' if n == 1 else 'introduction' if n == 2 else '5.1' if n <= 6 else '5.2' if n <= 11 else '5.3' if n <= 16 else 'reflection'
def main():
    a=argparse.ArgumentParser(description=__doc__); a.add_argument('pdf',type=Path); a.add_argument('--out',type=Path,required=True); args=a.parse_args()
    digest=sha(args.pdf.read_bytes())
    if digest != EXPECTED: raise SystemExit('Wrong input SHA-256: refusing to relabel a different version.')
    out=args.out; (out/'pages').mkdir(parents=True,exist_ok=True)
    raw=subprocess.check_output(['pdftotext','-layout','-enc','UTF-8',str(args.pdf),'-'])
    pages=raw.decode('utf-8').split('\f'); assert len(pages)==18 and not pages[-1].strip()
    doc=fitz.open(args.pdf); assert len(doc)==17
    (out/'text-layer-layout.txt').write_bytes(raw)
    manifest=[]; structured=[]; inventory=[]
    md=['# 第五章 v0.1r：PDF 文本层恢复稿（非原始排版源码）','',
        '本文件按最终 17 页 PDF 的物理页序保存可编辑文本。仅增加页标题与文本围栏；不更改提取正文。图形、曲线、地图几何和转为轮廓的文字不在文本层中。未重新认证统计或法律判断。见 README.md。','']
    for i,page in enumerate(doc):
        n=i+1; text=pages[i]; name=f'page-{n:02}.txt'; (out/'pages'/name).write_text(text,encoding='utf-8')
        blocks=page.get_text('dict',flags=fitz.TEXTFLAGS_DICT & ~fitz.TEXT_PRESERVE_IMAGES)['blocks']
        links=[{'uri':x['uri'],'rect':list(x['from'])} for x in page.get_links() if 'uri' in x]
        pix=page.get_pixmap(matrix=fitz.Matrix(1,1),colorspace=fitz.csRGB,alpha=False)
        stream=b''.join(doc.xref_stream(x) for x in page.get_contents())
        manifest.append({'page':n,'full_book_page':136+n,'section':section(n),'text_file':f'pages/{name}',
          'text_utf8_sha256':sha(text.encode()),'pdf_content_stream_concat_sha256':sha(stream),
          'render_rgb_72dpi_sha256':sha(pix.samples),'render_width':pix.width,'render_height':pix.height,
          'page_width_pt':page.rect.width,'page_height_pt':page.rect.height,
          'text_characters':len(text),'pdf_image_references':len(page.get_images()),'vector_drawing_count':len(page.get_drawings())})
        structured.append({'page':n,'section':section(n),'coordinate_units':'PDF points; top-left origin','text_blocks':blocks,'links':links})
        plain=page.get_text()
        cap=re.search(r'图5[‑-](\d+)\s*([^\n]+)',plain)
        if cap:
            inventory.append({'figure':f'5-{cap[1]}','page':n,'section':section(n),'title':cap[2].strip(),
               'source_links':[x['uri'] for x in links],'status':'Caption and text layer recovered; chart artwork and numerical source not reconstructed.'})
        md += [f'## 第 {n} 页 | 全书第 {136+n} 页 | {section(n)}','', '```text',text.rstrip('\n'),'```','']
    assert len(inventory)==14
    (out/'chapter5-v0.1r-editable-text.md').write_text('\n'.join(md),encoding='utf-8')
    dump(out/'page-manifest.json',{'input_filename':'GOSD_2026_第五章_清洁整理_v0.1r_重建评审稿.pdf','input_sha256':digest,'pages':manifest,
        'hash_definitions':{'text':'Exact UTF-8 per-page pdftotext -layout output, including whitespace; excludes form-feed page separators.',
        'content_stream':'Concatenated decoded page /Contents streams in PDF order; does not include referenced objects and is NOT a self-contained page hash.',
        'render':'Raw RGB samples at 72dpi, alpha=False, PyMuPDF '+fitz.VersionBind+'; renderer-version dependent; no images exported.'},
        'tools':{'PyMuPDF':fitz.VersionBind,'pdftotext':subprocess.run(['pdftotext','-v'],capture_output=True,text=True).stderr.strip()}})
    dump(out/'text-blocks.json',structured); dump(out/'figure-inventory.json',inventory)
    assert ''.join((out/'pages'/f'page-{i:02}.txt').read_text(encoding='utf-8')+'\f' for i in range(1,18)) == raw.decode()
    print('PASS: 17 pages, 14 figure captions, exact per-page text round trip; input SHA-256 matches assembly manifest.')
if __name__=='__main__': main()

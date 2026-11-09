from pathlib import Path
import fitz,json
R=Path(__file__).resolve().parents[1]; src=R/'work/report.pdf'; out=R/'output/GOSD_2026_第六章与附录A及致谢_v0.2_评审稿.pdf'
d=fitz.open(src); meta=d.metadata;meta.update(title='2026全球开源发展报告｜第六章、附录A与致谢评审稿 v0.2',author='GOSD编制组',subject='第六章：未来展望与行动建议；附录A：指标体系与数据来源；致谢；动态星座v2.0.0；评审稿，未公开发布');d.set_metadata(meta)
toc=d.get_toc()
for item in toc:
 if '回望' in item[1]:item[0]=2
toc.append([1,'附录 A 指标体系与数据来源',11])
toc.sort(key=lambda x:(x[2],x[0]))
d.set_toc(toc)
d.save(out,garbage=4,deflate=True)
print(json.dumps({'file':str(out),'pages':len(d),'bytes':out.stat().st_size},ensure_ascii=False))

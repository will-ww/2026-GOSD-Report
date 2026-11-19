#!/usr/bin/env python3
"""Validate distribution metadata without opening or modifying external PDFs.

Versions and page counts are cross-checked across the current manifests, not
pinned in this program. A new accepted baseline can therefore advance when its
configs, shared-content evidence, current pointers, and build inputs advance
consistently. This checks recorded evidence, not the truth of an absent PDF.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

SHA256 = re.compile(r"[0-9a-f]{64}\Z")
DISTRIBUTIONS = {"cossi", "community"}
LANGUAGES = {"zh-CN", "en"}
LOGOS = {
    "cossi": ["ccosi", "singularity"],
    "community": ["x-lab", "singularity", "ccosi", "kaiyuanshe"],
}
WINDOW = {"start": "2025-07-01", "end": "2026-06-30"}


def version(value):
    return str(value).removeprefix("v") if value is not None else None


class Review:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.repo = self.root.parents[2]
        self.errors = []
        self.checks = 0
        self.summary = {}

    def require(self, condition, message):
        self.checks += 1
        if not condition:
            self.errors.append(message)
        return bool(condition)

    def path(self, origin, relative, label):
        if not self.require(isinstance(relative, str) and bool(relative), f"{label}: missing relative path"):
            return None
        target = (Path(origin).parent / relative).resolve()
        if not self.require(target.is_relative_to(self.repo), f"{label}: path escapes repository: {relative}"):
            return None
        if not self.require(target.exists(), f"{label}: missing path {relative}"):
            return None
        return target

    def load(self, path):
        try:
            data = json.loads(Path(path).read_text(encoding="utf-8"))
            self.require(isinstance(data, dict), f"{path}: JSON root must be an object")
            return data if isinstance(data, dict) else {}
        except (OSError, TypeError, ValueError) as exc:
            self.require(False, f"{path}: cannot read JSON: {exc}")
            return {}

    def equal(self, left, right, label):
        self.require(left == right, f"{label}: mismatch ({left!r} != {right!r})")

    def hash(self, value, label):
        self.require(isinstance(value, str) and bool(SHA256.fullmatch(value)), f"{label}: invalid SHA-256")

    def planned(self, config, label):
        # Apply only while planned; a properly registered future translation may advance.
        if config.get("translation_status") != "planned":
            return
        self.equal(config.get("editorial_status"), "not_started", f"{label}.editorial_status")
        self.equal(config.get("publication_status"), "not_scheduled", f"{label}.publication_status")
        empty_fields = {
            "artifact_version", "approved_artifact", "physical_pages", "printed_pages",
            "pages", "page_count", "publication_date", "release_date", "completed_on",
            "reviewed_by", "reviewed_on", "public_download_url",
        }
        for key in empty_fields:
            self.require(config.get(key) in (None, [], {}), f"{label}: planned translation must not have {key}")

    def markdown_links(self, paths):
        for path in sorted(set(paths)):
            try:
                text = path.read_text(encoding="utf-8")
            except OSError as exc:
                self.require(False, f"{path}: cannot read Markdown: {exc}")
                continue
            # Inline links/images in project documentation; fenced examples are excluded.
            text = re.sub(r"```.*?```|~~~.*?~~~", "", text, flags=re.S)
            for raw in re.findall(r"!?\[[^\]]*\]\(([^\n)]+)\)", text):
                target = raw.strip().split(' "', 1)[0].strip("<>")
                parsed = urlsplit(target)
                if parsed.scheme or parsed.netloc or not parsed.path:
                    continue
                self.path(path, unquote(parsed.path), f"{path.relative_to(self.repo)} link")

    def forbidden_files(self):
        # Include tracked and untracked prospective source files, excluding gitignored builds.
        proc = subprocess.run(
            ["git", "-C", str(self.repo), "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
            capture_output=True, check=False,
        )
        if proc.returncode:
            self.require(False, "Cannot list repository files with git for PDF/font/archive exclusion")
            return
        forbidden = {".pdf", ".ttf", ".otf", ".ttc", ".woff", ".woff2", ".zip", ".7z", ".rar"}
        for name in set(proc.stdout.decode("utf-8").split("\0")) - {""}:
            path = self.repo / name
            if not path.is_file():
                continue
            self.require(path.suffix.lower() not in forbidden, f"Forbidden repository artifact: {name}")
            try:
                with path.open("rb") as stream:
                    prefix = stream.read(8)
                self.require(not prefix.startswith(b"%PDF-"), f"PDF content disguised by extension: {name}")
            except OSError as exc:
                self.require(False, f"Cannot inspect {name}: {exc}")

    def source_revision(self, reg_path, reg, current_path, current, content_path, content):
        pointer = reg.get('current_source_revision')
        if not pointer and not current.get('current_source_revision'):
            return
        pointer = pointer or {}
        revision_path = self.path(reg_path, pointer.get('manifest'), 'active source revision')
        other = current.get('current_source_revision', {})
        self.equal(self.path(current_path, other.get('manifest'), 'current source pointer'), revision_path, 'source pointer target')
        if not revision_path:
            return
        revision = self.load(revision_path)
        for key in ['content_id', 'status']:
            self.equal(pointer.get(key), revision.get(key), f'source revision {key}')
            self.equal(other.get(key), revision.get(key), f'current source revision {key}')
        self.require(revision.get('content_id') != content.get('content_id'), 'Source revision must have a new content ID')
        self.equal(revision.get('previous_content_id'), content.get('content_id'), 'source parent content ID')
        self.equal(self.path(revision_path, revision.get('previous_content_manifest'), 'source parent'), content_path, 'source parent manifest')
        self.equal(revision.get('main_window'), WINDOW, 'source revision main period')
        self.equal(revision.get('status'), 'source_revision_pending_layout', 'source revision status')
        self.equal(revision.get('approved_artifact'), None, 'Unrendered source has no accepted PDF')
        self.equal(set(revision.get('synchronization', {})), {'cossi_zh-CN', 'cossi_en', 'community_zh-CN', 'community_en'}, 'source synchronization scope')
        self.equal(revision.get('synchronization', {}).get('community_en'), 'planned', 'Community English source status')
        self.path(revision_path, revision.get('build_entry'), 'source preparation entry')
        self.path(revision_path, revision.get('review'), 'source review')
        self.summary['current_source_revision'] = revision.get('content_id')

    def repository_markdown(self):
        # Local build outputs may contain historical links; validate repository sources only.
        paths = subprocess.check_output(
            ['git', '-C', str(self.repo), 'ls-files', '--cached', '--others',
             '--exclude-standard', '-z', '--', self.root.relative_to(self.repo).as_posix()]
        ).decode('utf-8').split('\0')
        return [self.repo / p for p in paths if p.endswith('.md')]

    def run(self):
        """Schema 2 allows independently accepted languages and frozen editions."""
        reg_path=self.root/'registry.json'
        reg=self.load(reg_path)
        if reg.get('schema_version')==1:
            return self.run_schema1()
        self.equal(reg.get('schema_version'),2,'registry schema')
        self.equal(reg.get('main_window'),WINDOW,'main period')
        self.equal(reg.get('outputs',{}).get('pdf',{}).get('in_repository'),False,'PDF exclusion')
        current_path=self.root.parent/'current.json'
        current=self.load(current_path)
        self.equal(current.get('main_window'),WINDOW,'current main period')
        self.equal(current.get('pdf_in_repository'),False,'current PDF exclusion')
        self.equal(self.path(current_path,current.get('distribution_registry'),'registry pointer'),reg_path,'registry target')
        for origin,data in [(reg_path,reg),(current_path,current)]:
            self.path(origin,data.get('review'),'current approval')
        content_path=self.path(reg_path,reg.get('shared_content_manifest'),'current shared content')
        content=self.load(content_path) if content_path else {}
        self.equal(content.get('content_id'),reg.get('shared_content_id'),'current content ID')
        self.equal(content.get('main_window'),WINDOW,'shared main period')
        self.source_revision(reg_path, reg, current_path, current, content_path, content)
        historical_path=self.path(reg_path,reg.get('historical_common_body_manifest'),'historical body manifest')
        historical=self.load(historical_path) if historical_path else {}
        self.equal(historical.get('content_id'),'gosd-2026-essential-body-v1.4','frozen historical content')
        detail_path=self.path(historical_path,historical.get('equality_verification',{}).get('detail'),'historic equivalence') if historical_path else None
        detail=self.load(detail_path) if detail_path else {}
        self.equal(len(detail.get('body',[])),historical.get('body_pages'),'historic body count')
        for i,row in enumerate(detail.get('body',[])):
            self.equal(row.get('printed_page'),i+1,'historic body sequence')
            for key in ['text_identical','content_stream_bytes_identical','raster36dpi_identical']:
                self.equal(row.get(key),True,f'historic row {i+1}: {key}')
            self.hash(row.get('raster_sha256'),'historic raster identity')
        shared_path=self.path(content_path,content.get('shared_annual_changes'),'shared annual changes') if content_path else None
        shared=self.load(shared_path) if shared_path else {}
        self.equal(shared.get('status'),'author_approved','annual changes approval')
        self.equal(shared.get('content_id'),content.get('content_id'),'annual content ID')
        self.equal(shared.get('main_window'),WINDOW,'annual main period')
        self.path(shared_path,shared.get('review'),'annual approval')
        data_path=self.path(shared_path,shared.get('shared_data'),'single numeric source')
        if data_path:
            import hashlib
            self.equal(hashlib.sha256(data_path.read_bytes()).hexdigest(),shared.get('shared_data_sha256'),'shared data fingerprint')
        entries=reg.get('distributions',[])
        self.equal({x.get('id') for x in entries},DISTRIBUTIONS,'edition identities')
        self.equal(len(entries),2,'edition count')
        configs={}
        naming=reg.get('naming',{})
        self.equal(naming.get('institution_abbreviation'),'CCOSI','institution name')
        self.equal(naming.get('distribution_label'),'COSSI','edition label')
        for entry in entries:
            did=entry.get('id')
            self.equal(set(entry.get('languages',{})),LANGUAGES,f'{did} languages')
            for lang,ref in entry.get('languages',{}).items():
                path=self.path(reg_path,ref.get('config'),f'{did}/{lang} config')
                if not path:continue
                cfg=self.load(path);configs[did,lang]=(path,cfg)
                for key,expected in [('distribution_id',did),('language',lang),('content_scope','essential'),('report_year',2026),('institution_abbreviation','CCOSI'),('pdf_in_repository',False),('logo_order',LOGOS[did]),('display_name',entry.get('display_name'))]:
                    self.equal(cfg.get(key),expected,f'{did}/{lang}.{key}')
                self.require(not cfg.get('publication_date') or cfg.get('publication_status')!='not_scheduled',f'{did}/{lang} publication date/state')
                if ref.get('status')=='planned':
                    self.equal(cfg.get('translation_status'),'planned',f'{did}/{lang} planned')
                    self.planned(cfg,f'{did}/{lang}')
                    continue
                self.equal(ref.get('status'),'accepted_baseline',f'{did}/{lang} registered state')
                self.equal(cfg.get('editorial_status'),'accepted_baseline',f'{did}/{lang} editorial state')
                if lang=='en':
                    self.equal(cfg.get('translation_status'),'accepted_baseline',f'{did}/{lang} translation state')
                    self.require(bool(cfg.get('reviewed_on') and cfg.get('reviewed_by')),'English approval identity')
                artifact=cfg.get('approved_artifact') or {}
                self.hash(artifact.get('sha256'),f'{did}/{lang} approved PDF')
                self.equal(artifact.get('in_repository'),False,f'{did}/{lang} binary exclusion')
                total=artifact.get('pages')
                self.require(isinstance(total,int) and total>0,f'{did}/{lang} page count')
                self.require(isinstance(artifact.get('bytes'),int) and artifact['bytes']>0,f'{did}/{lang} bytes')
                for key in ['source_filename','export_filename']:
                    self.require(str(artifact.get(key,'')).endswith(f"_v{cfg.get('artifact_version')}.pdf"),f'{did}/{lang} filename/version')
                pages=cfg.get('physical_pages') or {}
                self.equal(pages.get('back_cover'),total,f'{did}/{lang} last page')
                for k,val in pages.items():
                    vals=val if isinstance(val,list) else [val]
                    self.require(all(isinstance(x,int) and 1<=x<=total for x in vals),f'{did}/{lang}.{k} page range')
                build=cfg.get('build',{})
                self.path(path,build.get('entry'),f'{did}/{lang} build source')
                self.path(path,build.get('source_content'),f'{did}/{lang} build content')
                pointers=[p for p in current.get('current_full_prints',{}).values() if p.get('language')==lang and (current_path.parent/p.get('config','')).resolve()==path]
                self.equal(len(pointers),1,f'{did}/{lang} current pointer')
                if pointers:
                    self.equal(pointers[0].get('version'),cfg.get('artifact_version'),f'{did}/{lang} current version')
                    self.equal(pointers[0].get('pages'),total,f'{did}/{lang} current pages')
                if did=='cossi':
                    self.equal(cfg.get('content_id'),content.get('content_id'),f'{lang} current content')
                    layout=content.get('language_layouts',{}).get(lang,{})
                    self.equal(layout.get('artifact'),artifact,f'{lang} shared artifact')
                    self.equal(shared.get('approved_full_artifacts',{}).get(lang),artifact,f'{lang} increment artifact')
                    part=shared.get('languages',{}).get(lang,{})
                    self.equal(part.get('full_version'),cfg.get('artifact_version'),f'{lang} increment version')
                    self.equal(part.get('full_pages'),total,f'{lang} increment page count')
                    self.equal(part.get('physical_pages'),pages.get('annual_changes'),f'{lang} insert location')
                    self.path(shared_path,part.get('content'),f'{lang} editable prose')
                    self.path(shared_path,part.get('integration'),f'{lang} assembly source')
                    lo,hi=layout.get('body_printed_range',[0,0])
                    self.equal(pages.get('body_end',0)-pages.get('body_start',0)+1,hi-lo+1,f'{lang} body length')
                else:
                    old=historical.get('approved_pdf_sources',{}).get(did,{})
                    self.equal(artifact.get('sha256'),old.get('sha256'),'frozen Community PDF')
                    self.equal(cfg.get('content_id'),historical.get('content_id'),'frozen Community content')
                self.summary[f'{did}/{lang}']={'version':cfg.get('artifact_version'),'pages':total}
        for did in DISTRIBUTIONS:
            zh=configs.get((did,'zh-CN'))
            en=configs.get((did,'en'))
            if zh and en:
                self.equal(self.path(en[0],en[1].get('source_distribution_config'),f'{did} translation source'),zh[0],f'{did} source config')
                self.equal(en[1].get('source_content_id'),zh[1].get('content_id'),f'{did} source content ID')
                self.summary[did]={'version':zh[1].get('artifact_version'),'pages':zh[1].get('approved_artifact',{}).get('pages'),'language':'zh-CN','english_status':en[1].get('translation_status')}
        self.summary['shared_body_pages']='language-specific pagination; historical 118-page identity retained'
        self.markdown_links(self.repository_markdown()+[self.root.parent/'README.md'])
        self.forbidden_files()
        return {'ok':not self.errors,'checks':self.checks,'summary':self.summary,'errors':self.errors,
                'scope':'Current bilingual metadata and immutable historical records; external PDFs are validated by the separate build/verification route.'}

    def run_schema1(self):
        reg_path = self.root / "registry.json"
        reg = self.load(reg_path)
        current_path = self.root.parent / "current.json"
        current = self.load(current_path)
        baseline_path = self.path(reg_path, reg.get("shared_content_manifest"), "shared_content_manifest")
        base = self.load(baseline_path) if baseline_path else {}
        detail_path = self.path(baseline_path, base.get("equality_verification", {}).get("detail"), "equality detail") if baseline_path else None
        detail = self.load(detail_path) if detail_path else {}
        terms = self.load(self.root / "shared/terminology.json")
        inputs_path = self.root / "shared/source/input-materials.json"
        inputs = self.load(inputs_path)
        self.equal(reg.get("worktree_edition_id"), "insights", "registry worktree edition")
        self.equal(current.get("edition_id"), "insights", "current edition_id")
        self.equal(reg.get("content_scope"), "essential", "content scope")
        self.equal(base.get("content_scope"), reg.get("content_scope"), "shared content scope")
        self.equal(base.get("source_language"), "zh-CN", "shared source language")
        content_id = reg.get("shared_content_id")
        self.require(isinstance(content_id, str) and bool(content_id), "shared_content_id is required")
        self.equal(base.get("content_id"), content_id, "shared content ID")
        for label, data in [("registry", reg), ("shared", base), ("current", current)]:
            self.equal(data.get("main_window"), WINDOW, f"{label} main statistical window")
        self.equal(current.get("pdf_in_repository"), False, "current PDF exclusion")
        self.equal(reg.get("outputs", {}).get("pdf", {}).get("in_repository"), False, "registry PDF exclusion")
        self.equal(self.path(current_path, current.get("distribution_registry"), "current distribution registry"), reg_path, "current registry target")
        for origin, value in [(reg_path, reg.get("review")), (current_path, current.get("review"))]:
            self.path(origin, value, "current review")
        if baseline_path:
            self.path(baseline_path, base.get("source_archive", {}).get("path"), "historical source archive")

        naming = reg.get("naming", {})
        self.equal(naming.get("distribution_id"), "cossi", "naming distribution_id")
        self.equal(naming.get("distribution_label"), "COSSI", "COSSI publication label")
        self.equal(naming.get("institution_abbreviation"), "CCOSI", "CCOSI institution abbreviation")
        entries = reg.get("distributions", [])
        self.require(isinstance(entries, list), "distributions must be a list")
        entries = entries if isinstance(entries, list) else []
        self.equal([e.get("id") for e in entries if isinstance(e, dict)].count("cossi"), 1, "COSSI entry count")
        self.equal([e.get("id") for e in entries if isinstance(e, dict)].count("community"), 1, "Community entry count")
        self.equal({e.get("id") for e in entries if isinstance(e, dict)}, DISTRIBUTIONS, "distribution axis")
        configs, config_paths = {}, {}
        for entry in entries:
            if not isinstance(entry, dict):
                self.require(False, "Distribution entry must be an object")
                continue
            did = entry.get("id")
            languages = entry.get("languages", {})
            self.equal(set(languages), LANGUAGES, f"{did} language axis")
            for lang, reference in languages.items():
                path = self.path(reg_path, reference.get("config"), f"{did}/{lang} config")
                if not path:
                    continue
                cfg = self.load(path)
                configs[(did, lang)], config_paths[(did, lang)] = cfg, path
                for key, expected in [("distribution_id", did), ("language", lang), ("content_scope", reg.get("content_scope")), ("report_year", reg.get("report_year")), ("institution_abbreviation", naming.get("institution_abbreviation")), ("pdf_in_repository", False)]:
                    self.equal(cfg.get(key), expected, f"{did}/{lang}.{key}")
                self.equal(cfg.get("display_name"), entry.get("display_name"), f"{did}/{lang}.display_name")
                self.equal(cfg.get("logo_order"), LOGOS.get(did), f"{did}/{lang}.logo_order")
                if lang == "zh-CN":
                    self.equal(cfg.get("content_id"), content_id, f"{did} source content ID")
                    self.equal(reference.get("status"), cfg.get("editorial_status"), f"{did} editorial status")
                    self.equal(cfg.get("editorial_status"), "accepted_baseline", f"{did} current accepted baseline")
                else:
                    self.equal(reference.get("status"), cfg.get("translation_status"), f"{did}/en translation status")
                    self.require(cfg.get("translation_status") in {"planned", "translating", "editorial_review", "accepted_baseline"}, f"{did}/en: unknown translation status")
                    self.equal(cfg.get("source_content_id"), content_id, f"{did}/en source content ID")
                    self.equal(cfg.get("source_language"), base.get("source_language"), f"{did}/en source language")
                    self.path(path, cfg.get("source_distribution_config"), f"{did}/en Chinese source config")
                    self.planned(cfg, f"{did}/en")
        self.equal(len(configs), len(DISTRIBUTIONS) * len(LANGUAGES), "configuration count")

        count = base.get("body_pages")
        printed = base.get("printed_page_range", [])
        valid_count = isinstance(count, int) and not isinstance(count, bool) and count > 0
        self.require(valid_count, "shared body_pages must be a positive integer")
        self.require(isinstance(printed, list) and len(printed) == 2 and all(isinstance(x, int) for x in printed), "printed page range must contain two integers")
        valid_range = isinstance(printed, list) and len(printed) == 2 and all(isinstance(x, int) for x in printed)
        if valid_range and valid_count:
            self.equal(printed[1] - printed[0] + 1, count, "printed range/body page count")
        self.equal(inputs.get("body_printed_range"), printed, "builder printed range")
        self.equal(set(base.get("approved_pdf_sources", {})), DISTRIBUTIONS, "shared approved source distributions")
        self.equal(set(inputs.get("approved_artifacts", {})), DISTRIBUTIONS, "builder approved source distributions")
        physical_ranges = {}
        for did in sorted(DISTRIBUTIONS):
            cfg = configs.get((did, "zh-CN"), {})
            path = config_paths.get((did, "zh-CN"))
            en = configs.get((did, "en"), {})
            en_path = config_paths.get((did, "en"))
            artifact = cfg.get("approved_artifact") or {}
            source = base.get("approved_pdf_sources", {}).get(did, {})
            build_input = inputs.get("approved_artifacts", {}).get(did, {})
            pointer = current.get("current_full_prints", {}).get(did, {})
            self.equal(version(cfg.get("artifact_version")), version(source.get("version")), f"{did} config/shared version")
            self.equal(version(cfg.get("artifact_version")), version(build_input.get("version")), f"{did} config/builder version")
            self.equal(version(cfg.get("artifact_version")), version(pointer.get("version")), f"{did} config/current version")
            self.require(cfg.get("artifact_version") is not None, f"{did} accepted Chinese artifact version required")
            for field in ["source_filename", "export_filename"]:
                filename = artifact.get(field)
                suffix = f"_v{version(cfg.get('artifact_version'))}.pdf"
                self.require(isinstance(filename, str) and filename.endswith(suffix), f"{did} {field}: filename/version mismatch")
            for other, label in [(source, "shared"), (build_input, "builder")]:
                self.equal(artifact.get("sha256"), other.get("sha256"), f"{did} config/{label} PDF SHA")
            self.hash(artifact.get("sha256"), f"{did} approved PDF")
            self.equal(artifact.get("source_filename"), source.get("filename"), f"{did} approved source filename")
            self.equal(artifact.get("pages"), build_input.get("pages"), f"{did} config/builder total pages")
            self.equal(artifact.get("pages"), pointer.get("pages"), f"{did} config/current total pages")
            self.equal(build_input.get("language"), cfg.get("language"), f"{did} builder language")
            self.equal(pointer.get("language"), cfg.get("language"), f"{did} current language")
            self.equal(artifact.get("in_repository"), False, f"{did} approved PDF exclusion")
            self.require(isinstance(artifact.get("bytes"), int) and artifact["bytes"] > 0, f"{did} artifact byte size required")
            pages = cfg.get("physical_pages") or {}
            total = artifact.get("pages")
            self.require(isinstance(total, int) and total > 0, f"{did} total pages must be a positive integer")
            self.equal(pages.get("back_cover"), total, f"{did} last physical page")
            self.equal(source.get("physical_range"), [pages.get("body_start"), pages.get("body_end")], f"{did} source physical range")
            physical_ranges[did] = source.get("physical_range", [])
            if valid_count and all(isinstance(pages.get(k), int) for k in ["body_start", "body_end", "inside_back_cover", "back_cover"]):
                self.equal(pages["body_end"] - pages["body_start"] + 1, count, f"{did} physical body length")
                self.equal(pages["inside_back_cover"], pages["body_end"] + 1, f"{did} inside back cover")
                self.equal(pages["back_cover"], pages["inside_back_cover"] + 1, f"{did} back cover")
            for key, value in pages.items():
                values = value if isinstance(value, list) else [value]
                self.require(all(isinstance(v, int) and 1 <= v <= total for v in values) if isinstance(total, int) else False, f"{did}.{key}: invalid physical page")
            if path:
                self.equal(self.path(current_path, pointer.get("config"), f"{did} current config"), path, f"{did} current config target")
                build = cfg.get("build", {})
                self.path(path, build.get("entry"), f"{did} builder entry")
                self.equal(self.path(path, build.get("source_content"), f"{did} builder content"), baseline_path, f"{did} builder content target")
                fm = build.get("frontmatter", "")
                if fm.startswith("."):
                    self.path(path, fm, f"{did} frontmatter source")
            if en_path:
                self.equal(self.path(en_path, en.get("source_distribution_config"), f"{did}/en source config"), path, f"{did}/en mapped Chinese config")
                self.equal(en.get("logo_order"), cfg.get("logo_order"), f"{did} language logo consistency")
            self.summary[did] = {"version": cfg.get("artifact_version"), "pages": total, "language": cfg.get("language"), "english_status": en.get("translation_status")}
        community = configs.get(("community", "zh-CN"), {}).get("approved_artifact") or {}
        builder_base = inputs.get("community_baseline", {})
        for key, source_key in [("filename", "source_filename"), ("sha256", "sha256"), ("page_count", "pages")]:
            self.equal(builder_base.get(key), community.get(source_key), f"builder community_baseline.{key}")

        rows = detail.get("body", [])
        self.require(isinstance(rows, list), "body equivalence detail must be a list")
        rows = rows if isinstance(rows, list) else []
        self.equal(len(rows), count, "body equivalence row count")
        equality = base.get("equality_verification", {})
        for key in ["text_pages", "content_stream_pages", "raster_pages"]:
            self.equal(equality.get(key), count, f"equality summary {key}")
        dpi = equality.get("raster_dpi")
        self.require(isinstance(dpi, (int, float)) and dpi > 0, "equality raster DPI required")
        raster_key = f"raster{dpi:g}dpi_identical" if isinstance(dpi, (int, float)) else "raster_invalid"
        expected_printed = list(range(printed[0], printed[1] + 1)) if valid_range else []
        self.equal([row.get("printed_page") for row in rows], expected_printed, "complete ordered printed page mapping")
        for index, row in enumerate(rows):
            for key in ["text_identical", "content_stream_bytes_identical", raster_key]:
                self.require(row.get(key) is True, f"body row {index + 1}: {key} must be true")
            self.hash(row.get("raster_sha256"), f"body row {index + 1} raster")
            for did, page_range in physical_ranges.items():
                if len(page_range) == 2 and isinstance(page_range[0], int):
                    self.equal(row.get(f"{did}_physical"), page_range[0] + index, f"body row {index + 1} {did} mapping")
        trailing = detail.get("trailing_pages", [])
        self.equal(len(trailing), 2, "inside/back cover verification count")
        for index, row in enumerate(trailing):
            for key in ["text_identical", raster_key]:
                self.require(row.get(key) is True, f"trailing row {index + 1}: {key} must be true")
            for did in DISTRIBUTIONS:
                pages = configs.get((did, "zh-CN"), {}).get("physical_pages") or {}
                self.equal(row.get(f"{did}_physical"), pages.get(["inside_back_cover", "back_cover"][index]) if index < 2 else None, f"trailing row {index + 1} {did} mapping")
        self.summary["shared_body_pages"] = count

        term_map = {t.get("id"): t for t in terms.get("terms", [])}
        self.equal(term_map.get("CCOSI", {}).get("en"), naming.get("institution_name_en"), "English institution name")
        self.equal(term_map.get("CCOSI", {}).get("zh"), naming.get("institution_name_zh"), "Chinese institution name")
        for did in DISTRIBUTIONS:
            cfg = configs.get((did, "zh-CN"), {})
            for lang in ["zh", "en"]:
                self.equal(term_map.get(f"{did}_edition", {}).get(lang), cfg.get("display_name", {}).get(lang), f"{did} {lang} naming/terminology")
        markdown = self.repository_markdown() + [self.root.parent / "README.md"]
        review_path = self.path(reg_path, reg.get("review"), "review documentation")
        if review_path:
            markdown.append(review_path)
        self.markdown_links(markdown)
        self.forbidden_files()
        return {"ok": not self.errors, "checks": self.checks, "summary": self.summary, "errors": self.errors,
                "scope": "Registry and recorded evidence consistency only; external PDFs are not opened or revalidated."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent, help="Distribution registry directory")
    parser.add_argument("--json", action="store_true", help="Print the full machine-readable result")
    args = parser.parse_args()
    result = Review(args.root).run()
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"Distribution registry: {'PASS' if result['ok'] else 'FAIL'} ({result['checks']} checks)")
        for did in sorted(DISTRIBUTIONS):
            item = result["summary"].get(did, {})
            print(f"  {did}: {item.get('language')} v{item.get('version')} / {item.get('pages')} pages; en={item.get('english_status')}")
        print(f"  shared body: {result['summary'].get('shared_body_pages')} pages")
        for error in result["errors"]:
            print(f"  ERROR: {error}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())

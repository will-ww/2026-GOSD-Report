PYTHON ?= python3
.PHONY: all fonts sources figures revised-figures pdf qa clean
all: pdf
fonts:
	$(PYTHON) configure_fonts.py
sources:
	$(PYTHON) scripts/build_chapter.py
	$(PYTHON) scripts/sync_markdown.py
figures:
	$(PYTHON) scripts/export_vector_assets.py
revised-figures:
	$(PYTHON) scripts/draw_chapter_revision.py
pdf: fonts sources
	xelatex -interaction=nonstopmode -halt-on-error chapter2.tex
	xelatex -interaction=nonstopmode -halt-on-error chapter2.tex
qa:
	$(PYTHON) scripts/render_qa.py
	$(PYTHON) scripts/audit_chapter.py
clean:
	rm -f chapter2.aux chapter2.log chapter2.out chapter2.toc

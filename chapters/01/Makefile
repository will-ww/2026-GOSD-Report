.PHONY: all figures pdf clean
all: pdf
figures:
	python draw_report_figures.py
	python draw_chapter_figures.py
	python draw_sdgs_dpga.py
pdf: figures
	xelatex -interaction=nonstopmode -halt-on-error chapter1.tex
	xelatex -interaction=nonstopmode -halt-on-error chapter1.tex
	xelatex -interaction=nonstopmode -halt-on-error chapter1.tex
clean:
	rm -f chapter1.aux chapter1.log chapter1.out chapter1.toc chapter1.pdf

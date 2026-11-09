#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p work/.texcache/{var,config,cache} output
python3 configure_fonts.py
export TEXMFVAR="$PWD/work/.texcache/var" TEXMFCONFIG="$PWD/work/.texcache/config" XDG_CACHE_HOME="$PWD/work/.texcache/cache"
export TEXMF=/usr/share/texlive/texmf-dist TEXMFDBS="$TEXMFVAR"
export TEXINPUTS=.:/usr/share/texlive/texmf-dist/tex//:
export OPENTYPEFONTS=/usr/share/fonts//:/usr/share/texmf/fonts//:/usr/share/texlive/texmf-dist/fonts//:
export TTFONTS="$OPENTYPEFONTS" TFMFONTS=/usr/share/texmf/fonts//:/usr/share/texlive/texmf-dist/fonts//:
export ENCFONTS="$TFMFONTS" TEXFONTMAPS="$TFMFONTS" TEXFORMATS="$PWD/work/.texcache:"
if [[ ! -f work/.texcache/xelatex.fmt ]]; then (cd work/.texcache && xetex -ini -etex -jobname=xelatex -progname=xelatex xelatex.ini > format.log); fi
(cd atlas && xelatex -interaction=nonstopmode -halt-on-error atlas.tex > build.log)
for pass in 1 2 3; do xelatex -interaction=nonstopmode -halt-on-error -output-directory=work report.tex > "work/pass${pass}.log"; done
cp work/report.pdf output/GOSD_2026_第三章_清洁整理_v0.1_评审稿.pdf

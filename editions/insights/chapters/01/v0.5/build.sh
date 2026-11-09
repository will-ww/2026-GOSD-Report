#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p output
python3 prepare_assets.py
python3 build_figures.py
python3 build_infographics.py
python3 build_readability.py
# Standard TeX Live installations need no configuration. The following fallback
# supports a runtime that has TeX packages but lacks its filename/format index.
if ! kpsewhich article.cls >/dev/null 2>&1; then
  export TEXMF='{/usr/share/texmf,/usr/share/texlive/texmf-dist}'
fi
if ! kpsewhich xelatex.fmt >/dev/null 2>&1; then
  mkdir -p .build/texmf-var
  export TEXMFVAR="$PWD/.build/texmf-var"
  export TEXFORMATS="$PWD/.build/texmf-var"
  if [ ! -f "$TEXFORMATS/xelatex.fmt" ]; then
    xelatex -ini -etex -interaction=nonstopmode -jobname=xelatex -output-directory="$TEXFORMATS" '\input xelatex.ini' >output/format-build.txt 2>&1
  fi
fi
for pass in 1 2; do
  xelatex -interaction=nonstopmode -halt-on-error -output-directory=output -jobname=GOSD_2026_Insights_Chapter1_Review_v0.5 chapter1.tex >output/build-pass-${pass}.txt 2>&1
done

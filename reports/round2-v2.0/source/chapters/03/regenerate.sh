#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python3 scripts/prepare_chapter.py
python3 scripts/prepare_atlas.py
python3 scripts/compact_project_pages.py
python3 scripts/draw_brand.py
python3 scripts/align_vector_palette.py
python3 scripts/redraw_rank_matrices.py
python3 scripts/redraw_emerging_boards.py
bash build.sh
python3 scripts/check_render.py
python3 scripts/final_verify.py

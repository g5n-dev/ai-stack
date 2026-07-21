#!/bin/bash

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

if [ -d "venv" ]; then
  # shellcheck disable=SC1091
  source venv/bin/activate
fi

SKIP_BUILD=0
SERVE=0
GENERATOR_ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --skip-build)
      SKIP_BUILD=1
      shift
      ;;
    --serve)
      SERVE=1
      shift
      ;;
    *)
      GENERATOR_ARGS+=("$1")
      shift
      ;;
  esac
done

python3 scripts/preflight.py
if [[ ${#GENERATOR_ARGS[@]} -gt 0 ]]; then
  python3 scripts/generate_content.py "${GENERATOR_ARGS[@]}"
else
  python3 scripts/generate_content.py
fi

python3 scripts/build_lineage.py \
  --content-root blog/content \
  --internal-output data/lineage \
  --public-output blog/static/data/lineage \
  --apply-post-metadata
python3 scripts/verify_lineage.py \
  --public-root blog/static/data/lineage \
  --internal-root data/lineage \
  --verify-hashes
python3 scripts/build_content_quality_manifest.py \
  --content-root blog/content \
  --output blog/data/content_quality.json \
  --fail-on-quarantine \
  --fail-on-structural-warning \
  --fail-on-unverified-provenance
python3 scripts/build_stack_trends.py \
  --content-root blog/content \
  --quality-manifest blog/data/content_quality.json \
  --output blog/static/data/stack-trends
python3 scripts/verify_stack_trends.py \
  --root blog/static/data/stack-trends \
  --verify-hashes
TAG_GRAPH_ENABLE_CONTENT_MINING=0 \
TAG_INTRO_ENABLED=0 \
TAG_INTRO_MAX_NEW=0 \
  python3 -m processor.tag_graph
python3 scripts/verify_graph.py --assets-only --public-dir blog/static

if [[ "$SKIP_BUILD" -eq 0 ]]; then
  python3 scripts/preflight.py --require-hugo
  (
    cd blog
    hugo --minify --cleanDestinationDir
  )
fi

if [[ "$SERVE" -eq 1 ]]; then
  python3 scripts/preflight.py --require-hugo
  (
    cd blog
    hugo server -D
  )
fi

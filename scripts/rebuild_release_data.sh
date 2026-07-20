#!/usr/bin/env bash
# 在无网络、无密钥环境中按依赖顺序重建所有 Post 派生发布数据。
set -euo pipefail

export PYTHONPATH="${PYTHONPATH:-$(pwd)}"

# Historical repairs are deliberately offline at release time.  A release may
# consume previously captured evidence, but it must never mutate or re-fetch
# historical Posts while producing deterministic derived assets.
python3 scripts/repair_historical_content.py --check

# PR1 兼容尚无 lineage 的 main；第二门加入配置后即 fail-closed 强制。
if [[ -f config/lineage.yaml ]]; then
  test -f scripts/build_lineage.py
  # Public routes drive the interactive lookup, while Post front matter drives
  # canonical/noindex.  Apply both at the same deterministic release fixed point
  # so representative deletion or a newly discovered earlier source cannot
  # leave stale SEO lineage metadata behind.
  python3 scripts/build_lineage.py --apply-post-metadata
  python3 scripts/verify_lineage.py --verify-hashes
fi

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
python3 scripts/release_marker.py prune-product \
  --root blog/static/data/tag-graph
python3 scripts/verify_graph.py --assets-only --public-dir blog/static

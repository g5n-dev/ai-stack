#!/usr/bin/env bash

# Local production-boundary preflight. The only authoritative deployment path
# remains .github/workflows/deploy.yml on main.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
PYTHON_BIN="${PYTHON_BIN:-python3}"
SITE_BASE_URL="${SITE_BASE_URL:-https://ai-stack.site/}"
TMP_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/ai-stack-release.XXXXXX")"

cleanup() {
  rm -rf "$TMP_ROOT"
}
trap cleanup EXIT

cd "$PROJECT_ROOT"

if ! command -v hugo >/dev/null 2>&1; then
  echo "缺少 Hugo 0.153.4；请先按 DEPLOYMENT.md 安装。" >&2
  exit 2
fi
HUGO_VERSION_OUTPUT="$(hugo version)"
if [[ "$HUGO_VERSION_OUTPUT" != *"v0.153.4+extended"* ]]; then
  echo "Hugo 版本不匹配：需要 v0.153.4+extended，当前为 ${HUGO_VERSION_OUTPUT}。" >&2
  exit 2
fi
if [[ ! -x node_modules/.bin/pagefind || ! -x node_modules/.bin/tailwindcss ]]; then
  echo "缺少锁定的前端依赖；请先运行 npm ci --ignore-scripts。" >&2
  exit 2
fi

echo "[1/7] 校验内容来源与历史修复固定点"
"$PYTHON_BIN" scripts/build_content_quality_manifest.py \
  --content-root blog/content \
  --output "$TMP_ROOT/content_quality.json" \
  --fail-on-quarantine \
  --fail-on-structural-warning \
  --fail-on-unverified-provenance
cmp --silent blog/data/content_quality.json "$TMP_ROOT/content_quality.json"
"$PYTHON_BIN" scripts/repair_historical_content.py --check

echo "[2/7] 校验分层知识图谱资产"
"$PYTHON_BIN" scripts/verify_graph.py --assets-only --public-dir blog/static

echo "[3/7] 从已审核内容重建并比对趋势快照"
"$PYTHON_BIN" scripts/build_stack_trends.py \
  --content-root blog/content \
  --quality-manifest blog/data/content_quality.json \
  --output "$TMP_ROOT/stack-trends"
"$PYTHON_BIN" scripts/verify_stack_trends.py \
  --root "$TMP_ROOT/stack-trends" \
  --verify-hashes
diff -qr blog/static/data/stack-trends "$TMP_ROOT/stack-trends"

echo "[4/7] 重建并比对静态样式"
npm run build:css
git diff --exit-code -- blog/static/css/tailwind.css

echo "[5/7] 运行前端交付测试"
npm test

echo "[6/7] 以生产 baseURL 构建 Hugo"
PUBLIC_DIR="$TMP_ROOT/public"
(
  cd blog
  hugo --baseURL "$SITE_BASE_URL" --minify --cleanDestinationDir --destination "$PUBLIC_DIR"
)

echo "[7/7] 构建 Pagefind 并核对目录"
./node_modules/.bin/pagefind --site "$PUBLIC_DIR"
"$PYTHON_BIN" -m ai_stack.pagefind_catalog --public-root "$PUBLIC_DIR"
test -s "$PUBLIC_DIR/pagefind/pagefind.js"
test -s "$PUBLIC_DIR/pagefind/catalog.json"
test -s "$PUBLIC_DIR/pagefind/catalog.manifest.json"

echo "本地发布边界全部通过。实际部署仅由 main 上的 Build and Deploy 工作流执行。"

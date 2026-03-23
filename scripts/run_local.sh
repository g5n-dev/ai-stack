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

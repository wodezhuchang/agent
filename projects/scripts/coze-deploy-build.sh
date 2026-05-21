#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

cd "$PROJECT_DIR"

# uv 安装依赖
if [ -n "$PIP_TARGET" ]; then
  echo "[deploy] Installing to PIP_TARGET=$PIP_TARGET"
  uv export --frozen --no-hashes --no-dev | uv pip install --no-cache --target "$PIP_TARGET" -r -
else
  echo "[deploy] Installing to .venv"
  if [ -f "uv.lock" ]; then
    uv sync --frozen || uv sync
  else
    uv sync
  fi
fi

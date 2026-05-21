#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_DIR"

# 激活虚拟环境
if [ -f "${PROJECT_DIR}/.venv/bin/activate" ]; then
  source "${PROJECT_DIR}/.venv/bin/activate"
fi

# 安装依赖（如果需要）
if [ -f "pyproject.toml" ]; then
  if [ -n "${PIP_TARGET:-}" ]; then
    uv export --frozen --no-hashes --no-dev | uv pip install --no-cache --target "$PIP_TARGET" -r - 2>/dev/null || true
  elif [ -f ".venv/.uv_ready" ] || [ -d ".venv" ]; then
    uv sync --frozen 2>/dev/null || uv sync 2>/dev/null || true
  fi
fi

#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_DIR"

export PORT=5000

# 清理 5000 端口残留进程
fuser -k 5000/tcp 2>/dev/null || true
sleep 1

# 激活虚拟环境
if [ -f "${PROJECT_DIR}/.venv/bin/activate" ]; then
  source "${PROJECT_DIR}/.venv/bin/activate"
fi

exec python src/main.py -m http -p 5000

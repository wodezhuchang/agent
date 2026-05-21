#!/bin/bash

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

PORT=5000

# 激活虚拟环境
if [ -f "${PROJECT_DIR}/.venv/bin/activate" ]; then
  source "${PROJECT_DIR}/.venv/bin/activate"
fi

cd "$PROJECT_DIR"
python src/main.py -m http -p $PORT

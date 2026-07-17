#!/usr/bin/env bash
# 改编版渲染脚本（中文环境）
# 用法： bash scripts/render_all.sh lesson.json "$OUTPUT_DIR"
set -euo pipefail

json="$(cygpath -w "${1}" 2>/dev/null || echo "${1}")"
outdir="$(cygpath -w "${2}" 2>/dev/null || echo "${2}")"
PY="${KB_PYTHON:-C:/Users/红红/.workbuddy/binaries/python/envs/default/Scripts/python.exe}"

# 用 cygpath 把脚本路径解析为原生 Windows 路径，避免 MSYS 把 C:/ 拼成 /c/ 再被 cwd _drive 污染
if command -v cygpath >/dev/null 2>&1; then
  here="$(cygpath -w "$0" 2>/dev/null)"
  here="$(dirname "$here")"
else
  here="$(cd "$(dirname "$0")" && pwd)"
fi

mkdir -p "$outdir"
if "$PY" -c "import docx" 2>/dev/null; then
  "$PY" "$here/render_documents.py" "$json" --format both --outdir "$outdir"
else
  "$PY" "$here/render_documents.py" "$json" --format html --outdir "$outdir"
  echo "error: python-docx 不可用，仅生成 html 预览" >&2
  exit 1
fi
cp "$json" "$outdir/$(basename "$json")" 2>/dev/null || true

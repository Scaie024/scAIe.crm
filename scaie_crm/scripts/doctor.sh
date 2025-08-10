#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "== scAIe Doctor =="
echo "Repo root: $ROOT_DIR"

need() { command -v "$1" >/dev/null 2>&1 || { echo "FALTA: $1"; return 1; }; }

ok=1
for c in bash git python3 node npm; do
  if ! need "$c"; then ok=0; fi
done
if [ $ok -eq 0 ]; then
  echo "Instala lo faltante. En macOS: brew install python node git"
fi

python3 --version || true
node -v || true
npm -v || true

if [ ! -f ".env" ]; then
  echo "No existe .env. Crea uno desde .env.example y completa claves."
else
  echo "Encontrado .env"
  grep -E '^(DASHSCOPE_API_KEY|QWEN_MODEL|DISABLE_LLM|DATABASE_URL|SECRET_KEY|TELEGRAM_BOT_TOKEN|BACKEND_URL)=' .env || true
fi

is_free() { ! lsof -iTCP:"$1" -sTCP:LISTEN >/dev/null 2>&1; }
for p in 8003 5173; do
  if is_free "$p"; then
    echo "Puerto $p libre"
  else
    echo "ADVERTENCIA: Puerto $p en uso"
  fi
done

curl -sSf "http://127.0.0.1:8003/health" >/dev/null 2>&1 && echo "Backend OK en /health" || echo "Backend no respondió /health (normal si no está corriendo)"

echo "== Doctor terminado =="

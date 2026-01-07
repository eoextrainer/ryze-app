#!/usr/bin/env bash
set -e
PORT=${PORT:-8000}
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

echo "Stopping any existing server on port ${PORT}..."
if command -v lsof >/dev/null 2>&1; then
  PIDS=$(lsof -t -i :"${PORT}" || true)
  if [ -n "${PIDS}" ]; then
    kill -9 ${PIDS} || true
  fi
fi

echo "Starting static server from ${ROOT_DIR} on port ${PORT}..."
cd "${ROOT_DIR}"
PY_BIN="${PY_BIN:-python3}"
"${PY_BIN}" -m http.server "${PORT}" >/tmp/ryze_server.log 2>&1 &
SERVER_PID=$!
echo "Server PID ${SERVER_PID}. Logs: /tmp/ryze_server.log"
sleep 1
if command -v xdg-open >/dev/null 2>&1; then
  xdg-open "http://localhost:${PORT}" >/dev/null 2>&1 &
fi

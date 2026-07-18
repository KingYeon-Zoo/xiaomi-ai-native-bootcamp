#!/usr/bin/env bash
#
# start.sh — one-command launcher for the Loops moderation system
# (llm_api approach: no local ML models, talks to a cloud LLM API)
#
# Brings up:  MongoDB (Docker) → FastAPI backend → React/Vite frontend
# Stop everything with Ctrl+C.
#
set -euo pipefail

# ── paths & config ──────────────────────────────────────────────────
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$ROOT_DIR/src/backend"
FRONTEND_DIR="$ROOT_DIR/src/frontend"
VENV_DIR="$BACKEND_DIR/.venv"

MONGO_CONTAINER="loops-mongo"
MONGO_VOLUME="loops-mongo-data"
MONGO_PORT="27017"
# Preferred backend port; auto-bumped if occupied (e.g. another local service).
BACKEND_PORT="${BACKEND_PORT:-8008}"

# ── pretty logging ──────────────────────────────────────────────────
c_blue="\033[1;34m"; c_green="\033[1;32m"; c_yellow="\033[1;33m"; c_red="\033[1;31m"; c_reset="\033[0m"
log()  { echo -e "${c_blue}▶${c_reset} $*"; }
ok()   { echo -e "${c_green}✅${c_reset} $*"; }
warn() { echo -e "${c_yellow}⚠️ ${c_reset} $*"; }
err()  { echo -e "${c_red}❌${c_reset} $*" >&2; }

# ── cleanup on exit ─────────────────────────────────────────────────
BACKEND_PID=""
FRONTEND_PID=""
cleanup() {
  echo ""
  log "Shutting down..."
  [ -n "$FRONTEND_PID" ] && kill "$FRONTEND_PID" 2>/dev/null || true
  [ -n "$BACKEND_PID" ]  && kill "$BACKEND_PID"  2>/dev/null || true
  # Leave the Mongo container running so data/state persists between runs.
  # Stop it manually with:  docker stop $MONGO_CONTAINER
  ok "Backend & frontend stopped. MongoDB container '$MONGO_CONTAINER' left running."
}
trap cleanup EXIT INT TERM

# ── 0. prerequisite checks ──────────────────────────────────────────
log "Checking prerequisites..."
command -v docker >/dev/null 2>&1 || { err "docker not found. Install Docker Desktop."; exit 1; }
command -v python3 >/dev/null 2>&1 || { err "python3 not found."; exit 1; }
command -v npm >/dev/null 2>&1 || { err "npm not found. Install Node.js 18+."; exit 1; }

if ! docker info >/dev/null 2>&1; then
  err "Docker daemon is not running. Start Docker Desktop and re-run this script."
  exit 1
fi
ok "docker, python3 ($(python3 --version 2>&1 | awk '{print $2}')), npm ($(npm --version)) present"

# Find a free backend port starting from the preferred one (some machines
# already run other services on 8000).
port_in_use() { lsof -iTCP:"$1" -sTCP:LISTEN -n -P >/dev/null 2>&1; }
_orig_port="$BACKEND_PORT"
while port_in_use "$BACKEND_PORT"; do
  BACKEND_PORT=$((BACKEND_PORT + 1))
  [ "$BACKEND_PORT" -gt $((_orig_port + 20)) ] && { err "No free port near $_orig_port."; exit 1; }
done
[ "$BACKEND_PORT" != "$_orig_port" ] && warn "Port $_orig_port busy — using $BACKEND_PORT instead"
API_TARGET="http://localhost:${BACKEND_PORT}"

# ── 1. MongoDB (idempotent) ─────────────────────────────────────────
log "Ensuring MongoDB container..."
if docker ps --format '{{.Names}}' | grep -qx "$MONGO_CONTAINER"; then
  ok "MongoDB already running"
elif docker ps -a --format '{{.Names}}' | grep -qx "$MONGO_CONTAINER"; then
  docker start "$MONGO_CONTAINER" >/dev/null
  ok "Started existing MongoDB container"
else
  # Bind to 127.0.0.1 only — the dev DB has no auth and must not be exposed.
  docker run -d \
    --name "$MONGO_CONTAINER" \
    -p 127.0.0.1:${MONGO_PORT}:27017 \
    -v "${MONGO_VOLUME}:/data/db" \
    mongo:7 >/dev/null
  ok "Created MongoDB container (mongo:7, 127.0.0.1:${MONGO_PORT})"
fi

# wait for Mongo to accept connections
log "Waiting for MongoDB to be ready..."
for i in $(seq 1 30); do
  if docker exec "$MONGO_CONTAINER" mongosh --quiet --eval 'db.runCommand({ping:1}).ok' >/dev/null 2>&1; then
    ok "MongoDB is ready"; break
  fi
  [ "$i" -eq 30 ] && { err "MongoDB did not become ready in time."; exit 1; }
  sleep 1
done

# ── 2. backend ──────────────────────────────────────────────────────
log "Setting up backend..."
cd "$BACKEND_DIR"

_install_backend_deps=0
if [ ! -x "$VENV_DIR/bin/python" ]; then
  python3 -m venv "$VENV_DIR"
  ok "Created virtualenv"
  _install_backend_deps=1
elif ! "$VENV_DIR/bin/python" -c 'import fastapi, uvicorn' >/dev/null 2>&1; then
  warn "Existing virtualenv is stale or was moved — rebuilding it"
  python3 -m venv --clear "$VENV_DIR"
  _install_backend_deps=1
fi
# shellcheck disable=SC1091
source "$VENV_DIR/bin/activate"

# Install only if a sentinel is missing (fast on repeat runs).
if [ ! -f "$VENV_DIR/.deps-installed" ] || [ "$_install_backend_deps" -eq 1 ]; then
  log "Installing lightweight backend deps (no torch)..."
  "$VENV_DIR/bin/python" -m pip install --quiet --upgrade pip
  "$VENV_DIR/bin/python" -m pip install --quiet -r requirements-llm.txt
  touch "$VENV_DIR/.deps-installed"
  ok "Backend deps installed"
else
  ok "Backend deps already installed (delete $VENV_DIR/.deps-installed to force reinstall)"
fi

[ -f .env ] || { cp .env.example .env; warn "Created src/backend/.env from example — add your ARK_API_KEY"; }

log "Starting FastAPI on :${BACKEND_PORT}..."
# 使用虚拟环境解释器按模块启动，避免目录移动后入口脚本的 shebang 失效。
"$VENV_DIR/bin/python" -m uvicorn app.main:app --host 0.0.0.0 --port "$BACKEND_PORT" --reload &
BACKEND_PID=$!

# wait for backend health
log "Waiting for backend to be ready..."
for i in $(seq 1 30); do
  if curl -sf "http://localhost:${BACKEND_PORT}/health" >/dev/null 2>&1; then
    ok "Backend healthy — http://localhost:${BACKEND_PORT}/docs"; break
  fi
  if ! kill -0 "$BACKEND_PID" 2>/dev/null; then err "Backend process died during startup."; exit 1; fi
  [ "$i" -eq 30 ] && { err "Backend did not become healthy in time."; exit 1; }
  sleep 1
done

# ── 3. frontend ─────────────────────────────────────────────────────
log "Setting up frontend..."
cd "$FRONTEND_DIR"
if [ ! -d node_modules ]; then
  log "Installing frontend deps..."
  npm install --silent
  ok "Frontend deps installed"
else
  ok "Frontend deps already installed"
fi

log "Starting Vite dev server on 127.0.0.1 (proxying /api → ${API_TARGET})..."
VITE_API_TARGET="$API_TARGET" npm run dev -- --host 127.0.0.1 &
FRONTEND_PID=$!

# ── done ────────────────────────────────────────────────────────────
echo ""
ok "All services up:"
echo -e "   ${c_green}Frontend${c_reset}  http://localhost:5173"
echo -e "   ${c_green}Backend${c_reset}   http://localhost:${BACKEND_PORT}  (docs: /docs)"
echo -e "   ${c_green}MongoDB${c_reset}   127.0.0.1:${MONGO_PORT}  (container: $MONGO_CONTAINER)"
echo ""
warn "Approach = llm_api. Add ARK_API_KEY to src/backend/.env for cloud evidence"
warn "(without it, required Agent evidence is unavailable and the policy routes conservatively)."
echo -e "${c_yellow}Press Ctrl+C to stop backend & frontend.${c_reset}"

# keep script alive until a child exits or Ctrl+C
wait

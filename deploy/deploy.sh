#!/usr/bin/env bash
# ============================================================
# deploy.sh — Deploys the "Exam Generator" infrastructure to
# the remote server 172.28.230.10 (DGX H200 USFQ)
#
# Usage:
#   ./deploy.sh              # Deploy (copy code + start)
#   ./deploy.sh --no-build   # Copy and start without rebuild
#   ./deploy.sh --down       # Tear down the infrastructure
#   ./deploy.sh --status     # Show container status
#
# Requirements:
#   - SSH key configured for 172.28.230.10 (user dpilacuan)
#   - tar available on the local machine (Git Bash includes it)
# ============================================================
set -euo pipefail

REMOTE_HOST="172.28.230.10"
REMOTE_USER="dpilacuan"
REMOTE_BASE="/home/${REMOTE_USER}/my_containers/exam"

# Project root directory (goes up 1 level from deploy/)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# ============================================================
# Functions
# ============================================================
remote() { ssh "${REMOTE_HOST}" "$@"; }

# Copies a set of files/directories to the remote using tar+ssh
# (more reliable than rsync on Windows/Git Bash environments).
# Usage: copy_tar <remote_dest> <file1> <dir1> ...
copy_tar() {
  local dest="$1"; shift
  tar -C "${PROJECT_ROOT}" -cf - "$@" | ssh "${REMOTE_HOST}" "tar -xf - -C ${dest}"
}

cmd_up() {
  echo "🚀 Creating remote directory..."
  remote "mkdir -p ${REMOTE_BASE}/projects/latex-compiler \
                 ${REMOTE_BASE}/projects/embedding-service \
                 ${REMOTE_BASE}/projects/exam-app \
                 ${REMOTE_BASE}/projects/frontend \
                 ${REMOTE_BASE}/docker/openwebui \
                 ${REMOTE_BASE}/data/agent_outputs \
                 ${REMOTE_BASE}/data/inputs \
                 ${REMOTE_BASE}/data/postgres \
                 ${REMOTE_BASE}/data/openwebui"

  echo "📦 Copying source code to the server..."
  copy_tar "${REMOTE_BASE}" \
    alembic.ini requirements.txt src scripts projects

  echo "🐳 Copying docker/ (compose, css)..."
  remote "mkdir -p ${REMOTE_BASE}/docker"
  copy_tar "${REMOTE_BASE}" \
    docker/openwebui

  # Copy the remote docker-compose.yml
  scp -q "$(dirname "${BASH_SOURCE[0]}")/docker-compose.yml" \
    "${REMOTE_USER}@${REMOTE_HOST}:${REMOTE_BASE}/docker-compose.yml"

  # Create the remote .env (the compose `environment` variables take
  # priority over the .env in pydantic-settings). OPENAI_API_KEY is
  # required by the USFQ LLM gateway and is read from the local .env.
  local api_key
  api_key="$(grep -E '^OPENAI_API_KEY=' "${PROJECT_ROOT}/.env" | head -n1 | cut -d= -f2-)"
  if [ -z "${api_key}" ]; then
    echo "❌ OPENAI_API_KEY not found in ${PROJECT_ROOT}/.env" >&2
    exit 1
  fi
  remote "cat > ${REMOTE_BASE}/.env << 'EOF'
LATEX_COMPILER_URL=http://latex-compiler:8080/compile
EOF"
  remote "echo \"OPENAI_API_KEY=${api_key}\" >> ${REMOTE_BASE}/.env"

  echo "⬆️  Starting the infrastructure..."
  if [ "${1:-}" = "--no-build" ]; then
    remote "cd ${REMOTE_BASE} && docker compose up -d"
  else
    remote "cd ${REMOTE_BASE} && docker compose up -d --build"
  fi

  echo "⏳ Waiting for postgres to be ready..."
  remote "for i in \$(seq 1 30); do docker exec exam_postgres_db pg_isready -U exam_user >/dev/null 2>&1 && break; sleep 2; done"

  echo "🔁 Verifying exam-app is running (retries if it failed on timing)..."
  remote "cd ${REMOTE_BASE} && docker compose up -d exam-app 2>/dev/null || true"
  sleep 5

  echo ""
  echo "✅ Infrastructure deployed on ${REMOTE_HOST}"
  echo "   - Frontend:   http://${REMOTE_HOST}:39005"
  echo "   - OpenWebUI:  http://${REMOTE_HOST}:39001"
  echo "   - API:        http://${REMOTE_HOST}:39002"
  echo "   - Postgres:   ${REMOTE_HOST}:39000"
  echo ""
  remote "cd ${REMOTE_BASE} && docker compose ps"
}

cmd_down() {
  echo "🛑 Tearing down the infrastructure..."
  remote "cd ${REMOTE_BASE} && docker compose down 2>/dev/null || true"
  echo "✅ Containers removed. Data (volumes) is preserved."
  echo "   To also delete the data: docker compose down -v"
}

cmd_status() {
  echo "📊 Infrastructure status on ${REMOTE_HOST}:"
  remote "cd ${REMOTE_BASE} && docker compose ps 2>/dev/null || echo 'No infrastructure deployed'"
}

# ============================================================
# Main
# ============================================================
case "${1:-up}" in
  up)         cmd_up ;;
  --no-build) cmd_up --no-build ;;
  down)       cmd_down ;;
  --down)     cmd_down ;;
  status)     cmd_status ;;
  --status)   cmd_status ;;
  *)
    echo "Usage: $0 [up|down|status|--no-build]"
    exit 1
    ;;
esac

#!/usr/bin/env bash
# down.sh — Tears down the Exam Generator infrastructure on the
# remote server 172.28.230.10.
#
# Behavior:
#   ./down.sh        → Removes containers + Docker volumes,
#                      BUT PRESERVES the data (which lives in the home
#                      as bind mounts, not in Docker volumes).
#   ./down.sh --full → Also deletes the home data (postgres,
#                      openwebui, agent_outputs, inputs).
#   ./down.sh --purge→ Deletes EVERYTHING (containers, volumes, data,
#                      built images and the remote directory).
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

REMOTE_HOST="172.28.230.10"
REMOTE_BASE="/home/dpilacuan/my_containers/exam"

case "${1:-}" in
  --full)
    echo "🛑 Removing containers, volumes and home DATA..."
    ssh "${REMOTE_HOST}" "cd ${REMOTE_BASE} && docker compose down -v 2>/dev/null || true"
    ssh "${REMOTE_HOST}" "rm -rf ${REMOTE_BASE}/data/postgres ${REMOTE_BASE}/data/openwebui ${REMOTE_BASE}/data/agent_outputs/* ${REMOTE_BASE}/data/inputs/* 2>/dev/null || true"
    echo "✅ Containers, volumes and data removed."
    ;;
  --purge)
    echo "💥 FULL PURGE — removing containers, volumes, data, images and directory..."
    ssh "${REMOTE_HOST}" "cd ${REMOTE_BASE} 2>/dev/null && docker compose down -v 2>/dev/null || true"
    ssh "${REMOTE_HOST}" "docker images -q | xargs -r docker rmi -f 2>/dev/null || true" 2>/dev/null || true
    ssh "${REMOTE_HOST}" "rm -rf ${REMOTE_BASE}"
    echo "✅ Everything removed. The directory ${REMOTE_BASE} no longer exists."
    ;;
  *)
    echo "🛑 Removing containers and Docker volumes (DATA is preserved in the home)..."
    ssh "${REMOTE_HOST}" "cd ${REMOTE_BASE} 2>/dev/null && docker compose down -v 2>/dev/null || true"
    echo ""
    echo "✅ Containers and Docker volumes removed."
    echo "   Data persists at: ${REMOTE_BASE}/data/"
    echo "   (postgres/, openwebui/, agent_outputs/, inputs/)"
    echo ""
    echo "   To start again: ./up.sh"
    echo "   To also delete the data: ./down.sh --full"
    ;;
esac


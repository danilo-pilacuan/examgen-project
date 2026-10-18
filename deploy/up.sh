#!/usr/bin/env bash
# up.sh — Starts the Exam Generator infrastructure on the
# remote server 172.28.230.10.
#
# Usage: ./up.sh            (copies code and starts with build)
#      ./up.sh --no-build (starts without rebuilding images)
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
./deploy.sh "${1:-up}"

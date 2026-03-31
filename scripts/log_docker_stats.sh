#!/usr/bin/env bash
# Append `docker stats --no-stream` for a container to a log file every N seconds (default 60).
# Usage:
#   ./scripts/log_docker_stats.sh [container] [output_file] [interval_seconds]
# Example:
#   ./scripts/log_docker_stats.sh litellm-litellm-1 ./litellm-docker-stats.log 60

set -euo pipefail

CONTAINER="${1:-litellm-litellm-1}"
OUTFILE="${2:-./litellm-docker-stats.log}"
INTERVAL="${3:-60}"

echo "Logging docker stats for '${CONTAINER}' every ${INTERVAL}s to '${OUTFILE}' (Ctrl+C to stop)" >&2

while true; do
  {
    echo "=== $(date -Iseconds) ==="
    docker stats "$CONTAINER" --no-stream
    echo ""
  } >>"$OUTFILE"
  sleep "$INTERVAL"
done

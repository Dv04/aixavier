#!/usr/bin/env bash
set -euo pipefail
PROFILE=${PROFILE:-all}
docker compose --profile ${PROFILE} build

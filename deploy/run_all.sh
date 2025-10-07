#!/usr/bin/env bash
set -euo pipefail
PROFILE=${PROFILE:-all}
PROFILE=$PROFILE docker compose --profile ${PROFILE} up --build

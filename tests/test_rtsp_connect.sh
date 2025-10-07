#!/usr/bin/env bash
set -euo pipefail
URL=${CAMERA_RTSP_URL_01:-demo://synthetic}
if [[ "$URL" == demo://synthetic ]]; then
  echo "Using synthetic demo stream"
  exit 0
fi
if command -v gst-launch-1.0 >/dev/null 2>&1; then
  gst-launch-1.0 -v rtspsrc location="$URL" ! fakesink -e >/tmp/rtsp_test.log 2>&1 || {
    cat /tmp/rtsp_test.log
    exit 1
  }
else
  echo "gst-launch not available; skipping"
fi

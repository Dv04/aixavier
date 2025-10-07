#!/usr/bin/env bash
set -euo pipefail
# Helper script to apply JetPack prerequisites after flashing.
# Assumes JetPack already installed via SDK Manager.

sudo apt-get update
sudo apt-get install -y \ 
  python3-pip python3-venv python3-opencv \ 
  gstreamer1.0-tools gstreamer1.0-plugins-{base,good,bad} \ 
  gstreamer1.0-libav libgstreamer1.0-dev \ 
  nvidia-jetpack

# Enable maximum clocks for benchmarking (optional).
if [[ "${ENABLE_JETSON_CLOCKS:-1}" == "1" ]]; then
  sudo /usr/bin/jetson_clocks
fi

# Configure power mode.
if [[ -n "${JETSON_POWER_MODE:-}" ]]; then
  sudo nvpmodel -m "${JETSON_POWER_MODE}"
fi

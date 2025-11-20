# Getting Started (Flash + Setup)
_Date: 2025-11-20_

This combines the bring-up checklist and setup steps for Jetson/x86 nodes.

## 1) Flash / Base OS
- Flash Jetson Xavier AGX/NX with your chosen JetPack (>=5.1 recommended).
- Set power profile after boot: `sudo nvpmodel -m 0` (45W AGX) or `-m 2` (25W NX).
- Lock thermals: `sudo /usr/bin/jetson_clocks` once cooling is verified.
- Patch + harden: `sudo apt update && sudo apt upgrade`; disable unused services (`cups`, `avahi-daemon`).
- Provision `/media/ssd` (ext4, `noatime`) and record device serial/MAC/GPU UUID.
- Configure time sync (PTP preferred) referencing `{{TIME_SYNC_SOURCE}}`.

## 2) System Packages
```bash
sudo apt update
sudo apt install -y python3-pip python3-venv git-lfs htop nvtop
bash deploy/install_jetpack.sh
bash deploy/install_deps.sh
```

## 3) Power & Thermals
- `sudo nvpmodel -m 0` (AGX) / `-m 2` (NX) for perf mode.
- `tegrastats` to watch temps; throttle guard at 85°C.

## 4) Storage Layout
- Clips: mount SSD at `/media/ssd` → symlink to `{{STORAGE_CLIPS_PATH}}`.
- Logs: `/var/log/edge-cctv` (bind-mount to Docker volumes).
- Create logrotate entry: `deploy/logrotate-edge-cctv`.

## 5) Repository Bootstrap
```bash
git clone {{GIT_REMOTE_URL}}
cd edge-cctv-jetson
cp .env.example .env
make placeholders:list
make placeholders:resolve FROM=.env
make bootstrap
```

## 6) Initial Run
```bash
make demo      # synthetic pipeline
make perf      # baseline metrics
```

## 7) UI / API (FastAPI)
- Mount router from `src/aixavier/ui/api.py` for ROI/events/toggles.

## 8) Production Rollout
- Populate `configs/cameras.yaml` per coach.
- Render systemd services from `deploy/systemd/*.service`:
  ```bash
  sudo cp deploy/systemd/*.service /etc/systemd/system/
  sudo systemctl enable edge-cctv.target
  sudo systemctl start edge-cctv.target
  ```
- Resolve placeholders before shipping: `make placeholders:check`.

> This file replaces `docs/SETUP.md` and `deploy/flash-checklist.md`.

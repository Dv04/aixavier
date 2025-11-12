# Setup

## 1. Base OS & JetPack
1. Flash Jetson Xavier AGX/NX with desired JetPack release (>=5.1 recommended).
2. Complete `deploy/flash-checklist.md` before network access.
3. (Optional) Lock rootfs to read-only after docker stack verified.

## 2. System Packages
```bash
sudo apt update
sudo apt install -y python3-pip python3-venv git-lfs htop nvtop
bash deploy/install_jetpack.sh
bash deploy/install_deps.sh
```

## 3. Power & Thermals
- Set power profile via `sudo nvpmodel -m 0` (45W AGX) or `-m 2` (25W NX).
- Run `sudo /usr/bin/jetson_clocks` during benchmarking; disable for steady-state if thermal margin <10 °C.
- Monitor temps with `tegrastats`; throttle guard at 85 °C.

## 4. Storage Layout
- Clips: mount SSD at `/media/ssd` and symlink to `{{STORAGE_CLIPS_PATH}}`.
- Logs: persist under `/var/log/edge-cctv` (bind-mount to docker volumes).
- Configure logrotate: copy `deploy/logrotate-edge-cctv` (create before enabling).

## 5. Time Sync
- Preferred: PTP Grandmaster at {{TIME_SYNC_SOURCE}}.
- Fallback: `chrony` with GPS PPS; ensure `timedatectl status` shows `System clock synchronized: yes`.

## 6. Repository Bootstrap

```bash
git clone {{GIT_REMOTE_URL}}
cd edge-cctv-jetson
cp .env.example .env
# Fill in required secrets and config keys in .env
make placeholders:list                  # discover unresolved placeholders
make placeholders:resolve FROM=.env     # render .env into configs/*
make bootstrap
```

**Important:** Before deploying or shipping, run `make placeholders:check` to ensure all required secrets and config keys are resolved. Only commit `.env.example` and templates—never real secrets. See [`docs/placeholders.md`](docs/placeholders.md) and the [README](../README.md) for onboarding and hygiene guidance.

## 7. Initial Run

```bash
make demo    # validates synthetic pipeline, no external streams
make perf    # capture baseline metrics (stores under artifacts/perf)
```

## 9. UI Endpoints

The FastAPI UI backend exposes endpoints for ROI editing, event browsing, and toggles:

- `POST /ui/roi` – Add a region of interest
- `GET /ui/roi` – List all ROIs
- `DELETE /ui/roi/{roi_id}` – Delete an ROI
- `POST /ui/events` – Add an event
- `GET /ui/events` – List all events
- `POST /ui/toggles` – Set a UI toggle
- `GET /ui/toggles` – List all toggles

Mount the UI router from `src/aixavier/ui/api.py` in your FastAPI app, or use the demo Compose service for local testing. See `src/aixavier/ui/README.md` for details.

## 8. Production Rollout
- Populate `configs/cameras.yaml` for each coach.
- Render systemd units using `deploy/systemd/*.service` and enable target:
  ```bash
  sudo cp deploy/systemd/*.service /etc/systemd/system/
  sudo systemctl enable edge-cctv.target
  sudo systemctl start edge-cctv.target
  ```
- Configure secrets via placeholder resolver before switching PROFILE=production.


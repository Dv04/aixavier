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
# fill placeholders via tools
make placeholders:list
make placeholders:resolve FROM=.env
make bootstrap
```

## 7. Initial Run
```bash
make demo    # validates synthetic pipeline, no external streams
make perf    # capture baseline metrics (stores under artifacts/perf)
```

## 8. Production Rollout
- Populate `configs/cameras.yaml` for each coach.
- Render systemd units using `deploy/systemd/*.service` and enable target:
  ```bash
  sudo cp deploy/systemd/*.service /etc/systemd/system/
  sudo systemctl enable edge-cctv.target
  sudo systemctl start edge-cctv.target
  ```
- Configure secrets via placeholder resolver before switching PROFILE=production.


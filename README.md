# Aixavier Edge Analytics Stack

> Railway-grade CCTV analytics, automation agents, and orchestration tooling tuned for NVIDIA Jetson Xavier (AGX / NX).

This repository contains everything needed to ingest RTSP/ONVIF feeds, execute 22 analytics workloads, surface events, and keep the stack documented through an automation agent that curates model intel and changelogs. The current layout is being refactored toward the conventions captured in `AGENTS.md`; refer to that guide when adding new modules under `src/aixavier/`.

## Quickstart
```bash
git clone https://github.com/{{ORG_NAME}}/aixavier.git
cd aixavier
cp .env.example .env                    # keep placeholders until secrets are issued
make placeholders:list                  # discover required variables
make placeholders:resolve FROM=.env     # map .env into configs/*
make bootstrap                          # create .venv, install deps, warm TensorRT engines
make demo                               # bring up docker-compose demo with synthetic RTSP feed
```

Once the demo profile is healthy, switch to production profiles by exporting `PROFILE=all` (full 22-rule workload) or pointing to a bespoke profile file via `PROFILE=path/to/profile.yaml`.

## Daily Driver Commands
| Command | Purpose |
|---------|---------|
| `make bootstrap` | Bootstrap virtualenv, install runtime + dev tooling, pre-build engines. |
| `make run PROFILE=<name>` | Launch the docker compose stack for the selected profile. |
| `make demo` | Generate demo assets and start the curated eight-rule showcase. |
| `make perf` | Capture FPS, latency, and GPU utilisation snapshots from the exporter API. |
| `make test` | Run pytest suite plus RTSP smoke tests. |
| `make lint` | Run ruff (lint) and mypy (type checks) over `src` and `tools`. |
| `make agent:refresh -- --dry-run` | Exercise the maintainer agent without mutating docs. |
| `make clean` | Tear down compose services, remove the virtualenv, and clear caches. |

### Model assets
- Place development ONNX exports under `models/yolo/onnx/` and `models/pose/onnx/` if you want CPU-backed inference.
- Promote production TensorRT engines (FP16/INT8) into `models/usecases/<use-case>/fp16|int8/` and update `configs/detectors/*.yaml` to match.
- Run `models/bootstrap_models.py` to generate placeholder files when CI needs to stub missing assets.

### Webcam smoke test
```bash
export CAMERA_RTSP_URL_01=webcam://0   # change index if you have multiple cameras
make run PROFILE=demo                  # launches ingest + detectors using your webcam frames
```
The ingest service recognises `webcam://<index>` in `configs/cameras.yaml` (or `.env`). Use this to validate detections locally before pointing at RTSP/ONVIF streams.

### Generating detector engines
1. Export ONNX (if you haven’t already) and place it under `models/usecases/<use-case>/onnx/`.
2. Convert to TensorRT FP16 on Jetson/x86 with TensorRT installed:
   ```bash
   trtexec \
     --onnx=models/usecases/pose/rtmpose_onnx/.../end2end.onnx \
     --saveEngine=models/usecases/pose/fp16/rtmpose.engine \
     --fp16 --workspace=4096
   trtexec \
     --onnx=models/usecases/object_detection/onnx/yolov8n.onnx \
     --saveEngine=models/usecases/object_detection/fp16/yolov8n.engine \
     --fp16 --workspace=4096
   ```
3. Update `configs/detectors/object.yaml` / `configs/detectors/pose_velocity.yaml` if your filenames differ. Leave INT8 calibration for later (the scripts under `models/*/calibrate.sh` act as placeholders until we capture calibration sets).

## Runtime Profiles at a Glance
| Profile | Focus | FPS Target | Notable Intervals |
|---------|-------|------------|-------------------|
| `minimal` | Tamper + Trespass | 30 | Detectors on every frame. |
| `demo` | Eight representative use cases | 25 | Action detectors every 3 frames, face recognition every 2. |
| `all` | Full 22-rule workload | 25 | Per-use-case intervals in `configs/usecases/*.yaml`. |

Select a profile by exporting `PROFILE=<name>` or passing `PROFILE=...` to individual make targets. Compose profiles live under `docker-compose.yml`.

## System Overview
1. **Ingest (`src/ingest_gst/`)** – DeepStream-based RTSP/ONVIF ingestion with automatic reconnects, watermarks, and NVMM zero-copy paths.
2. **Runners (`src/runners/`)** – TensorRT engines (FP16 baseline, INT8 optional) grouped by modality: object, face, pose, action, smoke, and violence. The shared detector runtime (`src/runners/detectors.py`) can fall back to ONNX/CPU inference when engines are absent, so you can validate pipelines before dropping production engines into `models/usecases/`.
3. **Trackers (`src/trackers/`)** – currently a lightweight IoU-based `SimpleTracker` for stable IDs; upgrade to ByteTrack + ReID before production.
4. **Rules (`src/rules/`)** – YAML-driven behavioural engine handling ROIs, dwell times, line crossings, and domain-specific semantics.
5. **Privacy (`src/privacy/`)** – SCRFD + ArcFace inference, encrypted embeddings, RBAC checks, and audit logging.
6. **Events (`src/events/`)** – Normalises detections, ships MQTT/REST payloads, and persists artefacts.
7. **Recorder (`src/recorder/`)** – Circular buffers with pre/post recording windows, watermarking, hashing, and export flows.
8. **Exporter (`src/exporter/`)** – Prometheus metrics and OpenTelemetry traces surfaced via HTTP.
9. **UI (`src/ui/`)** – FastAPI backend and Streamlit-based dashboard with live mosaics and ROI editor.
10. **Automation Agent (`src/agent/`)** – Gathers model intelligence, updates documentation, and logs activity to `HANDOFF.md`.

The refactor toward `src/aixavier/` will co-locate agents under `src/aixavier/agents/` and shared infrastructure under `src/aixavier/core/`. Existing modules will migrate in-place; prefer those paths for new code.

## Repository Layout
- `AGENTS.md` – Contribution, testing, and naming conventions (read before opening PRs).
- `configs/` – Profiles, rulepacks, camera definitions, and placeholder-friendly YAML.
- `deploy/` – Flash scripts, systemd units, Grafana dashboards, and logrotate configs.
- `docs/` – Operational runbooks (`SETUP.md`, `PERFORMANCE.md`, `PRIVACY.md`, `TROUBLESHOOT.md`, etc).
- `docs/IMPLEMENTATION_STATUS.md` – Snapshot of current service/model progress for quick onboarding.
- `models/` – TensorRT engine builders and calibration scripts.
- `models/usecases/` – drop-in folder for the 22 production-ready detection/pose engines (place FP16/INT8 artifacts here when promoting models).
- `src/` – Runtime services and automation agent (pending relocation to `src/aixavier/`).
- `tests/` – Pytest suites, fixtures, and RTSP connectivity scripts.
- `tools/` – Placeholder resolvers, lint helpers, and release automation.
- `HANDOFF.md` – Append-only log shared with the automation agent.
- `.env.example` – Placeholder inventory; keep secrets out of Git.

## Documentation & Observability
- Metrics surface at `http://{{PROMETHEUS_SCRAPE_PORT}}/metrics`; Grafana dashboard JSON lives in `deploy/grafana/edge-cctv.json`.
- Refer to `docs/TROUBLESHOOT.md` for RTSP/ONVIF, codec, and thermal triage.
- `docs/PERFORMANCE.md` outlines DeepStream batching, detector intervals, and `nvpmodel` presets.
- `docs/placeholders.md` serves as the live index for required secrets and config keys.

## Automation Agent Workflow
The maintainer bot runs via `make agent:refresh` or the scheduled workflow under `.github/workflows/agent-refresh.yml`. It:
- Scans for new vision models and datasets (`src/agent/webscan`).
- Ranks candidates based on deployment constraints (`src/agent/rank`).
- Updates documentation blocks and logs actions to `HANDOFF.md`.

Gate the agent with a dry run before allowing it to write:
```bash
make agent:refresh -- --dry-run
```
When satisfied, drop the `--dry-run` flag to persist updates.

## Security & Placeholder Hygiene
- Never substitute real credentials directly in committed files—leave `{{PLACEHOLDER}}` tokens intact.
- Use `make placeholders:check` to ensure all placeholders resolve before shipping production builds.
- Secrets live in `.env` (gitignored) and environment-specific secret stores.

## Governance & Next Steps
- Follow Conventional Commits and keep subject lines ≤72 characters.
- CI (see `.github/workflows/agent-ci.yml`) runs lint, tests, placeholder checks, and secret scanning.
- Record any roadmap items in `docs/roadmap.md` (coming soon) rather than inline TODO comments.
- The next structural milestone is migrating runtime modules under `src/aixavier/` per `AGENTS.md`.

## Live Auto Sections
<!-- auto:start name=recommended-models -->
| Rank | Task | Model | FP16 (ms) | INT8 (ms) | Accuracy | License | Last Checked |
|------|------|-------|-----------|-----------|----------|---------|--------------|
| 1 | face_recognition | MobileFaceNet ArcFace | 2.10 | 1.50 | 0.996 | MIT | 2025-09-27 |
| 2 | reid | OSNet_x0_25 | 1.90 | 1.30 | 0.508 | MIT | 2025-09-22 |
| 3 | face_detection | SCRFD-500M | 6.20 | 4.10 | 0.915 | MIT | 2025-09-27 |
| 4 | fire_smoke_detection | EfficientNet-B0 Fire | 9.80 | 6.70 | 0.923 | Apache-2.0 | 2025-09-18 |
| 5 | violence_detection | MobileNet-TSM | 12.90 | 9.00 | 0.842 | Apache-2.0 | 2025-09-21 |
| 6 | pose_estimation | YOLOv8n-pose | 11.30 | 7.90 | 0.608 | GPLv3 | 2025-09-30 |
<!-- auto:end -->

<!-- auto:start name=performance-tuning -->
- **DeepStream primary-gie batching**: Use batch-size=2 for YOLOv8n on AGX when PROFILE=all; falls back to 1 on NX. (_Impact_: Improves ingest FPS by ~8% while keeping latency under 40 ms.)
- **TensorRT DLA offload**: Assign SCRFD embedding head to DLA0 in demo profile to free SMs for violence detector. (_Impact_: Reduces GPU util by 6% during peak loads.)
- **Recorder I/O buffering**: Set GStreamer queue `max-size-time=3000000000` (3 s) for circular buffer stability. (_Impact_: Prevents underflow when writing to slower eMMC storage.)
<!-- auto:end -->

<!-- auto:start name=known-issues -->
- **[MEDIUM] INT8 export fails for YOLOv10n on TensorRT 8.6.1** — The TensorRT ONNX parser in JetPack 5.1.2 lacks support for new YOLOv10 detection head ops. _Impact_: INT8 acceleration unavailable for YOLOv10n until JetPack 6 or custom plugin compiled. _Workaround_: Stick to FP16 or backport the opset-18 plugin from TensorRT OSS. [Details](https://github.com/THU-MIG/yolov10/issues/42)
- **[LOW] SCRFD false positives in dense steam scenarios** — Steam near coach doors triggered high-confidence face detections. _Impact_: FRS blur triggers and audit noise during cleaning cycles. _Workaround_: Enable ROI mask for door corners and tighten `FRS_THRESHOLD` to 0.52 when cleaning profile active. [Details](https://insightface.ai/docs/scrfd/troubleshooting)
- **[HIGH] X3D-S memory spike on Jetson Xavier NX 8GB** — Batch=2 clip inference spikes VRAM over 7.2GB causing OOM with UI co-located. _Impact_: Violence detector crashes on NX unless intervals increased. _Workaround_: Set `ACTION_CLIP_BATCH=1` and raise clip stride to 3. [Details](https://forums.developer.nvidia.com/t/x3d-s-oom/298741)
<!-- auto:end -->

<!-- auto:start name=changelog -->
- 2025-10-07: Catalog refresh (models=10, datasets=44, placeholders=40).
- 2025-10-07: Catalog refresh (models=10, datasets=44, placeholders=42).
- 2025-10-07: Initial repository scaffold for Jetson Xavier railway CCTV analytics.
- 2025-10-07: Updated README to document bootstrap commands, module layout, and upcoming `src/aixavier/` migration.
<!-- auto:end -->
- Detector post-processing unit tests rely on NumPy; set `AIXAVIER_ENABLE_NUMPY_TESTS=1` when that runtime is available.

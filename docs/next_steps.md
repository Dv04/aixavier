# Next Steps – Aixavier Edge Analytics Stack
_Date: 2025-10-29_

## TL;DR
**Verdict:** The repo is **demo-ready** (synthetic pipeline works via `docker-compose` and `make demo`), but **not yet production-ready / deployable to real cameras**. Several components are stubs or simulations (detectors, tracker, recorder, exporter); secrets are unresolved ({42} placeholders), model bootstrap creates placeholders not real engines, and CI would fail the placeholder hygiene check.

What’s left is to replace simulated pieces with real implementations, resolve secrets, tighten CI, and complete privacy/recording paths for a compliant rollout.

---

## What I checked
- Repository structure, code modules in `src/`, Dockerfiles, and `docker-compose.yml`.
- Configs under `configs/`, docs under `docs/`, deploy assets (`deploy/`), and Makefile targets.
- Tests in `tests/` and CI workflows in `.github/workflows/`.
- Presence of placeholder secrets and placeholder-resolver tooling.

## Services & modules at a glance
**Compose services (13):** ingest, detect_object, detect_face, detect_action, tracker, rules, events, privacy, recorder, ui, exporter, agent, demo_rtsp

**Makefile targets:** agent:refresh, bootstrap, ci, clean, demo, format, help, lint, perf, placeholders:check, placeholders:list, placeholders:resolve, run, run-detached, stop, test

### Component readiness matrix
| Component | main/app | Dockerfile | In compose | Tests | Status |
|---|---:|---:|---:|---:|---|
| agent | ✅ | ✅ | ✅ | — | Demo-ready (no tests) |
| common | — | — | — | ✅ | Library |
| events | ✅ | ✅ | ✅ | ✅ | Demo-ready |
| exporter | ✅ | ✅ | ✅ | — | Demo-ready (no tests) |
| ingest_gst | ✅ | ✅ | ✅ | — | Demo-ready (no tests) |
| privacy | ✅ | ✅ | ✅ | — | Demo-ready (no tests) |
| recorder | ✅ | ✅ | ✅ | — | Demo-ready (no tests) |
| rules | ✅ | ✅ | ✅ | ✅ | Demo-ready |
| runners | ✅ | ✅ | ✅ | — | Demo-ready (no tests) |
| trackers | ✅ | ✅ | ✅ | — | Demo-ready (no tests) |
| ui | ✅ | ✅ | ✅ | ✅ | Demo-ready |

Notes:
- `runners` powers three services `detect_object`, `detect_face`, `detect_action` and currently **simulates** detections.
- `recorder` writes JSON artifacts, not video; `exporter` reports **simulated** metrics; `ui` is a minimal FastAPI API.
- `ingest_gst` produces frames from synthetic/demo sources; RTSP/ONVIF capture paths are present but need validation on-device.

## Placeholder & secrets inventory
- **Distinct placeholders:** **42**  
  (Run `make placeholders:list` and `make placeholders:check` to validate; current linter reports failures.)
- Examples: CAMERA_ONVIF_HOST_01, CAMERA_ONVIF_PASS, CAMERA_ONVIF_USER, CAMERA_RTSP_URL_01, DATASET_PATH_FACE_CALIB, DATASET_PATH_FIRE_SMOKE, DATASET_PATH_OBJECT_CALIB, DATASET_PATH_POSE_CALIB, DATASET_PATH_REID_CALIB, DATASET_PATH_VIOLENCE, EVENTS_REST_ENDPOINT, FRS_BLACKLIST_EMBEDDING_01…

> Resolution flow: copy `.env.example` → `.env`, then `make placeholders:resolve FROM=.env` to render into `configs/*`. Keep real secrets out of Git.

## Gaps & recommended next steps (by area)

### P0 — Must-have to implement real deployments
1. **Real detectors (TensorRT + DeepStream)**  
   - Replace simulated emits in `src/runners/main.py` with model-backed inference for **object**, **face**, **action**, **pose**.  
   - Wire runners to artifacts from `models/*/export_trt.sh` (or add a real downloader/builder in `models/bootstrap_models.py`, which currently writes placeholders).
2. **Live ingest over RTSP/ONVIF**  
   - Validate `src/ingest_gst/pipeline.py` on Jetson (reconnects, FPS limiting, NVMM zero-copy).  
   - Confirm ONVIF time-sync and per-camera configs in `configs/cameras.yaml`.
3. **Tracking**  
   - Implement BYTETrack + optional OSNet ReID in `src/trackers/` (now pass‑through). Verify stable IDs across motion/occlusion.
4. **Rules engine completeness**  
   - Finish all rule handlers in `src/rules/engine.py` (ROI, lines, dwell, velocity drop, trespass, action-score, etc.). Current tests cover basics only.  
   - Validate rulepack YAMLs under `configs/usecases/*.yaml` against real events.
5. **Recorder (circular video buffers)**  
   - Replace JSON stubs with real pre/post video clip spooling, watermarking, hashing, and export manifests.
6. **Privacy & FRS**  
   - Implement encrypted embedding store in `src/privacy/store.py`, FastAPI endpoints for enrollment/match/whitelist/blacklist, and RBAC enforcement.  
   - Honor per-camera privacy settings (blur non-matches; approval for exports).
7. **Exporter / Observability**  
   - Replace simulated metrics with NVML/tegrastats readings, detector latency histograms, and per-camera FPS.  
   - Confirm Prometheus scrape on `PROMETHEUS_SCRAPE_PORT` and ship Grafana dashboard (`deploy/grafana/edge-cctv.json`).
8. **Secrets & placeholders**  
   - Resolve **all 42 placeholders** and commit only templates. Gate CI on `make placeholders:check`.

### P1 — Quality, safety, & ops
- **End-to-end tests on Xavier (AGX/NX)**: RTSP smoke (`tests/test_rtsp_connect.sh`) plus golden-event assertions for a few rulepacks.  
- **CI hardening**: Expand `.github/workflows/agent-ci.yml` to build container images and run headless tests; fail PRs on unresolved placeholders, lint, and mypy.  
- **Container baselines**: Ensure `nvcr.io/nvidia/l4t-base:35.4.1` aligns with the installed JetPack; pin DeepStream images.  
- **Deployment**: Validate `deploy/systemd/*.service` units on-device; confirm volumes (`/data/recordings`, `/data/exports`, logs) ownership and quota/retention.  
- **Security**: OAuth/OIDC proxy in front of UI, short‑lived JWTs, mTLS for events REST when used over WAN; secret scanning in CI.

### P2 — UX & docs
- **UI**: Add ROI editor, live camera mosaic, rulepack toggles, and event browser.  
- **Docs**: Flesh out `docs/SETUP.md`, `PRIVACY.md`, and `TROUBLESHOOT.md` with concrete JetPack/DeepStream versions and gotchas.  
- **README**: Replace the placeholder sections (auto blocks) after the maintainer agent writes first real tables.

## Evidence (auto-collected)

### Compose services
- ingest
- detect_object
- detect_face
- detect_action
- tracker
- rules
- events
- privacy
- recorder
- ui
- exporter
- agent
- demo_rtsp

### Makefile targets
- `agent:refresh`
- `bootstrap`
- `ci`
- `clean`
- `demo`
- `format`
- `help`
- `lint`
- `perf`
- `placeholders:check`
- `placeholders:list`
- `placeholders:resolve`
- `run`
- `run-detached`
- `stop`
- `test`

### Placeholders (complete list, with sample locations)
- **{{CAMERA_ONVIF_HOST_01}}** — e.g., .env.example
- **{{CAMERA_ONVIF_PASS}}** — e.g., .env.example
- **{{CAMERA_ONVIF_USER}}** — e.g., .env.example
- **{{CAMERA_RTSP_URL_01}}** — e.g., .env.example
- **{{DATASET_PATH_FACE_CALIB}}** — e.g., .env.example
- **{{DATASET_PATH_FIRE_SMOKE}}** — e.g., .env.example
- **{{DATASET_PATH_OBJECT_CALIB}}** — e.g., .env.example
- **{{DATASET_PATH_POSE_CALIB}}** — e.g., .env.example
- **{{DATASET_PATH_REID_CALIB}}** — e.g., .env.example
- **{{DATASET_PATH_VIOLENCE}}** — e.g., .env.example
- **{{EVENTS_REST_ENDPOINT}}** — e.g., .env.example
- **{{FRS_BLACKLIST_EMBEDDING_01}}** — e.g., docs/placeholders.md
- **{{FRS_BLACKLIST_NAME_01}}** — e.g., docs/placeholders.md
- **{{FRS_BLACKLIST_REASON_01}}** — e.g., docs/placeholders.md
- **{{FRS_ENROLLMENT_OPERATOR_NAME}}** — e.g., .env.example
- **{{FRS_STAFF_EMBEDDING_01}}** — e.g., docs/placeholders.md
- **{{FRS_STAFF_EMPLOYEE_ID_01}}** — e.g., docs/placeholders.md
- **{{FRS_STAFF_NAME_01}}** — e.g., docs/placeholders.md
- **{{FRS_THRESHOLD}}** — e.g., .env.example
- **{{FRS_WHITELIST_EMBEDDING_01}}** — e.g., docs/placeholders.md
- **{{FRS_WHITELIST_EXPIRY_01}}** — e.g., docs/placeholders.md
- **{{FRS_WHITELIST_NAME_01}}** — e.g., docs/placeholders.md
- **{{GIT_REMOTE_URL}}** — e.g., .env.example
- **{{INSTALL_PREFIX}}** — e.g., .env.example
- **{{METRICS_PUSH_URL}}** — e.g., .env.example
- **{{MQTT_BROKER_HOST}}** — e.g., .env.example
- **{{MQTT_BROKER_PASS}}** — e.g., .env.example
- **{{MQTT_BROKER_URL}}** — e.g., .env.example
- **{{MQTT_BROKER_USER}}** — e.g., .env.example
- **{{ORG_NAME}}** — e.g., README.md
- **{{PLACEHOLDER}}** — e.g., README.md
- **{{PROMETHEUS_SCRAPE_PORT}}** — e.g., README.md
- **{{RETENTION_DAYS}}** — e.g., .env.example
- **{{SEC_EXPORT_ENCRYPTION_KEY}}** — e.g., .env.example
- **{{STORAGE_CLIPS_PATH}}** — e.g., .env.example
- **{{STORAGE_EXPORT_PATH}}** — e.g., .env.example
- **{{TIME_SYNC_SOURCE}}** — e.g., .env.example
- **{{UI_ADMIN_PASS}}** — e.g., .env.example
- **{{UI_ADMIN_USER}}** — e.g., .env.example
- **{{UI_HOST}}** — e.g., .env.example
- **{{UI_PORT}}** — e.g., .env.example
- **{{UPPER_SNAKE_CASE}}** — e.g., tools/resolve_placeholders.py

### Tests present
- `tests/test_rules.py` — rule engine triggers  
- `tests/test_perf.py` — metrics scrape parser  
- `tests/test_rtsp_connect.sh` — RTSP connectivity smoke  
(Overall test coverage is still low.)

## Quick “go / no‑go”
- **Go for demo**: You can run `make demo` locally and see synthetic events flow through the stack.  
- **No‑go for production**: Replace simulations, finalize privacy/recording, and resolve secrets before real deployments.

---

_This file was generated by inspecting the repository snapshot only; no internet access or external builds were run._

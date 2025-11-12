# Next Steps – Aixavier Edge Analytics Stack
_Date: 2025-11-09_

## TL;DR

**Verdict:** The repo is **demo-ready** for the eight workloads covered by the current detectors/rules and now carries a **single source of truth for all 22 analytics use cases** via the new manifest/registry. We are still **not production-ready**: face/action detectors stay simulated, secrets remain unresolved (40 placeholders), model bootstrap only creates placeholders, and CI would fail the placeholder hygiene gate.

**Onboarding:** See [`docs/IMPLEMENTATION_STATUS.md`](docs/IMPLEMENTATION_STATUS.md) for live service/model status, [`docs/placeholders.md`](docs/placeholders.md) for placeholder hygiene, and the [README](../README.md) for quickstart and contribution rules.

Recent work (2025-11-09):
- Parsed `All Data Analytics use cases for CCTV under POC.xlsx` into `assets/usecases/catalog.yaml` and surfaced it through `src/aixavier/core/usecases.py` so rules/tests/CLI can reason over all 22 workloads.
- Taught `src/rules/engine.py` to hydrate metadata from the registry (complete with `summary()`), ensuring even unimplemented workloads appear in reports.
- Updated docs and configs to pull ONNX weights from modality folders (`models/pose/onnx/...`) and kept TensorRT promotion under `models/usecases/<slug>/`.
- Carried forward earlier detector-and-runner fixes (object + pose ONNX/TRT runtime) plus demo profile wiring.

---

## What I checked
- Repository structure, code modules in `src/`, Dockerfiles, and `docker-compose.yml`.
- Configs under `configs/`, docs under `docs/`, deploy assets (`deploy/`), and Makefile targets.
- Tests in `tests/` and CI workflows in `.github/workflows/`.
- Presence of placeholder secrets and placeholder-resolver tooling.
- `All Data Analytics use cases for CCTV under POC.xlsx` → generated manifest at `assets/usecases/catalog.yaml` and cross-checked that every slug matches the existing `configs/usecases/*.yaml` files.

## Services & modules at a glance
**Compose services (14):** ingest, detect_object, detect_pose, detect_face, detect_action, tracker, rules, events, privacy, recorder, ui, exporter, agent, demo_rtsp

**Makefile targets:** agent:refresh, bootstrap, ci, clean, demo, format, help, lint, perf, placeholders:check, placeholders:list, placeholders:resolve, run, run-detached, stop, test

### Component readiness matrix
| Component  | main/app | Dockerfile | In compose | Tests | Status                                                 |
| ---------- | -------: | ---------: | ---------: | ----: | ------------------------------------------------------ |
| agent      |        ✅ |          ✅ |          ✅ |     — | Demo-ready (no tests)                                  |
| common     |        — |          — |          — |     ✅ | Library                                                |
| events     |        ✅ |          ✅ |          ✅ |     ✅ | Demo-ready                                             |
| exporter   |        ✅ |          ✅ |          ✅ |     — | Demo-ready (simulated metrics)                         |
| ingest_gst |        ✅ |          ✅ |          ✅ |     — | Demo-ready (RTSP + webcam); needs on-device validation |
| privacy    |        ✅ |          ✅ |          ✅ |     — | Demo-ready (simulated matching)                        |
| recorder   |        ✅ |          ✅ |          ✅ |     — | Demo-ready (JSON stubs)                                |
| rules      |        ✅ |          ✅ |          ✅ |     ✅ | Demo-ready                                             |
| runners    |        ✅ |          ✅ |          ✅ |     ✅ | Object/Pose operational; face/action simulated         |
| trackers   |        ✅ |          ✅ |          ✅ |     ✅ | Demo-ready (ByteTrack-lite; add ReID later)            |
| ui         |        ✅ |          ✅ |          ✅ |     ✅ | Demo-ready                                             |

Notes:
- `runners` powers four services (`detect_object`, `detect_pose`, `detect_face`, `detect_action`); object/pose use the shared detector runtime, while face/action remain simulated.
- `trackers` now assigns stable IDs via `SimpleTracker` (IoU-based); replace with ByteTrack + ReID when production ready.
- `recorder` writes JSON artifacts, not video; `exporter` reports **simulated** metrics; `ui` is a minimal FastAPI API.
- `ingest_gst` produces frames from synthetic/demo sources; RTSP/ONVIF capture paths are present but need validation on-device.
- Production-ready TensorRT engines should be staged under `models/usecases/<use-case>/` and referenced from `configs/detectors/*.yaml` before shipping.

## Placeholder & secrets inventory
- **Distinct placeholders:** **40**  
  (Run `make placeholders:list` and `make placeholders:check` to validate; current linter reports failures.)
- Examples: CAMERA_ONVIF_HOST_01, CAMERA_ONVIF_PASS, CAMERA_ONVIF_USER, CAMERA_RTSP_URL_01, DATASET_PATH_FACE_CALIB, DATASET_PATH_FIRE_SMOKE, DATASET_PATH_OBJECT_CALIB, DATASET_PATH_POSE_CALIB, DATASET_PATH_REID_CALIB, DATASET_PATH_VIOLENCE, EVENTS_REST_ENDPOINT, FRS_BLACKLIST_EMBEDDING_01…

> Resolution flow: copy `.env.example` → `.env`, then `make placeholders:resolve FROM=.env` to render into `configs/*`. Keep real secrets out of Git.

## Gaps & recommended next steps (by area)

### P0 — Must-have to implement real deployments
1. **Bridge the 14 planned (non demo-ready) use cases surfaced by the registry**  
   - Use `UseCaseRegistry.summary()` (or the table in `docs/IMPLEMENTATION_STATUS.md`) to track progress per slug.  
   - Assign detector owners for audio (`calling_out_signal_aspect`), telemetry joiners (`coach_door_panel_security`, `panic_alarm_validation`, `emergency_brake_valve_spad`), and action/pose-heavy workloads (stone pelting, child safety, vandalism, mobile phone usage).
2. **Remaining detector modalities (TensorRT + DeepStream)**  
   - Promote **face** and **action** detectors from simulation to model-backed inference.  
   - Wire engines exported via `models/*/export_trt.sh` (and stage under `models/usecases/`) so docker services pick them up automatically.
2. **Live ingest over RTSP/ONVIF**  
   - Validate `src/ingest_gst/pipeline.py` on Jetson (reconnects, FPS limiting, NVMM zero-copy).  
   - Confirm ONVIF time-sync and per-camera configs in `configs/cameras.yaml`.
3. **Tracking**  
   - ByteTrack-lite is in place; next step is wiring OSNet ReID and validating long-term ID stability across cameras/occlusions.
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
   - Resolve **all 40 placeholders** and commit only templates. Gate CI on `make placeholders:check`.

### P1 — Quality, safety, & ops
- **End-to-end tests on Xavier (AGX/NX)**: RTSP smoke (`tests/test_rtsp_connect.sh`) plus golden-event assertions for a few rulepacks.  
- **CI hardening**: Expand `.github/workflows/agent-ci.yml` to build container images and run headless tests; fail PRs on unresolved placeholders, lint, and mypy.  
- **Container baselines**: Ensure `nvcr.io/nvidia/l4t-base:35.4.1` aligns with the installed JetPack; pin DeepStream images.  
- **Deployment**: Validate `deploy/systemd/*.service` units on-device; confirm volumes (`/data/recordings`, `/data/exports`, logs) ownership and quota/retention.  
- **Security**: OAuth/OIDC proxy in front of UI, short‑lived JWTs, mTLS for events REST when used over WAN; secret scanning in CI.

### P2 — UX & docs
- **UI**: FastAPI endpoints for ROI editor, event browser, and toggles are now scaffolded (`src/aixavier/ui/`). Mount the router in your app or use the Compose service. Next: add frontend components and integrate with event pipeline.
- **Docs**: Flesh out `docs/SETUP.md`, `PRIVACY.md`, and `TROUBLESHOOT.md` with concrete JetPack/DeepStream versions and gotchas, and keep `docs/IMPLEMENTATION_STATUS.md`/`assets/usecases/catalog.yaml` in sync when the spreadsheet changes.  
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
- `tests/test_tracker.py` — SimpleTracker + ByteTrack-lite behaviours  
- `tests/test_tracker_manager.py` — TrackerManager (ByteTrack/simple lifecycle)  
- `tests/test_pose_assoc.py` — pose-to-person association logic  
- `tests/test_event_bus.py` — FileEventBus enqueue/persist  
- `tests/test_healthcheck.py` — ingest healthcheck success/failure  
- `tests/test_exporter.py` — pose event counting (auto-skips if `prometheus_client` missing)  
- `tests/test_detectors.py` — ONNX/TensorRT output normalisation (skipped unless `AIXAVIER_ENABLE_NUMPY_TESTS=1`)  
- `tests/test_perf.py` — metrics scrape parser  
- `tests/test_rtsp_connect.sh` — RTSP connectivity smoke  
(Overall test coverage is still low, but the most critical plumbing now has unit tests.)

## Quick “go / no‑go”
- **Go for demo**: You can run `make demo` locally and see synthetic events flow through the stack.  
- **No‑go for production**: Replace simulations, finalize privacy/recording, and resolve secrets before real deployments.

---

> See also `docs/IMPLEMENTATION_STATUS.md` for a condensed snapshot of services/models and `models/*/TODO.md` for per-use-case checklists.

_This file was generated by inspecting the repository snapshot only; no internet access or external builds were run._

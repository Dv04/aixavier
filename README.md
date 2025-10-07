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

## Runtime Profiles at a Glance
| Profile | Focus | FPS Target | Notable Intervals |
|---------|-------|------------|-------------------|
| `minimal` | Tamper + Trespass | 30 | Detectors on every frame. |
| `demo` | Eight representative use cases | 25 | Action detectors every 3 frames, face recognition every 2. |
| `all` | Full 22-rule workload | 25 | Per-use-case intervals in `configs/usecases/*.yaml`. |

Select a profile by exporting `PROFILE=<name>` or passing `PROFILE=...` to individual make targets. Compose profiles live under `docker-compose.yml`.

## System Overview
1. **Ingest (`src/ingest_gst/`)** – DeepStream-based RTSP/ONVIF ingestion with automatic reconnects, watermarks, and NVMM zero-copy paths.
2. **Runners (`src/runners/`)** – TensorRT engines (FP16 baseline, INT8 optional) grouped by modality: object, face, pose, action, smoke, and violence.
3. **Trackers (`src/trackers/`)** – BYTETrack with optional OSNet ReID features to maintain identities between frames.
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
- `models/` – TensorRT engine builders and calibration scripts.
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
_No agent run yet. Section will list recommended models once `src/agent` submits its first PR._
<!-- auto:end -->

<!-- auto:start name=performance-tuning -->
_No automated performance notes yet. Agent PRs update expected FPS, GPU util, and tuning tips._
<!-- auto:end -->

<!-- auto:start name=known-issues -->
_No known issues logged by agent. Track manual issues in the normal issue tracker._
<!-- auto:end -->

<!-- auto:start name=changelog -->
- 2025-10-07: Initial repository scaffold for Jetson Xavier railway CCTV analytics.
- 2025-10-07: Updated README to document bootstrap commands, module layout, and upcoming `src/aixavier/` migration.
<!-- auto:end -->

# Operations Guide (Troubleshooting + Performance)
_Date: 2025-11-20_

## Troubleshooting
- RTSP/ONVIF: `gst-launch-1.0 rtspsrc location=${CAMERA_RTSP_URL_01} ! decodebin ! fakesink`; verify ONVIF creds/time sync.
- Black frames: check `nvidia-l4t-gstreamer`; set `drop-on-late=0` in `ingest_gst/pipeline.conf`.
- Thermal: watch `tegrastats`; <80°C target; reduce action interval or enable camera downscale.
- MQTT: `mosquitto_sub -h {{MQTT_BROKER_HOST}} -t diagnostics/#`; inspect `events/logs/*.json` for failures.
- Placeholder linter: `make placeholders:check`; update `docs/placeholders.md` before rerun.
- Agent PR conflicts: agent works on `agent/update-YYYYMMDD`; mark manual sections with `<!-- manual -->`.

## Performance Tuning (DeepStream/RT)
- DeepStream knobs (Minimal / Demo / All):
  - primary-gie batch: 1 / 1 / 2
  - interval (object): 0 / 1 / 1
  - interval (face):   0 / 1 / 1
  - interval (action): 0 / 2 / 2
  - enable `nvbuf-memory-type=3`, `nvdsosd` GPU mode.
- TensorRT: prefer FP16; INT8 after calibration; `builder.max_workspace_size=2<<30` for large pose/action.
- CPU affinity: pin ingest/recorder to CPU0-1; detection/tracking CPU2-5; UI/agent CPU6-7.
- Thermal budget: soak with `tegrastats --interval 1000`.

## Expected Metrics (estimates; refresh with `make perf`)
- Tamper ~0.5 ms CPU; Trespass ~8 ms GPU; Unattended baggage ~4 ms GPU; Violence ~6 ms GPU; FRS ~3 ms GPU; Medical collapse ~5 ms GPU (per frame/clip as configured).
- Targets: ≥25 FPS per 1080p stream; GPU <85%, CPU <75% sustained.

## Benchmark Workflow
```bash
make perf
python tests/test_perf.py --endpoint http://localhost:9100/metrics --report artifacts/perf/latest.json
```
Capture temps alongside reports.

> Replaces `docs/TROUBLESHOOT.md` and the tuning portions of `docs/PERFORMANCE.md`.

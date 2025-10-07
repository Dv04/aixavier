# Troubleshooting

## RTSP / ONVIF
- Verify stream reachable: `gst-launch-1.0 rtspsrc location=${CAMERA_RTSP_URL_01} ! decodebin ! fakesink`
- If ONVIF discovery fails, confirm credentials `{{CAMERA_ONVIF_USER}}` / `{{CAMERA_ONVIF_PASS}}` and NTP sync.
- Use `tests/test_rtsp_connect.sh` for quick health probe.

## Black Frames / Decoder Issues
- Ensure Jetson multimedia packages installed. Run `dpkg -l | grep nvidia-l4t-gstreamer`.
- Enable `drop-on-late=0` in `ingest_gst/pipeline.conf` to avoid frame drops.

## Thermal Throttling
- Watch `tegrastats`; if GPU throttle, clean heatsink and reduce action detector interval.
- Consider dynamic tiler resolution (set `downscale: 0.5` in `configs/cameras.yaml`).

## MQTT Delivery
- Confirm broker accessible: `mosquitto_sub -h {{MQTT_BROKER_HOST}} -t diagnostics/#`.
- Use `events/logs/*.json` to inspect failed deliveries.

## Placeholder Linter Failures
- Run `make placeholders:check` for detailed output.
- Update `docs/placeholders.md` with new placeholders before re-running CI.

## Agent PR Conflicts
- Agent operates on branch `agent/update-YYYYMMDD`. If manual edits conflict, mark file sections inside `<!-- manual -->` blocks.


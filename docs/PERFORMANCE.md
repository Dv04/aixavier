# Performance

## Target
- Single 1080p H.265 RTSP stream per Xavier
- ≥25 FPS end-to-end with all 22 analytics active
- GPU utilization <85%, CPU <75% sustained

## DeepStream Tuning
| Parameter | Minimal | Demo | All |
|-----------|---------|------|-----|
| `primary-gie` batch size | 1 | 1 | 2 |
| `interval` (object) | 0 | 1 | 1 |
| `interval` (face) | 0 | 1 | 1 |
| `interval` (action)` | 0 | 2 | 2 |
| `nvinfer` tensor-meta` | off | on | on |

- Enable `nvbuf-memory-type=3` to keep NVMM buffers zero-copy.
- Use `nvdsosd` in GPU mode to reduce CPU load.

## TensorRT Knobs
- Favor FP16 (already exported); INT8 when calibration dataset ready.
- Set `builder.max_workspace_size = 2 << 30` for large pose/action models.
- For INT8, use per-channel quantization when supported.

## CPU Affinity & NUMA
- Pin ingest and recorder threads to CPU0-1 using `taskset` (configured in containers).
- Dedicate CPU2-5 to detection/tracking; CPU6-7 to UI/agent.

## Thermal Budget
- Use `tegrastats --interval 1000` during soak tests.
- If temps exceed 80 °C, reduce action detector interval or enable downscale in `configs/cameras.yaml`.

## Expected Metrics
| Use Case | Detector Interval | FPS Contribution | Notes |
|----------|-------------------|------------------|-------|
| Tamper | 1 | ~0.5 ms CPU | pure image stats |
| Trespass | 1 | 8 ms GPU | YOLO + tracker |
| Unattended baggage | 2 | 4 ms GPU | shares YOLO detections |
| Violence | 3 | 6 ms GPU | X3D clip inference |
| FRS | 2 | 3 ms GPU | SCRFD + embedding |
| Medical collapse | 3 | 5 ms GPU | pose velocity |

## Storage & Retention
- Default retention: `{{RETENTION_DAYS}}` days; adjust per camera in `configs/cameras.yaml`.
- Recorder prunes oldest clips nightly; metrics exported via `storage_bytes_used` gauge.

## Benchmark Workflow
```bash
make perf
python tests/test_perf.py --endpoint http://localhost:9100/metrics --report artifacts/perf/latest.json
```
Outputs CSV + HTML summary in `artifacts/perf/` for trend analysis.


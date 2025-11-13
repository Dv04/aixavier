
# Aixavier Day-0 Demo Patch

Adds demo-focused pieces for UC8 (collapse), UC20 (hand gestures), UC22 (phone usage).
Heuristics now; swap to ONNX models later with same interfaces.

## Synthetic demo loop

```bash
export AIX_ARTIFACTS=./artifacts_demo
python src/apps/demo_runner.py
# Watch events in $AIX_ARTIFACTS/events.jsonl
```

## Run tests

```bash
pytest -q
```

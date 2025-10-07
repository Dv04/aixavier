from __future__ import annotations

import argparse
import time
from pathlib import Path
from typing import Dict

import requests


def parse_metrics(text: str) -> Dict[str, float]:
    metrics: Dict[str, float] = {}
    for line in text.splitlines():
        if line.startswith("#") or not line.strip():
            continue
        if "{" in line:
            name, rest = line.split("{", 1)
            value = rest.split("}")[-1].strip()
        else:
            name, value = line.split(None, 1)
        try:
            metrics[name] = float(value)
        except ValueError:
            continue
    return metrics


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint", default="http://localhost:9100/metrics")
    parser.add_argument("--report", default="artifacts/perf/latest.json")
    args = parser.parse_args()

    for _ in range(3):
        try:
            response = requests.get(args.endpoint, timeout=2)
            response.raise_for_status()
            metrics = parse_metrics(response.text)
            Path(args.report).parent.mkdir(parents=True, exist_ok=True)
            Path(args.report).write_text(str(metrics), encoding="utf-8")
            print(metrics)
            return
        except Exception as exc:  # noqa: BLE001
            print(f"retry due to {exc}")
            time.sleep(1)
    raise SystemExit(1)


if __name__ == "__main__":
    main()

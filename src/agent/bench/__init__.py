from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass
class Benchmark:
    task: str
    model: str
    latency_ms: float
    accuracy: float
    vram_gb: float


def aggregate(records: List[dict]) -> List[Benchmark]:
    return [
        Benchmark(
            task=rec["task"],
            model=rec["model"],
            latency_ms=float(rec.get("latency_ms", 0.0)),
            accuracy=float(rec.get("accuracy", 0.0)),
            vram_gb=float(rec.get("vram_gb", 1.0)),
        )
        for rec in records
    ]

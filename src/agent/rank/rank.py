from __future__ import annotations

from typing import List


def _score(record: dict) -> float:
    latency = float(record.get("latency_fp16_ms") or record.get("latency_ms") or 1.0)
    accuracy = float(record.get("accuracy", 0.0))
    vram = float(record.get("vram_gb", 1.0))
    # Higher accuracy, lower latency/VRAM is better.
    return accuracy / (latency * (1.0 + vram * 0.1))


def rank_candidates(records: List[dict]) -> List[dict]:
    ranked = sorted(records, key=_score, reverse=True)
    for idx, rec in enumerate(ranked, start=1):
        rec["rank"] = idx
        rec["score"] = round(_score(rec), 6)
    return ranked

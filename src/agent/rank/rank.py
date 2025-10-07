from __future__ import annotations

from typing import List

from ..bench import aggregate


def rank_candidates(records: List[dict]) -> List[dict]:
    benchmarks = aggregate(records)
    ranked = sorted(benchmarks, key=lambda b: (b.latency_ms, -b.accuracy))
    return [b.__dict__ for b in ranked]

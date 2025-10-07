from __future__ import annotations

import logging
from typing import List

LOGGER = logging.getLogger("agent.scan")


class ModelScanner:
    """Dummy scanner placeholder. Replace with real web queries when network allowed."""

    def scan(self) -> List[dict]:
        LOGGER.info("Running offline scan (placeholder)")
        return [
            {
                "task": "object_detection",
                "model": "yolov8n",
                "source": "offline",
                "latency_ms": 8.0,
                "accuracy": 0.52,
            }
        ]

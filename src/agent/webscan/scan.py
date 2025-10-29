from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

LOGGER = logging.getLogger("agent.scan")


class ModelScanner:
    """Loads curated catalog data and prepares it for downstream ranking.

    In online mode this class can be extended to fetch remote benchmarks or
    scrape vendor release notes. The offline catalog keeps the automation
    reproductible inside CI while awaiting network approval.
    """

    def __init__(self, catalog_path: Path | None = None) -> None:
        self.catalog_path = catalog_path or Path(__file__).resolve().parent.parent / "data" / "catalog.json"

    def scan(self) -> Dict[str, Any]:
        if not self.catalog_path.exists():
            raise FileNotFoundError(f"Catalog file not found: {self.catalog_path}")
        LOGGER.info("Loading catalog data from %s", self.catalog_path)
        raw = json.loads(self.catalog_path.read_text(encoding="utf-8"))
        raw["scan_timestamp"] = datetime.now(timezone.utc).isoformat()
        return raw

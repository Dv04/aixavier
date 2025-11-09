from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional

import yaml


@dataclass(frozen=True)
class UseCaseDefinition:
    """Canonical metadata for a railway analytics use case."""

    id: int
    slug: str
    name: str
    description: str
    applicability: str
    deployment: str
    detectors: List[str]
    sensors: List[str]
    maturity: str

    def to_metadata(self) -> Dict[str, str]:
        return {
            "id": self.slug,
            "name": self.name,
            "description": self.description,
            "applicability": self.applicability,
            "deployment": self.deployment,
            "detectors": ", ".join(self.detectors),
            "sensors": ", ".join(self.sensors),
            "maturity": self.maturity,
        }


class UseCaseRegistry:
    """Loads the spreadsheet-backed manifest and exposes helper queries."""

    def __init__(
        self,
        manifest_path: Path | str = Path("assets/usecases/catalog.yaml"),
        configs_dir: Path | str = Path("configs/usecases"),
    ) -> None:
        self.manifest_path = Path(manifest_path)
        self.configs_dir = Path(configs_dir)
        self._definitions = self._load_manifest()
        self._by_slug = {definition.slug: definition for definition in self._definitions}

    def _load_manifest(self) -> List[UseCaseDefinition]:
        if not self.manifest_path.exists():
            raise FileNotFoundError(f"Use case manifest missing: {self.manifest_path}")
        payload = yaml.safe_load(self.manifest_path.read_text(encoding="utf-8")) or {}
        rows = payload.get("usecases", [])
        definitions: List[UseCaseDefinition] = []
        for row in rows:
            definitions.append(UseCaseDefinition(**row))
        return definitions

    @property
    def definitions(self) -> List[UseCaseDefinition]:
        return list(self._definitions)

    def get(self, slug: str) -> Optional[UseCaseDefinition]:
        return self._by_slug.get(slug)

    def missing_configs(self) -> List[str]:
        """Return slugs that do not yet have a YAML rule definition."""
        missing: List[str] = []
        for definition in self._definitions:
            if not (self.configs_dir / f"{definition.slug}.yaml").exists():
                missing.append(definition.slug)
        return missing

    def maturity_counts(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for definition in self._definitions:
            counts[definition.maturity] = counts.get(definition.maturity, 0) + 1
        return counts

    def enrich_metadata(self, slug: str, metadata: Optional[Dict[str, str]]) -> Dict[str, str]:
        """Merge manifest metadata with a config-specific metadata block."""
        enriched: Dict[str, str] = {}
        definition = self.get(slug)
        if definition:
            enriched.update(definition.to_metadata())
        if metadata:
            enriched.update(metadata)
        if "id" not in enriched:
            enriched["id"] = slug
        return enriched

    def to_report(self) -> Dict[str, object]:
        return {
            "total": len(self._definitions),
            "maturity": self.maturity_counts(),
            "missing_configs": self.missing_configs(),
        }


__all__ = ["UseCaseDefinition", "UseCaseRegistry"]

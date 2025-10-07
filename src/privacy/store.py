from __future__ import annotations

import base64
import hashlib
import json
import os
from pathlib import Path
from typing import Dict, Optional

from cryptography.fernet import Fernet


class EmbeddingStore:
    def __init__(self, path: Path, key_env: str = "SEC_EXPORT_ENCRYPTION_KEY") -> None:
        self.path = path
        self.path.parent.mkdir(parents=True, exist_ok=True)
        key_hex = os.getenv(key_env, "0" * 64)
        key_hex = (key_hex + "0" * 64)[:64]
        key_bytes = bytes.fromhex(key_hex)
        self.fernet = Fernet(base64.urlsafe_b64encode(key_bytes))
        if not self.path.exists():
            self.path.write_text(json.dumps({}), encoding="utf-8")

    def _load(self) -> Dict[str, str]:
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return data

    def _save(self, data: Dict[str, str]) -> None:
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def enroll(self, name: str, embedding: str) -> None:
        data = self._load()
        encrypted = self.fernet.encrypt(embedding.encode("utf-8")).decode("utf-8")
        data[name] = encrypted
        self._save(data)

    def match(self, embedding: str, threshold: float) -> Optional[Dict[str, float]]:
        data = self._load()
        target = hashlib.sha256(embedding.encode("utf-8")).hexdigest()
        for name, encrypted in data.items():
            decrypted = self.fernet.decrypt(encrypted.encode("utf-8")).decode("utf-8")
            candidate_hash = hashlib.sha256(decrypted.encode("utf-8")).hexdigest()
            score = _cosine_like(target, candidate_hash)
            if score >= threshold:
                return {"identity": name, "score": score}
        return None


def _cosine_like(a_hex: str, b_hex: str) -> float:
    matches = sum(1 for a, b in zip(a_hex, b_hex) if a == b)
    return matches / len(a_hex)


__all__ = ["EmbeddingStore"]

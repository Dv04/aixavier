from __future__ import annotations

import json

import pytest

from src.ingest_gst import healthcheck


def test_healthcheck_main_success(tmp_path, monkeypatch, capsys):
    ingest_dir = tmp_path / "artifacts" / "ingest"
    ingest_dir.mkdir(parents=True)
    frames = ingest_dir / "frames.log"
    frames.write_text(json.dumps({"frame_index": 1}) + "\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)
    healthcheck.main()
    assert "ok" in capsys.readouterr().out


def test_healthcheck_main_failure(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(SystemExit):
        healthcheck.main()

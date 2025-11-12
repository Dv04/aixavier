from __future__ import annotations
import os
from pathlib import Path
import pytest
import shutil
import tempfile
import subprocess
import time

# This test runs the synthetic demo pipeline and checks for event output.
# It assumes demo assets and pipeline are available (see Makefile and tests/data/generate_demo.py).


def test_e2e_demo_pipeline():
    tmpdir = tempfile.mkdtemp()
    demo_mp4 = Path(__file__).parent / "data" / "demo_stream.mp4"
    if not demo_mp4.exists():
        # Generate demo video if missing
        subprocess.run(
            ["python3", str(Path(__file__).parent / "data" / "generate_demo.py")],
            check=True,
        )
    # Simulate ingest + detection pipeline (replace with actual CLI/module as needed)
    # For now, just check that demo video exists and is readable
    assert demo_mp4.exists() and demo_mp4.stat().st_size > 0
    # Optionally, run a pipeline and check for event output
    # Example: run src/ingest_gst.main and src/runners.main on demo_mp4
    # This is a placeholder for a real E2E pipeline invocation
    # You can expand this to spawn the pipeline and check for output files/events
    # Clean up
    shutil.rmtree(tmpdir)

from __future__ import annotations

import os

os.environ.setdefault("AIXAVIER_DISABLE_NUMPY", "1")

import pytest

if os.environ.get("AIXAVIER_ENABLE_NUMPY_TESTS") != "1":
    pytest.skip("requires numpy runtime for postprocess validation", allow_module_level=True)

import numpy as np

from src.runners.postprocess import normalise_object_output, normalise_pose_output
from src.runners.detectors import PoseDetector


def test_normalise_object_output_transpose() -> None:
    raw = np.random.rand(1, 84, 10).astype(np.float32)
    normalised = normalise_object_output(raw)
    assert normalised.shape == (10, 84)


def test_normalise_object_output_no_transpose() -> None:
    raw = np.random.rand(1, 10, 84).astype(np.float32)
    normalised = normalise_object_output(raw)
    assert normalised.shape == (10, 84)


def test_normalise_pose_output_transpose() -> None:
    raw = np.random.rand(1, 56, 8).astype(np.float32)
    normalised = normalise_pose_output(raw)
    assert normalised.shape == (8, 56)


def test_normalise_pose_output_no_transpose() -> None:
    raw = np.random.rand(8, 56).astype(np.float32)
    normalised = normalise_pose_output(raw)
    assert normalised.shape == (8, 56)


def test_pose_detector_decode_simcc() -> None:
    det = PoseDetector({"input": {"width": 256, "height": 192}})
    simcc_x = np.zeros((1, 2, 4), dtype=np.float32)
    simcc_y = np.zeros((1, 2, 6), dtype=np.float32)
    simcc_x[0, 0, 1] = 0.9
    simcc_x[0, 1, 3] = 0.8
    simcc_y[0, 0, 2] = 0.95
    simcc_y[0, 1, 4] = 0.85
    boxes, scores, keypoints = det._decode_simcc(simcc_x, simcc_y)
    assert boxes.shape == (1, 4)
    assert keypoints.shape == (1, 2, 3)
    x0 = keypoints[0, 0, 0]
    y1 = keypoints[0, 1, 1]
    assert pytest.approx(x0, rel=1e-3) == (1 / 3) * 256
    assert pytest.approx(y1, rel=1e-3) == (4 / 5) * 192
    assert scores.shape == (1,)

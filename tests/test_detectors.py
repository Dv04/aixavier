from __future__ import annotations

import os

os.environ.setdefault("AIXAVIER_DISABLE_NUMPY", "1")

import pytest

if os.environ.get("AIXAVIER_ENABLE_NUMPY_TESTS") != "1":
    pytest.skip("requires numpy runtime for postprocess validation", allow_module_level=True)

import numpy as np

from runners.postprocess import normalise_object_output, normalise_pose_output


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

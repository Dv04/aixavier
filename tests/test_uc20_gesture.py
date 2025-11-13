import numpy as np

from src.models.gesture import GestureModel


def test_uc20_halt_when_right_wrist_high() -> None:
    keypoints = np.zeros((17, 2), dtype=float)
    keypoints[10] = [100, 50]
    keypoints[6] = [100, 100]
    label, score = GestureModel().predict(keypoints)
    assert label == "halt" and score >= 0.6

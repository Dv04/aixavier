import numpy as np

from src.models.phone import PhoneUsage


def test_uc22_phone_usage_triggers_after_dwell() -> None:
    model = PhoneUsage(hand_to_ear_px=50, dwell_s=0.3, fps=10)
    keypoints = np.zeros((17, 2), dtype=float)
    keypoints[10] = [100, 100]
    keypoints[4] = [110, 100]
    fired = False
    for _ in range(5):
        score, active = model.score(keypoints)
        if active:
            fired = True
    assert fired
    assert score >= 0.7

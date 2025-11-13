
import numpy as np
from src.models.phone import PhoneUsage

def test_uc22_phone_usage_triggers_after_dwell():
    p = PhoneUsage(hand_to_ear_px=50, dwell_s=0.3, fps=10)
    kps = np.zeros((17,2), dtype=float)
    idx = {"right_wrist": 10, "right_ear": 4}
    kps[idx["right_wrist"]] = [100,100]
    kps[idx["right_ear"]]   = [110,100]
    fired = False
    for _ in range(5):
        score, active = p.score(kps)
        if active: fired = True
    assert fired

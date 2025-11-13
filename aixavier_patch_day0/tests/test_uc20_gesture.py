
import numpy as np
from src.models.gesture import GestureModel

def test_uc20_halt_when_right_wrist_high():
    kps = np.zeros((17,2), dtype=float)
    kps[10] = [100, 50]
    kps[6] = [100, 100]
    label, score = GestureModel().predict(kps)
    assert label == 'halt' and score >= 0.6

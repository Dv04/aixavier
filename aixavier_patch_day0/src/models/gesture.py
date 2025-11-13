
import numpy as np

class GestureModel:
    LABELS = ("unknown","halt","proceed","reverse","caution")
    def __init__(self): pass

    @staticmethod
    def _y(kps, idx): return float(kps[idx][1])

    def predict(self, kps: np.ndarray):
        try:
            rw, rs = self._y(kps, 10), self._y(kps, 6)  # right_wrist, right_shoulder
            lw, ls = self._y(kps, 9),  self._y(kps, 5)  # left_wrist, left_shoulder
        except Exception:
            return ("unknown", 0.0)
        if rw < rs - 10: return ("halt", 0.8)
        if lw < ls - 10: return ("proceed", 0.7)
        return ("unknown", 0.1)

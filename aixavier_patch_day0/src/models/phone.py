
import numpy as np

def dist(a,b): 
    ax,ay=a; bx,by=b; return ((ax-bx)**2 + (ay-by)**2) ** 0.5

class PhoneUsage:
    def __init__(self, hand_to_ear_px=80, dwell_s=2.0, fps=15):
        self.hand_to_ear_px = hand_to_ear_px
        self.dwell_frames = int(dwell_s * fps)
        self._counter = 0

    def score(self, kps: np.ndarray):
        idx = {"right_wrist": 10, "right_ear": 4, "left_wrist": 9, "left_ear": 3}
        try:
            r = dist(kps[idx["right_wrist"]], kps[idx["right_ear"]])
            l = dist(kps[idx["left_wrist"]],  kps[idx["left_ear"]])
        except Exception:
            return (0.0, False)
        near = (r < self.hand_to_ear_px) or (l < self.hand_to_ear_px)
        self._counter = self._counter + 1 if near else 0
        if self._counter >= self.dwell_frames:
            return (0.7, True)
        return (0.2 if near else 0.0, False)

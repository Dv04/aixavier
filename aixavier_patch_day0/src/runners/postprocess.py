
import numpy as np

def ema(prev, cur, alpha=0.4):
    if prev is None:
        return cur
    return alpha * cur + (1 - alpha) * prev

class KeypointSmoother:
    def __init__(self, alpha=0.4):
        self.alpha = alpha
        self.prev = None

    def __call__(self, kps: np.ndarray):
        self.prev = ema(self.prev, kps, self.alpha)
        return self.prev


import threading

class Telemetry:
    def __init__(self):
        self._lock = threading.Lock()
        self.speed_kmph = 0.0
        self.door_open = False
        self.gps = None

    def snapshot(self):
        with self._lock:
            return {
                "speed_kmph": float(self.speed_kmph),
                "door_open": bool(self.door_open),
                "gps": self.gps,
            }

    def set_speed(self, v):
        with self._lock:
            self.speed_kmph = float(v)

    def set_door(self, open_: bool):
        with self._lock:
            self.door_open = bool(open_)

import threading
from typing import Any, Dict


class Telemetry:
    """Thread-safe telemetry snapshot for demo workloads."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self._snapshot: Dict[str, Any] = {
            "speed_kmph": 0.0,
            "door_open": False,
            "gps": None,
        }

    def snapshot(self) -> Dict[str, Any]:
        with self._lock:
            return dict(self._snapshot)

    def set_speed(self, value: float) -> None:
        with self._lock:
            self._snapshot["speed_kmph"] = float(value)

    def set_door(self, open_: bool) -> None:
        with self._lock:
            self._snapshot["door_open"] = bool(open_)

    def set_gps(self, gps: Any) -> None:
        with self._lock:
            self._snapshot["gps"] = gps

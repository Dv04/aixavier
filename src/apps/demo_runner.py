"""Synthetic loop emitting demo events for pose-based use cases."""

from __future__ import annotations

import os
import random
import time
from pathlib import Path

from src.common.event_bus import Event, FileEventBus
from src.models.collapse import CollapseModel
from src.models.gesture import GestureModel
from src.models.phone import PhoneUsage
from src.telemetry.ingest import Telemetry


def _fake_pose_sequence(length: int = 180, width: int = 640, height: int = 360):
    keypoints = [[width * 0.5, height * 0.5] for _ in range(17)]
    for frame in range(length):
        for idx in range(17):
            keypoints[idx][0] += random.uniform(-0.6, 0.6)
            keypoints[idx][1] += random.uniform(-0.6, 0.6)
        if 40 <= frame <= 50:
            keypoints[11][1] += 8.0
            keypoints[12][1] += 8.0
        if 51 <= frame <= 70:
            for idx in (0, 1, 2, 3, 4, 5, 6, 11, 12):
                keypoints[idx][1] = min(height - 5, keypoints[idx][1] + 4.5)
        yield [[float(x), float(y)] for x, y in keypoints]


def run_demo(out_dir: Path, fps: int = 15) -> None:
    bus = FileEventBus(out_dir)
    telemetry = Telemetry()
    collapse_model = CollapseModel(onnx_path=None)
    gesture_model = GestureModel()
    phone_model = PhoneUsage(fps=fps)

    feature_ring: list[dict[str, float]] = []
    previous_midhip: tuple[float, float] | None = None

    for keypoints in _fake_pose_sequence():
        midhip = (
            (keypoints[11][0] + keypoints[12][0]) / 2.0,
            (keypoints[11][1] + keypoints[12][1]) / 2.0,
        )
        if previous_midhip is None:
            velocity = 0.0
            accel = 0.0
        else:
            velocity = (
                (midhip[0] - previous_midhip[0]) ** 2
                + (midhip[1] - previous_midhip[1]) ** 2
            ) ** 0.5 * fps
            accel = velocity - feature_ring[-1]["v_mag"] if feature_ring else 0.0
        previous_midhip = midhip
        bbox_height = (
            max(
                1.0,
                abs(keypoints[0][1] - ((keypoints[11][1] + keypoints[12][1]) / 2.0)),
            )
            * 2.0
        )
        features = {"v_mag": velocity, "a_mag": accel, "prone_height_px": bbox_height}
        feature_ring.append(features)
        if len(feature_ring) > 90:
            feature_ring.pop(0)

        collapse_score = (
            collapse_model.score(feature_ring[-15:]) if len(feature_ring) >= 15 else 0.0
        )
        if collapse_score >= 0.65:
            bus.publish(
                Event(
                    "pose.collapse", {"score": collapse_score, "prone_px": bbox_height}
                )
            )

        label, gesture_score = gesture_model.predict(keypoints)
        if gesture_score >= 0.6 and label != "unknown":
            bus.publish(Event("pose.gesture", {"label": label, "score": gesture_score}))

        phone_score, active = phone_model.score(keypoints)
        if active:
            bus.publish(Event("pose.phone_usage", {"score": phone_score}))

        telemetry.set_speed(random.uniform(0, 15))
        time.sleep(1.0 / fps)


def main() -> int:
    out_dir = Path(os.environ.get("AIX_ARTIFACTS", "./artifacts")).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    run_demo(out_dir=out_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

# YOLO ONNX Exports

Place the ONNX versions of your YOLO detectors here (e.g., `yolov11n.onnx`, `yolov10n.onnx`). The detector runner will prefer these exports when TensorRT engines are unavailable, allowing CPU inference via `onnxruntime` for local testing.

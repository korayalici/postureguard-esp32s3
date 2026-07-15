"""Export the trained Keras posture model to TensorFlow Lite.

Reads the SavedModel produced by `train.py --nn` and writes a .tflite file.
With --int8, applies full-integer quantization using the processed windows
as the representative dataset (required for best TFLite Micro performance
on the ESP32-S3).

After export, convert to a C array for firmware/model/ with:
    python -c "print(open('posture_model.tflite','rb').read().hex())"  # or
    xxd -i posture_model.tflite > posture_model.h   (Git Bash / WSL)

Usage:
    python export_tflite.py --model-dir .\\artifacts\\training --output .\\artifacts\\model\\posture_model.tflite
    python export_tflite.py --model-dir .\\artifacts\\training --output .\\artifacts\\model\\posture_model_int8.tflite --int8 --processed .\\artifacts\\processed
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--model-dir", type=Path, required=True,
                        help="Training artifacts dir containing saved_model/ (from train.py --nn).")
    parser.add_argument("--output", type=Path, required=True,
                        help="Path for the exported .tflite file.")
    parser.add_argument("--int8", action="store_true",
                        help="Apply full-integer (int8) quantization.")
    parser.add_argument("--processed", type=Path,
                        help="Processed data dir (windows.npz) for the int8 representative dataset.")
    return parser


def representative_dataset(model_dir: Path, processed: Path):
    """Yield normalized windows so the converter can calibrate int8 ranges."""
    data = np.load(processed / "windows.npz", allow_pickle=False)
    norm = np.load(model_dir / "normalization.npz")
    windows = data["windows"].astype(np.float32)
    n = windows.shape[0]
    X = windows.reshape(n, -1)
    X = (X - norm["mean"]) / norm["std"]
    for i in range(min(n, 200)):
        yield [X[i:i + 1].astype(np.float32)]


def main() -> int:
    args = build_parser().parse_args()
    saved_model = args.model_dir / "saved_model"
    if not saved_model.exists():
        raise FileNotFoundError(
            f"{saved_model} not found. Run `python train.py --nn` first — "
            "no neural network has been trained yet.")
    if args.int8 and not args.processed:
        raise SystemExit("--int8 requires --processed (for the representative dataset).")

    import tensorflow as tf  # lazy import: heavy

    converter = tf.lite.TFLiteConverter.from_saved_model(str(saved_model))
    if args.int8:
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        converter.representative_dataset = lambda: representative_dataset(
            args.model_dir, args.processed)
        converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
        converter.inference_input_type = tf.int8
        converter.inference_output_type = tf.int8

    tflite_model = converter.convert()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(tflite_model)

    size_kb = len(tflite_model) / 1024
    print(f"Wrote {args.output.resolve()} ({size_kb:.1f} KB, int8={args.int8})")
    print("Next: convert to a C array and place it in firmware/model/.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

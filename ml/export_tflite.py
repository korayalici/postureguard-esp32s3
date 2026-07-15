"""Starter export stub for converting a trained model to TFLite."""

from __future__ import annotations

import argparse
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Export a trained posture model to TensorFlow Lite format."
    )
    parser.add_argument(
        "--model-dir",
        type=Path,
        required=True,
        help="Directory containing the trained model artifacts.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Path for the exported .tflite file.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    if not args.model_dir.exists():
        raise FileNotFoundError(f"Model directory not found: {args.model_dir}")

    args.output.parent.mkdir(parents=True, exist_ok=True)

    print("PostureGuard TFLite export stub")
    print(f"Model directory: {args.model_dir.resolve()}")
    print(f"Output file:     {args.output.resolve()}")
    print("TODO:")
    print("- Load the saved training artifact.")
    print("- Convert the model with TensorFlow Lite tools.")
    print("- Validate model size and inference compatibility.")
    print("- Move the exported file into firmware/model as needed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

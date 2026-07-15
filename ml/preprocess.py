"""Starter preprocessing stub for PostureGuard sensor data."""

from __future__ import annotations

import argparse
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Prepare labeled BMI270 sensor samples for posture model training."
    )
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Directory containing raw or sample CSV recordings.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Directory where processed windows will be written.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    if not args.input.exists():
        raise FileNotFoundError(f"Input directory not found: {args.input}")

    args.output.mkdir(parents=True, exist_ok=True)

    print("PostureGuard preprocessing stub")
    print(f"Input directory:  {args.input.resolve()}")
    print(f"Output directory: {args.output.resolve()}")
    print("TODO:")
    print("- Define CSV schema for BMI270 recordings.")
    print("- Segment signals into 2 s windows at 50 Hz.")
    print("- Attach labels for upright, slouch, and lean.")
    print("- Save processed features for training.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Starter training stub for PostureGuard posture classification."""

from __future__ import annotations

import argparse
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Train a baseline posture classifier from processed windows."
    )
    parser.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Directory containing processed training data.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Directory where model artifacts and logs will be saved.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()

    if not args.input.exists():
        raise FileNotFoundError(f"Processed data directory not found: {args.input}")

    args.output.mkdir(parents=True, exist_ok=True)

    print("PostureGuard training stub")
    print(f"Training data: {args.input.resolve()}")
    print(f"Artifacts dir: {args.output.resolve()}")
    print("TODO:")
    print("- Load processed windows and labels.")
    print("- Split data into train/validation sets.")
    print("- Train an initial lightweight model.")
    print("- Record honest metrics in docs/results.md.")
    print("- Save the model in a format suitable for TFLite export.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Starter serial-recording stub for future M5StickS3 data capture."""

from __future__ import annotations

import argparse
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Record sensor lines from a serial device into a local file."
    )
    parser.add_argument(
        "--port",
        default="COM3",
        help="Serial port placeholder, for example COM3 on Windows.",
    )
    parser.add_argument(
        "--baud",
        type=int,
        default=115200,
        help="Expected baud rate placeholder.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="Destination file for captured serial lines.",
    )
    return parser


def main() -> int:
    args = build_parser().parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)

    print("PostureGuard serial capture stub")
    print(f"Port:   {args.port}")
    print(f"Baud:   {args.baud}")
    print(f"Output: {args.output.resolve()}")
    print("TODO:")
    print("- Add pyserial-based device connection.")
    print("- Define the firmware serial packet format.")
    print("- Timestamp and store incoming BMI270 samples.")
    print("- Add label entry support during recording.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Record labeled IMU CSV lines from the M5StickS3 over serial.

Expects the firmware (Phase B) to stream one CSV line per BMI270 sample:
    timestamp_ms,ax,ay,az,gx,gy,gz

This script appends the current label and writes the full training schema:
    timestamp_ms,ax,ay,az,gx,gy,gz,label

Keyboard controls while recording:
    u -> label following samples "upright"
    s -> label following samples "slouch"
    l -> label following samples "lean"
    q -> stop and save

Requires: pip install pyserial

Usage:
    python record_serial.py --port COM3 --output ..\\data\\raw\\session_01.csv
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

HEADER = "timestamp_ms,ax,ay,az,gx,gy,gz,label"
KEY_TO_LABEL = {"u": "upright", "s": "slouch", "l": "lean"}


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--port", required=True, help="Serial port, e.g. COM3")
    parser.add_argument("--baud", type=int, default=115200)
    parser.add_argument("--output", type=Path, required=True,
                        help="Destination CSV (one session per file).")
    return parser


def read_key_nonblocking() -> str | None:
    """Return a pressed key without blocking (Windows)."""
    import msvcrt
    if msvcrt.kbhit():
        return msvcrt.getwch().lower()
    return None


def main() -> int:
    args = build_parser().parse_args()
    try:
        import serial
    except ImportError:
        print("pyserial is not installed. Run: pip install pyserial", file=sys.stderr)
        return 1

    if args.output.exists():
        print(f"Refusing to overwrite existing {args.output}", file=sys.stderr)
        return 1
    args.output.parent.mkdir(parents=True, exist_ok=True)

    label = "upright"
    lines_written = 0
    print(f"Opening {args.port} @ {args.baud}. Keys: u/s/l set label, q quits.")
    print(f"Starting label: {label}")

    with serial.Serial(args.port, args.baud, timeout=1) as ser, \
            args.output.open("w", newline="") as f:
        f.write(HEADER + "\n")
        while True:
            key = read_key_nonblocking()
            if key == "q":
                break
            if key in KEY_TO_LABEL:
                label = KEY_TO_LABEL[key]
                print(f"Label -> {label}")

            raw = ser.readline().decode("ascii", errors="ignore").strip()
            if not raw:
                continue
            parts = raw.split(",")
            if len(parts) != 7:
                continue  # skip boot noise / partial lines
            try:
                [float(p) for p in parts]
            except ValueError:
                continue
            f.write(f"{raw},{label}\n")
            lines_written += 1
            if lines_written % 250 == 0:
                print(f"{lines_written} samples ({label})")

    print(f"Saved {lines_written} samples to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

"""Preprocess labeled IMU session CSVs into training windows and features.

Input: a directory of session CSVs, one file per recording session, with columns:
    timestamp_ms, ax, ay, az, gx, gy, gz, label

Each row is one BMI270 sample. `label` is one of: upright, slouch, lean.
The session ID is taken from the file name (stem), so hold-out splits can be
done per session rather than per row.

Output (in --output directory):
    features.csv   one row per window: session, label, and per-channel stats
    windows.npz    raw windows (float32) + labels + sessions, for NN training

Usage:
    python preprocess.py --input ..\\data\\sample --output .\\artifacts\\processed
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

SAMPLE_RATE_HZ = 50
WINDOW_SECONDS = 2.0
WINDOW_SIZE = int(SAMPLE_RATE_HZ * WINDOW_SECONDS)  # 100 samples
WINDOW_STRIDE = WINDOW_SIZE // 2  # 50% overlap

CHANNELS = ["ax", "ay", "az", "gx", "gy", "gz"]
LABELS = ["upright", "slouch", "lean"]
REQUIRED_COLUMNS = ["timestamp_ms", *CHANNELS, "label"]


def load_session(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"{csv_path.name}: missing columns {missing}")
    unknown = set(df["label"].unique()) - set(LABELS)
    if unknown:
        raise ValueError(f"{csv_path.name}: unknown labels {sorted(unknown)}")
    return df.sort_values("timestamp_ms").reset_index(drop=True)


def window_session(df: pd.DataFrame):
    """Yield (window_array, label) for each full window with a single label."""
    values = df[CHANNELS].to_numpy(dtype=np.float32)
    labels = df["label"].to_numpy()
    for start in range(0, len(df) - WINDOW_SIZE + 1, WINDOW_STRIDE):
        end = start + WINDOW_SIZE
        window_labels = set(labels[start:end])
        if len(window_labels) != 1:
            continue  # skip windows that span a label transition
        yield values[start:end], window_labels.pop()


def window_features(window: np.ndarray) -> dict:
    """Simple per-channel statistics; a solid baseline before trying a NN."""
    feats: dict = {}
    for i, ch in enumerate(CHANNELS):
        col = window[:, i]
        feats[f"{ch}_mean"] = float(col.mean())
        feats[f"{ch}_std"] = float(col.std())
        feats[f"{ch}_min"] = float(col.min())
        feats[f"{ch}_max"] = float(col.max())
        feats[f"{ch}_rms"] = float(np.sqrt(np.mean(col**2)))
    acc_mag = np.linalg.norm(window[:, :3], axis=1)
    feats["acc_mag_mean"] = float(acc_mag.mean())
    feats["acc_mag_std"] = float(acc_mag.std())
    return feats


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", type=Path, required=True,
                        help="Directory containing session CSV files.")
    parser.add_argument("--output", type=Path, required=True,
                        help="Directory for features.csv and windows.npz.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    csv_files = sorted(args.input.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {args.input}")

    rows, windows, window_labels, window_sessions = [], [], [], []
    for csv_path in csv_files:
        session = csv_path.stem
        df = load_session(csv_path)
        count = 0
        for window, label in window_session(df):
            feats = window_features(window)
            feats["session"] = session
            feats["label"] = label
            rows.append(feats)
            windows.append(window)
            window_labels.append(label)
            window_sessions.append(session)
            count += 1
        print(f"{csv_path.name}: {len(df)} samples -> {count} windows")

    if not rows:
        raise ValueError("No complete single-label windows produced. "
                         f"Each session needs >= {WINDOW_SIZE} samples per label.")

    args.output.mkdir(parents=True, exist_ok=True)
    features = pd.DataFrame(rows)
    features.to_csv(args.output / "features.csv", index=False)
    np.savez_compressed(
        args.output / "windows.npz",
        windows=np.stack(windows),
        labels=np.array(window_labels),
        sessions=np.array(window_sessions),
    )

    print(f"\nWrote {len(features)} windows from {len(csv_files)} sessions")
    print(f"  {args.output / 'features.csv'}")
    print(f"  {args.output / 'windows.npz'}")
    print("Label counts:", features["label"].value_counts().to_dict())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

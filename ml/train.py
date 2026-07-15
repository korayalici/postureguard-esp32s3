"""Train a posture classifier with a session-based hold-out split.

Trains a RandomForest baseline on window features. With --nn, also trains a
small Keras MLP on raw windows (the model that will be exported to TFLite).

The split is per session (GroupShuffleSplit on session IDs), never per row,
so windows from the same recording never leak across train/test.

Metrics are written to the artifacts directory. Copy them into
docs/results.md manually only after running on REAL device data —
keep results.md as TBD until then.

Usage:
    python train.py --input .\\artifacts\\processed --output .\\artifacts\\training
    python train.py --input .\\artifacts\\processed --output .\\artifacts\\training --nn
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import GroupShuffleSplit

LABELS = ["upright", "slouch", "lean"]
TEST_FRACTION = 0.34
RANDOM_SEED = 42


def session_split(sessions: np.ndarray):
    """Split window indices so no session appears in both train and test."""
    unique = np.unique(sessions)
    if len(unique) < 2:
        raise ValueError(
            f"Need >= 2 sessions for a session-based hold-out, got {len(unique)}. "
            "Record more sessions before trusting any metrics."
        )
    splitter = GroupShuffleSplit(n_splits=1, test_size=TEST_FRACTION,
                                 random_state=RANDOM_SEED)
    train_idx, test_idx = next(splitter.split(sessions, groups=sessions))
    return train_idx, test_idx


def evaluate(name: str, y_true, y_pred, out_dir: Path) -> dict:
    acc = accuracy_score(y_true, y_pred)
    cm = confusion_matrix(y_true, y_pred, labels=LABELS)
    report = classification_report(y_true, y_pred, labels=LABELS, zero_division=0)

    print(f"\n=== {name} ===")
    print(f"Hold-out accuracy: {acc:.3f}")
    print("Confusion matrix (rows=true, cols=pred, order=" + ",".join(LABELS) + "):")
    print(cm)
    print(report)

    metrics = {"model": name, "accuracy": round(float(acc), 4),
               "labels": LABELS, "confusion_matrix": cm.tolist()}
    (out_dir / f"metrics_{name}.json").write_text(json.dumps(metrics, indent=2))
    (out_dir / f"report_{name}.txt").write_text(report)
    return metrics


def train_baseline(features_csv: Path, out_dir: Path) -> dict:
    df = pd.read_csv(features_csv)
    sessions = df["session"].to_numpy()
    y = df["label"].to_numpy()
    X = df.drop(columns=["session", "label"]).to_numpy()

    train_idx, test_idx = session_split(sessions)
    print(f"Baseline: train sessions {sorted(set(sessions[train_idx]))}, "
          f"test sessions {sorted(set(sessions[test_idx]))}")

    clf = RandomForestClassifier(n_estimators=100, random_state=RANDOM_SEED)
    clf.fit(X[train_idx], y[train_idx])
    return evaluate("random_forest", y[test_idx], clf.predict(X[test_idx]), out_dir)


def train_nn(windows_npz: Path, out_dir: Path) -> dict:
    import tensorflow as tf  # lazy import: heavy, only needed for --nn

    data = np.load(windows_npz, allow_pickle=False)
    windows = data["windows"].astype(np.float32)
    labels = data["labels"]
    sessions = data["sessions"]

    n, timesteps, channels = windows.shape
    X = windows.reshape(n, timesteps * channels)
    label_to_idx = {name: i for i, name in enumerate(LABELS)}
    y = np.array([label_to_idx[str(v)] for v in labels])

    train_idx, test_idx = session_split(sessions)

    # Normalize with train statistics only; firmware must apply the same values.
    mean = X[train_idx].mean(axis=0)
    std = X[train_idx].std(axis=0) + 1e-6
    X = (X - mean) / std

    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(timesteps * channels,)),
        tf.keras.layers.Dense(32, activation="relu"),
        tf.keras.layers.Dense(16, activation="relu"),
        tf.keras.layers.Dense(len(LABELS), activation="softmax"),
    ])
    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy",
                  metrics=["accuracy"])
    model.fit(X[train_idx], y[train_idx], epochs=30, batch_size=16, verbose=0)

    y_pred_idx = np.argmax(model.predict(X[test_idx], verbose=0), axis=1)
    idx_to_label = {i: name for name, i in label_to_idx.items()}
    y_true = [idx_to_label[i] for i in y[test_idx]]
    y_pred = [idx_to_label[i] for i in y_pred_idx]
    metrics = evaluate("keras_mlp", y_true, y_pred, out_dir)

    model.export(str(out_dir / "saved_model"))
    model.save(out_dir / "model.keras")
    np.savez(out_dir / "normalization.npz", mean=mean, std=std)
    print(f"Saved Keras model + normalization stats to {out_dir}")
    return metrics


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", type=Path, required=True,
                        help="Directory with features.csv / windows.npz from preprocess.py")
    parser.add_argument("--output", type=Path, required=True,
                        help="Directory for metrics and model artifacts.")
    parser.add_argument("--nn", action="store_true",
                        help="Also train the small Keras MLP for TFLite export.")
    return parser


def main() -> int:
    args = build_parser().parse_args()
    features_csv = args.input / "features.csv"
    if not features_csv.exists():
        raise FileNotFoundError(f"{features_csv} not found. Run preprocess.py first.")

    args.output.mkdir(parents=True, exist_ok=True)
    train_baseline(features_csv, args.output)
    if args.nn:
        train_nn(args.input / "windows.npz", args.output)

    print(f"\nArtifacts written to {args.output.resolve()}")
    print("NOTE: update docs/results.md only with metrics from REAL device data.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

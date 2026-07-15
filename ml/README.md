# ML pipeline

Offline training pipeline for the PostureGuard posture classifier
(3 classes: `upright`, `slouch`, `lean`).

## Design

- **Windowing:** 50 Hz × 2 s = 100 samples/window, 50% overlap
- **Split:** session-based hold-out (`GroupShuffleSplit` on session IDs) —
  windows from one recording never appear in both train and test
- **Models:** RandomForest baseline on window statistics; small Keras MLP on
  raw windows for TFLite export (train with `--nn`)

## Setup

> Note: install the venv at a short path (e.g. `C:\Users\<you>\.venvs\pg`) —
> TensorFlow's install can fail at deep paths on Windows without long-path support.

```powershell
python -m venv $env:USERPROFILE\.venvs\pg
& $env:USERPROFILE\.venvs\pg\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Run (from `ml/`)

```powershell
python preprocess.py --input ..\data\sample --output .\artifacts\processed
python train.py --input .\artifacts\processed --output .\artifacts\training --nn
python export_tflite.py --model-dir .\artifacts\training --output .\artifacts\model\posture_model_int8.tflite --int8 --processed .\artifacts\processed
```

## Honesty notes

- `data/sample/` currently contains **synthetic** data for smoke-testing only.
  Metrics from it mean nothing about real posture performance.
- `docs/results.md` stays TBD until training runs on real M5StickS3 recordings
  with a session-based split.
- `artifacts/` is a local working directory; do not commit it.

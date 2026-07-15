# Data

Posture datasets for PostureGuard.

## CSV schema (one file per recording session)

| Column | Type | Description |
| --- | --- | --- |
| `timestamp_ms` | int | Milliseconds since recording start |
| `ax`, `ay`, `az` | float | BMI270 accelerometer (g) |
| `gx`, `gy`, `gz` | float | BMI270 gyroscope (dps) |
| `label` | str | `upright`, `slouch`, or `lean` |

The session ID is the file name (stem). Keep one session per file so
training can use a session-based hold-out split.

## Directories

- `sample/` — tiny committed files only.
  **Current contents are SYNTHETIC** (`synthetic_session_*.csv`), generated
  purely to smoke-test the ML pipeline. They are NOT real posture recordings
  and no metrics derived from them are meaningful.
- `raw/` — real device recordings; git-ignored (create locally). Use
  `scripts/record_serial.py` once the M5StickS3 firmware streams IMU CSV.

Do not commit private or sensitive recordings.

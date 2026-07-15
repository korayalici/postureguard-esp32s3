# Design notes

## Target hardware

- **Board:** M5StickS3
- **MCU:** ESP32-S3
- **Sensor:** BMI270

## Proposed signal pipeline

- **Sampling rate:** 50 Hz
- **Window length:** 2 seconds
- **Classes:** upright, slouch, lean

## End-to-end workflow

1. Collect labeled IMU data from the wearable.
2. Preprocess and window the data for training.
3. Train a lightweight posture classifier.
4. Export the model to TensorFlow Lite.
5. Convert or package it for TensorFlow Lite Micro.
6. Flash the firmware to the M5StickS3 for on-device inference.

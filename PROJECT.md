# PROJECT BRIEF — PostureGuard (edge-posture-monitor)

You are helping me build this project end-to-end. Follow this brief exactly. Prefer small, working steps over big unfinished rewrites. Never invent results, accuracy numbers, or "completed" features that do not exist yet.

---

## 1. Who I am

- Name: Koray Alici
- Student: Computer Engineering (Honors), Texas Tech University, expected graduation Dec 2027
- Background: Summer 2025 research internship at Aoyama Gakuin University (Tokyo) — wearable posture monitoring with M5StickC Plus 2 + IMU + Python analysis
- Goal: Turn that research into a strong, public GitHub portfolio project for firmware / embedded / edge-ML internships
- Hardware I ordered: **M5StickS3** (ESP32-S3-PICO, 8MB Flash, 8MB PSRAM, BMI270 IMU, screen, battery) — arriving in ~10–20 business days
- Related later project (separate): STM32 Nucleo-F446RE + SparkFun BNO086 for FreeRTOS firmware skills — NOT part of this repo

---

## 2. What PostureGuard is

**One-liner:** Real-time posture classification **on the M5StickS3**, using IMU data and a small TFLite Micro model.

**Pipeline:**
1. Sample BMI270 IMU (accel + gyro)
2. Window the data (target design: ~50 Hz, ~2 second windows)
3. Run on-device inference (TFLite Micro, prefer int8 quantized)
4. Show class + confidence on the Stick screen / serial
5. Debounced alert when "slouch" persists

**Classes (start with exactly 3):**
- upright
- slouch
- lean

**Disclaimer (always keep in README):** Ergonomics / wellness prototype. **Not a medical device.**

---

## 3. Why this project matters (product story)

- Shows end-to-end embedded + ML: sensors → train → deploy → measure
- Direct sequel to my Japan internship (same problem domain, upgraded hardware: StickS3)
- Targets roles: Firmware Intern, Embedded Software Intern, IoT / Edge ML Intern
- Success for recruiters = demo video/GIF + metrics table + clean README, not a messy Arduino sketch

---

## 4. Hard technical constraints

- Primary board: **M5StickS3 only** for this repo (not M5StickC Plus 2, not ESP32-C3)
- Firmware should eventually use concurrent structure (FreeRTOS tasks or clearly separated sense / infer / alert loops)
- ML validation must be **session-based hold-out** when possible (do not rely only on random row split)
- Do not commit huge raw datasets (`data/raw/` ignored). Only tiny samples in `data/sample/`
- Do not invent employers, metrics, logos, or "finished" claims
- Prefer PlatformIO or Arduino-ESP32 first for speed; ESP-IDF later if needed

---

## 5. Repository layout (keep this)

```text
edge-posture-monitor/
├── README.md
├── LICENSE
├── .gitignore
├── docs/
│   ├── design.md
│   └── results.md
├── firmware/
│   ├── README.md
│   ├── src/
│   └── model/
├── ml/
│   ├── requirements.txt
│   ├── README.md
│   ├── preprocess.py
│   ├── train.py
│   ├── export_tflite.py
│   └── notebooks/        # optional exploration only
├── data/
│   ├── README.md
│   └── sample/           # tiny CSVs only
└── scripts/
    └── record_serial.py
```

---

## 6. Definition of done (MVP)

MVP is done when ALL are true:

1. Labeled IMU data can be collected and saved as CSV
2. Offline training produces a small classifier + confusion matrix in docs/results.md
3. Model exports to TFLite (prefer int8) and fits onboard use
4. Firmware runs inference on device and prints/shows: class, confidence, latency_ms
5. Device runs stably for ~10 minutes without crash
6. README has: one-liner, architecture overview, metrics table, how to train, how to flash
7. Optional but strong: short demo video/GIF linked from README

Stretch (after MVP only):
- BLE / phone notification
- Power-mode notes
- Calibration mode

---

## 7. Build plan (follow this order)

### Phase A — Before hardware arrives (NOW)
- Finish repo polish (README, design.md, .gitignore)
- Build Python ML pipeline stubs → then real preprocess/train/export
- Use synthetic or public IMU data OR simulated windows first if needed
- Implement scripts/record_serial.py ready for when Stick arrives

### Phase B — Hardware week 1
- Flash M5StickS3 hello-world + screen
- Stream BMI270 IMU as CSV over serial
- Collect labeled sessions for 3 classes

### Phase C — Train for real
- Session-based train/test
- Baseline sklearn model, then small neural net for TFLite
- Document honest metrics in docs/results.md

### Phase D — On-device deploy
- Convert model → TFLite Micro C array in firmware/model/
- Inference loop + latency logging
- Sense / infer / alert structure

### Phase E — Polish for jobs
- Demo video, GIF, architecture diagram
- Tag release v0.1.0-mvp
- Resume bullets with real measured numbers only

---

## 8. Coding standards for you (Copilot)

When I ask you to work:

1. Make the **smallest next working change**
2. Explain briefly what you changed and how to test it
3. Update docs when behavior/metrics change
4. Keep commits meaningful (suggest commit messages)
5. If blocked by missing hardware: work on ML/scripts/docs instead
6. If a JD-style claim would be dishonest: refuse and say what is actually true
7. Prefer clear C++/Python over clever one-liners
8. Always keep recruiter README quality high

---

## 9. Current status (update this as we go)

- [x] Project chosen: PostureGuard / edge-posture-monitor
- [x] Hardware ordered: M5StickS3
- [x] Repo scaffold created and pushed to GitHub
- [ ] ML pipeline training on real/sample data
- [ ] Firmware IMU CSV streaming
- [ ] On-device TFLite inference
- [ ] Demo video + MVP metrics

---

## 10. First tasks I want you to help with

Unless I say otherwise, help in this order:

1. Confirm or improve repo scaffold + README quality
2. Implement honest starter versions of:
   - ml/preprocess.py
   - ml/train.py
   - ml/export_tflite.py
   - scripts/record_serial.py
3. Write clear ml/README.md and firmware/README.md
4. When I get the Stick: IMU serial logger firmware
5. Then training → export → on-device inference

---

## 11. Resume angle (for README / commit messages)

Emphasize:
- End-to-end edge ML wearable system
- IMU → train → quantized on-device inference
- FreeRTOS/task-oriented firmware structure
- Measured latency / model size / hold-out accuracy (only when real)

Avoid:
- Calling it medical
- Claiming research paper results I do not have
- Padding with unfinished Arduino course demos as the headline

# ML pipeline

Starter workflow:

1. Create a virtual environment.
2. Install dependencies from `requirements.txt`.
3. Prepare labeled sensor CSV files.
4. Run preprocessing to build clean training windows.
5. Train an initial baseline model.
6. Export a `.tflite` artifact for firmware integration.

Example commands:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python preprocess.py --input ..\data\sample --output .\artifacts\processed
python train.py --input .\artifacts\processed --output .\artifacts\training
python export_tflite.py --model-dir .\artifacts\training --output .\artifacts\model\posture_model.tflite
```

Everything in this directory is a starter scaffold. No dataset, trained model, or benchmarked result is included yet.

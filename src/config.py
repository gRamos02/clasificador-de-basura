import os
from pathlib import Path

# Rutas base
BASE_DIR = Path(__file__).parent.parent
WEIGHTS_DIR = BASE_DIR / "weights"
DATASET_DIR = BASE_DIR / "dataset"
TEST_DIR = BASE_DIR / "tests"

# Configuración del modelo
TRAINED_MODEL_PATH = WEIGHTS_DIR / "best.pt"
DATA_CONFIG_PATH = DATASET_DIR / "data.yaml"
DEFAULT_MODEL = "yolov8n.pt"

# Configuración de entrenamiento
TRAIN_CONFIG = {
    "epochs": 100,
    "batch": 32,
    "imgsz": 640,
}
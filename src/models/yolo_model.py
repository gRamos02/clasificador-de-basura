import torch
from ultralytics import YOLO
from src.config import TRAINED_MODEL_PATH, DATA_CONFIG_PATH, TRAIN_CONFIG

class BasuraDetector:
    def __init__(self, model_path=None):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = self._load_model(model_path)
        self.class_names = self.model.model.names

    def _load_model(self, model_path):
        if model_path and model_path.exists():
            return YOLO(model_path)
        elif TRAINED_MODEL_PATH.exists():
            return YOLO(TRAINED_MODEL_PATH)
        else:
            return YOLO("yolov8n.pt")

    def train(self):
        return self.model.train(
            data=DATA_CONFIG_PATH,
            device=self.device,
            **TRAIN_CONFIG
        )

    def predict(self, source):
        return self.model.predict(source=source, save=False)
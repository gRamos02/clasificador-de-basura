import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from ultralytics import YOLO
import torch
import glob

# Ruta donde se guardará el modelo entrenado
TRAINED_MODEL_PATH = "weights/best.pt"
DATA_CONFIG_PATH = "./dataset/data.yaml"
TEST_IMAGES_DIR = "./tests"

def load_model(model_path="yolov8n.pt"):
    """
    Cargar el modelo YOLOv8.
    Si existe un modelo entrenado, se carga; de lo contrario, se carga el modelo preentrenado.
    """
    if os.path.exists(TRAINED_MODEL_PATH):
        print(f"Modelo entrenado encontrado en {TRAINED_MODEL_PATH}. Cargando modelo entrenado.")
        return YOLO(TRAINED_MODEL_PATH)
    else:
        print(f"Modelo entrenado no encontrado. Cargando modelo preentrenado desde {model_path}.")
        return YOLO(model_path)

def preprocess_image(image_path, target_size=(640, 640)):
    """
    Preprocesar la imagen: cargar y redimensionar.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Imagen no encontrada o no válida: {image_path}")
    image = cv2.resize(image, target_size)
    return image

def train_model(
    data_config=DATA_CONFIG_PATH,
    model_path="yolov8n.pt",
    epochs=50,
    batch=16,
    imgsz=640,
    device='cuda' if torch.cuda.is_available() else 'cpu'
):
    """
    Entrenar el modelo YOLOv8 utilizando el dataset configurado en el archivo YAML.
    """
    model = YOLO(model_path)
    results = model.train(data=data_config, epochs=epochs, batch=batch, imgsz=imgsz, device=device)
    return model

def test_model_on_images(model, test_dir=TEST_IMAGES_DIR):
    """
    Procesar todas las imagenes en el directorio de prueba utilizando el modelo YOLOv8.
    """
    # Obtener todas las imagenes con extensiones comunes
    image_extensions = ('*.jpg', '*.jpeg', '*.png', '*.bmp')
    image_paths = []
    for ext in image_extensions:
        image_paths.extend(glob.glob(os.path.join(test_dir, ext)))

    if not image_paths:
        print(f"No se encontraron imágenes en el directorio {test_dir}.")
        return

    for image_path in image_paths:
        try:
            image = preprocess_image(image_path)
            results = model.predict(source=image, save=False)
            for result in results:
                result_img = result.plot()
                # Mostrar la imagen con las detecciones
                cv2.imshow(f"Detecciones - {os.path.basename(image_path)}", result_img)
                cv2.waitKey(0)
                cv2.destroyAllWindows()
        except Exception as e:
            print(f"Error procesando la imagen {image_path}: {e}")

def main():
    # Verificar si CUDA esta disponible
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Dispositivo utilizado para entrenamiento/inferencia: {device}")

    # Cargar o entrenar el modelo
    if os.path.exists(TRAINED_MODEL_PATH):
        model = load_model()
    else:
        print("Iniciando entrenamiento...")
        model = train_model(device=device)
        print("Entrenamiento completado.")

    # Procesar imagenes de prueba
    test_model_on_images(model)

if __name__ == "__main__":
    main()
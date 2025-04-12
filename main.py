import cv2
import numpy as np
import matplotlib.pyplot as plt
from ultralytics import YOLO

def load_model(model_path="yolov8m.pt"):
    """
    Cargar el modelo preentrenado YOLOv8
    
    model_path (str): nombre del modelo, n es nano, m medium, ver tamaños en docmunetaicon. 
    
    Returns:
        model: Loaded YOLOv8 model.
    """
    try:
        # Cargar el modelo preetrenado; aquí es donde se implementará el aprendizaje por transferencia
        model = YOLO(model_path)
        print(f"Modelo cargado: {model_path}")
        return model
    except Exception as e:
        print(f"Error cargando modelo: {e}")
        return None

def preprocess_image(image_path, target_size=(640, 640)):
    """
    Preprocesar la imagen: cargar, redimensionar y normalizar.
    
    Returns:
        image: imagen preprocesada lista para la inferencia.
    """
    image = cv2.imread(image_path)
    if image is None:
        raise ValueError("Imagen no encontrada o no válida.")
    
    # Convertir BGR a RGB si es necesario
    # image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Redimensionar la imagen a 640x640
    # image = cv2.resize(image, target_size)
    
    # Normalizar la imagen (escalar los valores de píxeles al rango 0-1)
    # image = image.astype('float32') / 255.0
    
    return image

def main():
    # Cargar el modelo (usando un modelo por defecto; reemplazar con su modelo ajustado más tarde)
    model = load_model()
    if model is None:
        return

    # Carar imagenes de prueba
    test_image_path = "./cat_dog.jpg"
    
    try:
        image = preprocess_image(test_image_path)
         
        print("Imagen preprocesada y lista para la inferencia.")
        
        # Realizar la inferencia y obtener resultados
        results = model.predict(image)
        print(results[0])
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()

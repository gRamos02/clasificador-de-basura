# import os
# import cv2
# import numpy as np
# import matplotlib.pyplot as plt
# from ultralytics import YOLO
# import torch
# import glob
# import streamlit as st

# from utils import TipoBasura

# # Ruta donde se guardará el modelo entrenado
# TRAINED_MODEL_PATH = "./weights/best.pt"
# DATA_CONFIG_PATH = "./dataset/data.yaml"
# TEST_IMAGES_DIR = "./tests"


# YOLO_CLASS_TO_CATEGORY = {
#     'metal': TipoBasura.RECICLABLE,
#     'glass': TipoBasura.RECICLABLE,
#     'biological': TipoBasura.ORGANICO,
#     'paper': TipoBasura.RECICLABLE,
#     'battery': TipoBasura.BATERIA,
#     'trash': TipoBasura.NO_RECICLABLE,
#     'cardboard': TipoBasura.RECICLABLE,
#     'shoes': TipoBasura.NO_RECICLABLE,
#     'clothes': TipoBasura.NO_RECICLABLE,
#     'plastic': TipoBasura.RECICLABLE
# }

# def load_model(model_path="yolov8n.pt"):
#     """
#     Cargar el modelo YOLOv8.
#     Si existe un modelo entrenado, se carga; de lo contrario, se carga el modelo preentrenado.
#     """
#     if os.path.exists(TRAINED_MODEL_PATH):
#         print(f"Modelo entrenado encontrado en {TRAINED_MODEL_PATH}. Cargando modelo entrenado.")
#         return YOLO(TRAINED_MODEL_PATH)
#     else:
#         print(f"Modelo entrenado no encontrado. Cargando modelo preentrenado desde {model_path}.")
#         return YOLO(model_path)

# def preprocess_image(image_path, target_size=(640, 640)):
#     """
#     Preprocesar la imagen: cargar y redimensionar.
#     """
#     image = cv2.imread(image_path)
#     if image is None:
#         raise ValueError(f"Imagen no encontrada o no válida: {image_path}")
#     image = cv2.resize(image, target_size)
#     return image

# def train_model(
#     data_config=DATA_CONFIG_PATH,
#     model_path="yolov8n.pt",
#     epochs=50,
#     batch=16,
#     imgsz=640,
#     device=None
# ):
#     """
#     Entrenar el modelo YOLOv8 utilizando el dataset configurado en el archivo YAML.
#     """
#     model = YOLO(model_path)
#     results = model.train(data=data_config, epochs=epochs, batch=batch, imgsz=imgsz, device=device)
#     return model

# def test_model_on_images(model, test_dir=TEST_IMAGES_DIR):
#     """
#     Procesar todas las imagenes en el directorio de prueba utilizando el modelo YOLOv8.
#     """
#     # Obtener todas las imagenes con extensiones comunes
#     image_extensions = ('*.jpg', '*.jpeg', '*.png', '*.bmp')
#     image_paths = []
#     for ext in image_extensions:
#         image_paths.extend(glob.glob(os.path.join(test_dir, ext)))

#     if not image_paths:
#         print(f"No se encontraron imágenes en el directorio {test_dir}.")
#         return

#     for image_path in image_paths:
#         try:
#             image = preprocess_image(image_path)
#             results = model.predict(source=image, save=False)
#             for result in results:
#                 result_img = result.plot()
#                 # Mostrar la imagen con las detecciones
#                 cv2.imshow(f"Detecciones - {os.path.basename(image_path)}", result_img)
#                 cv2.waitKey(0)
#                 cv2.destroyAllWindows()
#         except Exception as e:
#             print(f"Error procesando la imagen {image_path}: {e}")

# def map_detection_to_category(yolo_result, class_names):
#     # Devuelve un diccionario con conteo por categoría
#     categories_count = {}
#     for box in yolo_result.boxes:
#         class_idx = int(box.cls[0])
#         class_name = class_names[class_idx]
#         category = YOLO_CLASS_TO_CATEGORY.get(class_name, 'Desconocido')
#         categories_count[category] = categories_count.get(category, 0) + 1
#     return categories_count

# def main():
#     # Verificar si CUDA esta disponible
#     device = "cuda" if torch.cuda.is_available() else "cpu"
#     print(f"Dispositivo utilizado para entrenamiento/inferencia: {device}")
#     model = None
#     # Cargar o entrenar el modelo
#     if os.path.exists(TRAINED_MODEL_PATH):
#         model = load_model()
#     else:
#         print("Iniciando entrenamiento...")
#         model = train_model(device=device)
#         print("Entrenamiento completado.")

#     class_names = model.model.names
#     st.title("Detección de Objetos con YOLOv8")    
#     st.write("Modelo cargado y listo para realizar inferencias.")
#     run = st.button("Iniciar")
#     stop = st.button("Detener")
#     FRAME_WINDOW = st.image([])
#     if run:
#         cap = cv2.VideoCapture(0)
#         while cap.isOpened():
#             ret, frame = cap.read()
#             if not ret:
#                 st.error("No se pudo acceder a la cámara.")
#                 break
#             # Inferencia con YOLO
#             results = model.predict(source=frame, save=False)
#             for result in results:
#                 # Mapear resultados
#                 categories_count = map_detection_to_category(result, class_names)
#                 # Dibujar detecciones
#                 result_img = result.plot()
#                 FRAME_WINDOW.image(result_img, channels="BGR")
#                 # st.write("Conteo por categoría:", categories_count)
#             if stop:
#                 cap.release()
#                 break
#         cap.release()
#     # Procesar imagenes de prueba
#     # test_model_on_images(model)
from src.interface.streamlit_app import StreamlitApp

def main():
    app = StreamlitApp()
    app.run()

if __name__ == "__main__":
    main()

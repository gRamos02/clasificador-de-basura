import streamlit as st
import cv2
from src.models.yolo_model import BasuraDetector
from src.utils.enums import CLASS_TO_CATEGORY
from src.utils.enums import CATEGORY_TO_SIGNAL 
from src.comm.serial_controller import SerialController
import numpy as np
import time

class StreamlitApp:
    def __init__(self):
        self.detector = BasuraDetector()
        self.serial_controller = SerialController(
            port='COM18'  # Cambia el puerto manualmente 
        )
        # Intentar conectar al Arduino
        if self.serial_controller.connect():
            st.success("Arduino conectado correctamente")
        else:
            st.error("No se pudo conectar al Arduino")
        
    def run(self):
        st.title("Detección de Objetos con YOLOv8")
        st.write("Modelo cargado y listo para realizar inferencias.")
        
        # Agregar sidebar
        st.sidebar.title("Opciones de Detección")
        detection_mode = st.sidebar.radio(
            "Seleccione el modo de detección",
            ["Subir Imagen","Webcam"]
        )
        
        if detection_mode == "Webcam":
            self._webcam_detection()
        else:
            self._image_detection()
    
    def _webcam_detection(self):
        run = st.button("Iniciar Webcam")
        stop = st.button("Detener")
        FRAME_WINDOW = st.image([])
        
        if run:
            self._run_detection(FRAME_WINDOW, stop)
    
    def _image_detection(self):
        uploaded_file = st.file_uploader("Seleccione una imagen", type=['jpg', 'jpeg', 'png'])
        
        if uploaded_file is not None:
            # Convertir la imagen subida a un array de numpy
            file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, 1)
            
            # Realizar la detección
            results = self.detector.predict(image)
            for result in results:
                result_img = result.plot()
                st.image(result_img, channels="BGR", caption="Resultado de la detección")
                # Mostrar las clases detectadas en la imagen
                clases_detectadas = [self.detector.class_names[int(cls)] for cls in result.boxes.cls]
                categoria = CLASS_TO_CATEGORY[clases_detectadas[0]]
                senal_arduino = CATEGORY_TO_SIGNAL[categoria]
                st.write(f"Clase detectada: {clases_detectadas[0]} ({categoria})")
                
                # Enviar señal al Arduino
                try:
                    self.serial_controller.send_category(senal_arduino)
                    st.success(f"Señal enviada al Arduino: {categoria}")
                except Exception as e:
                    st.error(f"Error al enviar señal: {str(e)}")
    
    def _run_detection(self, frame_window, stop):
        cap = cv2.VideoCapture(0)
        last_detection_time = None
        last_detected_category = None
        DETECTION_THRESHOLD = 1.0  # Tiempo en segundos para confirmar detección

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.error("No se pudo acceder a la cámara.")
                break
                
            results = self.detector.predict(frame)
            current_time = time.time()
            
            for result in results:
                result_img = result.plot()
                frame_window.image(result_img, channels="BGR")
                
                if len(result.boxes) > 0:
                    # Obtener categoría actual
                    clases_detectadas = [self.detector.class_names[int(cls)] for cls in result.boxes.cls]
                    categoria_actual = CLASS_TO_CATEGORY[clases_detectadas[0]]
                    senal_arduino = CATEGORY_TO_SIGNAL[categoria_actual]
                    
                    # Si es una nueva categoría o primera detección
                    if categoria_actual != last_detected_category:
                        last_detection_time = current_time
                        last_detected_category = categoria_actual
                    # Si es la misma categoría, verificar tiempo
                    elif (current_time - last_detection_time) >= DETECTION_THRESHOLD:
                        try:
                            self.serial_controller.send_category(senal_arduino)
                            st.success(f"Señal enviada al Arduino: {categoria_actual}")
                            # Reiniciar temporizador después de enviar
                            last_detection_time = None
                            last_detected_category = None
                        except Exception as e:
                            st.error(f"Error al enviar señal: {str(e)}")
                else:
                    # Si no hay detección, reiniciar temporizador
                    last_detection_time = None
                    last_detected_category = None
                
            if stop:
                break
                
        cap.release()
        self.serial_controller.close()
import streamlit as st
import cv2
from src.models.yolo_model import BasuraDetector
from src.utils.enums import YOLO_CLASS_TO_CATEGORY

class StreamlitApp:
    def __init__(self):
        self.detector = BasuraDetector()
        
    def run(self):
        st.title("Detección de Objetos con YOLOv8")
        st.write("Modelo cargado y listo para realizar inferencias.")
        
        run = st.button("Iniciar")
        stop = st.button("Detener")
        FRAME_WINDOW = st.image([])
        
        if run:
            self._run_detection(FRAME_WINDOW, stop)
    
    def _run_detection(self, frame_window, stop):
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                st.error("No se pudo acceder a la cámara.")
                break
                
            results = self.detector.predict(frame)
            for result in results:
                result_img = result.plot()
                frame_window.image(result_img, channels="BGR")
                
            if stop:
                break
                
        cap.release()
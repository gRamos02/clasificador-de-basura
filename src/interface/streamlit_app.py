import streamlit as st
import cv2
from src.models.yolo_model import BasuraDetector
from src.utils.enums import CLASS_TO_CATEGORY
from src.utils.enums import CATEGORY_TO_SIGNAL 
from src.comm.serial_controller import SerialController
import numpy as np
import time

# Configuración de la página - DEBE SER LO PRIMERO
st.set_page_config(
    page_title="Clasificador de Basura",
    page_icon="♻️",
    layout="wide"
)

class StreamlitApp:
    def __init__(self):
        self.detector = BasuraDetector()
        self.serial_controller = SerialController(
            port='COM18'  # Cambia el puerto manualmente 
        )
        # Intentar conectar al Arduino
        if self.serial_controller.connect():
            st.success("Sistema de recolección conectado correctamente")
        else:
            st.error("No se pudo conectar al Sistema de recolección")
        
    def run(self):
        # Página principal
        st.title("🤖 Sistema de Clasificación de Basura")
        st.markdown("---")

        # Descripción del proyecto
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("""
            ### Sobre el Proyecto
            Este sistema utiliza inteligencia artificial para clasificar residuos en tiempo real,
            ayudando a mejorar la gestión de residuos mediante:

            - 🔍 Detección automática usando YOLOv8
            - 📊 Clasificación en 4 categorías principales
            - 🔌 Integración con Arduino para señalización visual
            - 📷 Soporte para imágenes y detección en tiempo real
            """)

        # Estadísticas o información relevante
        st.markdown("---")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Categorías", "4")
        with col2:
            st.metric("Clases", "10")
        # with col3:
        #     st.metric("Precisión", "89%")
        with col4:
            st.metric("Estado", "En línea")

        # Agregar sidebar y opciones de detección
        st.sidebar.title("Opciones de Detección")
        detection_mode = st.sidebar.radio(
            "Seleccione el modo de detección",
            ["Inicio", "Subir Imagen", "Webcam"]
        )
        
        if detection_mode == "Webcam":
            self._webcam_detection()
        elif detection_mode == "Subir Imagen":
            self._image_detection()
        else:
            # Mostrar información de categorías
            st.markdown("### Categorías de Clasificación")
            categorias = {
                "♻️ Reciclable": "Metal, Vidrio, Papel, Cartón, Plástico",
                "🗑️ No Reciclable": "Basura general, Zapatos, Ropa",
                "🔋 Batería": "Baterías y dispositivos electrónicos",
                "🥬 Orgánico": "Residuos biológicos y alimentos"
            }
            
            for cat, desc in categorias.items():
                with st.expander(cat):
                    st.write(desc)

        # Agregar sección de créditos al final
        st.markdown("---")
        st.markdown("### 👥 Equipo de Desarrollo")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            - **Jorge Sepulveda Fraire**
              - No. Control: C21130330
            - **Sergio Daniel Chiquito Zuñiga**
              - No. Control: 21130605
            """)
        
        with col2:
            st.markdown("""
            - **Delma Guadalupe Castillo Jimenez**
              - No. Control: 21130885
            - **Gerardo Enrique Ramos Espinoza**
              - No. Control: 21130599
            """)

        st.markdown("---")
        st.markdown("*Proyecto desarrollado para la materia de Inteligencia Artificial - Instituto Tecnológico de La Laguna*")
        st.markdown("### Docente: Gibran López")
    
    def _webcam_detection(self):
        # Obtener cámaras disponibles
        cameras = get_available_cameras()
        if not cameras:
            st.error("No se detectaron cámaras disponibles")
            return
        
        # Selector de cámara
        selected_camera = st.selectbox(
            "Seleccionar cámara",
            options=cameras,
            index=0
        )
        
        camera_index = int(selected_camera.split()[-1])  # Obtiene el número de la cámara
        
        run = st.button("Iniciar Webcam")
        stop = st.button("Detener")
        FRAME_WINDOW = st.image([])
        
        if run:
            self._run_detection(FRAME_WINDOW, stop, camera_index)
    
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
                    st.success(f"Señal enviada al Sistema de recolección: {categoria}")
                except Exception as e:
                    st.error(f"Error al enviar señal: {str(e)}")
    
    def _run_detection(self, frame_window, stop, camera_index=0):
        cap = cv2.VideoCapture(camera_index)
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
                            st.success(f"Señal enviada al Sistema de recolección: {categoria_actual}")
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
        

def get_available_cameras():
    """Obtiene una lista de cámaras disponibles"""
    cameras = []
    index = 0
    while True:
        cap = cv2.VideoCapture(index)
        if not cap.read()[0]:
            break
        cameras.append(f"Cámara {index}")
        cap.release()
        index += 1
    return cameras

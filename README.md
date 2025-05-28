
# Clasificación de Basura con YOLOv8

Este proyecto implementa un sistema de clasificación de basura utilizando el modelo YOLOv8 y técnicas de aprendizaje por transferencia. El objetivo es detectar y clasificar diferentes tipos de residuos en imágenes, facilitando su separación y reciclaje.

## Requisitos Previos

- Python 3.8 o superior
- Git (opcional, para clonar el repositorio)

## Configuración del Entorno

1. **Clonar el Repositorio**

   ```bash
   git clone https://github.com/tu_usuario/tu_repositorio.git
   cd tu_repositorio
   ```

2. ***Crear un Entorno Virtual***

   Es recomendable utilizar un entorno virtual para gestionar las dependencias del proyecto.

   ```bash
   python -m venv env
   ```

   Para activar el entorno virtual:

   - En Windows:

     ```bash
     .\env\Scripts\activate
     ```

   - En macOS/Linux:

     ```bash
     source env/bin/activate
     ```

3. **Instalación de Dependencias**

   Instala las dependencias necesarias utilizando `pip`:

   ```bash
   pip install -r requirements.txt
   ```

## Descarga del Dataset

[Dataset del proyecto](https://universe.roboflow.com/ia-wx3de/clasificacion-de-basura-wxd8k)

Y coloca las carpetas test, train y valid dentro de ./dataset/

- `dataset/`: Contiene las imágenes y etiquetas utilizadas para el entrenamiento.
- `tests/`: Carpeta donde puedes colocar imágenes externas para probar el modelo.
- `main.py`: Script principal que ejecuta el entrenamiento y la inferencia.
- `requirements.txt`: Lista de dependencias del proyecto.
- `README.md`: Este archivo con las instrucciones del proyecto.

## Ejecución del Proyecto

1. **Entrenamiento del Modelo**

   Para iniciar el proyecto, ejecuta:

   ```bash
   streamlit run main.py
   ```

   El script verificará si existe un modelo previamente entrenado. Si no lo encuentra, iniciará el proceso de entrenamiento utilizando el dataset proporcionado.

2. **Prueba del Modelo**

   Después del entrenamiento, el modelo realizará inferencias sobre las imágenes ubicadas en la carpeta `tests/`. Los resultados se mostrarán en ventanas emergentes con las detecciones realizadas.

## Notas Adicionales

- Asegúrate de que las imágenes de prueba en la carpeta `tests/` tengan formatos compatibles como `.jpg`, `.jpeg`, `.png` o `.bmp`.
- Si deseas modificar parámetros de entrenamiento como el número de épocas, tamaño de lote o tamaño de imagen, puedes hacerlo editando la función `train_model` en `main.py`.

## Recursos

- [Documentación de YOLOv8](https://docs.ultralytics.com/)
- [Kaggle: Garbage Classification v2](https://www.kaggle.com/datasets/sumn2u/garbage-classification-v2)
- [Ultralytics GitHub](https://github.com/ultralytics/ultralytics)
- [Como detectar imagenes usando YOLOv8](https://www.freecodecamp.org/news/how-to-detect-objects-in-images-using-yolov8/)


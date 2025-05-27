import cv2

def preprocess_image(image_path, target_size=(640, 640)):
    """
    Preprocesar la imagen: cargar y redimensionar.
    """
    image = cv2.imread(str(image_path))
    if image is None:
        raise ValueError(f"Imagen no encontrada o no válida: {image_path}")
    image = cv2.resize(image, target_size)
    return image

def map_detection_to_category(yolo_result, class_names, category_mapping):
    categories_count = {}
    for box in yolo_result.boxes:
        class_idx = int(box.cls[0])
        class_name = class_names[class_idx]
        category = category_mapping.get(class_name, 'Desconocido')
        categories_count[category] = categories_count.get(category, 0) + 1
    return categories_count
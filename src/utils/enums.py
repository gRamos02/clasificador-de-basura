from enum import Enum, auto

class TipoBasura(Enum):
    RECICLABLE = auto()
    NO_RECICLABLE = auto()
    BATERIA = auto()
    ORGANICO = auto()

    def __str__(self):
        return self.name.lower().replace('_', ' ')

# Mapeo de clases YOLO a categorías
CLASS_TO_CATEGORY = {
    'metal': TipoBasura.RECICLABLE,
    'glass': TipoBasura.RECICLABLE,
    'biological': TipoBasura.ORGANICO,
    'paper': TipoBasura.RECICLABLE,
    'battery': TipoBasura.BATERIA,
    'trash': TipoBasura.NO_RECICLABLE,
    'cardboard': TipoBasura.RECICLABLE,
    'shoes': TipoBasura.NO_RECICLABLE,
    'clothes': TipoBasura.NO_RECICLABLE,
    'plastic': TipoBasura.RECICLABLE
}

CATEGORY_TO_SIGNAL = {
    TipoBasura.RECICLABLE: 'R',
    TipoBasura.NO_RECICLABLE: 'N',
    TipoBasura.BATERIA: 'B',
    TipoBasura.ORGANICO: 'O'
}
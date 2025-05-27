from enum import Enum, auto

class TipoBasura(Enum):
    RECICLABLE = auto()
    NO_RECICLABLE = auto()
    BATERIA = auto()
    ORGANICO = auto()

    def __str__(self):
        return self.name.lower().replace('_', ' ')
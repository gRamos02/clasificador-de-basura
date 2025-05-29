import serial
import time
from serial.tools import list_ports

class SerialController:
    def __init__(self, baudrate=9600, timeout=1, port=None):
        self.baudrate = baudrate
        self.timeout = timeout
        self.port = port 
        self.serial = None

    def list_available_ports(self):
        """Lista todos los puertos seriales disponibles"""
        return [port.device for port in list_ports.comports()]

    def connect(self):
        """Conecta al puerto serial especificado o al primer puerto disponible"""
        try:
            if self.port is None:
                available_ports = self.list_available_ports()
                if not available_ports:
                    raise Exception("No se encontraron puertos seriales disponibles")
                self.port = available_ports[0]

            self.serial = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout
            )
            self.port = self.port
            time.sleep(2)  # Esperar a que Arduino se reinicie
            return True
        except Exception as e:
            print(f"Error al conectar al puerto serial: {e}")
            return False

    def send_category(self, category):
        """Envía una categoría al Arduino"""
        if not self.serial or not self.serial.is_open:
            raise Exception("El puerto serial no está conectado")
        
        valid_categories = {'O', 'B', 'R', 'N'}
        if category not in valid_categories:
            raise ValueError(f"Categoría inválida. Debe ser una de: {valid_categories}")
        
        try:
            self.serial.write(category.encode())
            time.sleep(0.1)  # Pequeña pausa para asegurar el envío
            return True
        except Exception as e:
            print(f"Error al enviar categoría: {e}")
            return False

    def close(self):
        """Cierra la conexión serial"""
        if self.serial and self.serial.is_open:
            self.serial.close()

# Probando funcionamiento
if __name__ == "__main__":
    controller = SerialController(port='COM18')  # Cambia el puerto según tu sistema
    
    
    # Listar puertos disponibles
    print("Puertos disponibles:", controller.list_available_ports())
    
    # Conectar al primer puerto disponible
    if controller.connect():
        print(f"Conectado al puerto {controller.port}")
        
        # Ejemplo de envío de categorías
        categorias = ['O', 'B', 'R', 'N']
        for cat in categorias:
            print(f"Enviando categoría: {cat}")
            controller.send_category(cat)
            time.sleep(6)  # Esperar a que el LED se apague
            
        controller.close()
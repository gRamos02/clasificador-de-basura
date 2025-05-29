/*
  Indicador de Clasificación de Basura
  Sistema de LEDs para indicar la categoría de basura detectada por la cámara.
  
  Categorías:
    O - Orgánica
    B - Batería
    R - Reciclable
    N - No Reciclable
*/

// Definición de pines
const int LED_ORGANICA = 2;
const int LED_BATERIA = 3;
const int LED_RECICLABLE = 4;
const int LED_NO_RECICLABLE = 5;

// Array de LEDs para facilitar operaciones
const int NUM_LEDS = 4;
const int LEDS[NUM_LEDS] = {
  LED_ORGANICA,
  LED_BATERIA,
  LED_RECICLABLE,
  LED_NO_RECICLABLE
};

// Constantes de tiempo
const unsigned long TIEMPO_ENCENDIDO = 5000;    // 5 segundos para visualización
const unsigned long TIEMPO_MINIMO = 1000;       // 1 segundo mínimo
const unsigned long TIEMPO_MAXIMO = 10000;      // 10 segundos máximo

// Variables de control de tiempo
unsigned long tiempoUltimoLED = 0;
bool ledEncendido = false;
int categoriaActual = -1;

void setup() {
  // Inicializar todos los pines LED
  for (int i = 0; i < NUM_LEDS; i++) {
    pinMode(LEDS[i], OUTPUT);
  }
  Serial.begin(9600);
  // Parpadeo inicial para confirmar que el sistema está listo
  parpadeoInicial();
}

void loop() {
  unsigned long tiempoActual = millis();
  if (ledEncendido && (tiempoActual - tiempoUltimoLED >= TIEMPO_ENCENDIDO)) {
    apagarTodosLEDs();
    ledEncendido = false;
    delay(500);
    limpiarBufferSerial();
    return;
  } else if (ledEncendido) {
    return;
  }
  // Solo procesar nuevas entradas si no hay un LED encendido
  if (Serial.available() > 0) {
    Serial.println("Si entro");
    char categoria = Serial.read();
    if (categoria == 'O' || categoria == 'B' || categoria == 'R' || categoria == 'N') {
      actualizarLEDs(categoria);
      ledEncendido = true;
      tiempoUltimoLED = tiempoActual;
      limpiarBufferSerial();  // Limpia cualquier entrada adicional
    }// else {
    //   secuenciaError();
    // }
  }

}

void actualizarLEDs(char categoria) {
  apagarTodosLEDs();
  
  switch (categoria) {
    case 'O':
      digitalWrite(LED_ORGANICA, HIGH);
      Serial.println("Detectado: Orgánico");
      break;
    case 'B':
      digitalWrite(LED_BATERIA, HIGH);
      Serial.println("Detectado: Batería");
      break;
    case 'R':
      digitalWrite(LED_RECICLABLE, HIGH);
      Serial.println("Detectado: Reciclable");
      break;
    case 'N':
      digitalWrite(LED_NO_RECICLABLE, HIGH);
      Serial.println("Detectado: No Reciclable");
      break;
  }
}

void apagarTodosLEDs() {
  for (int i = 0; i < NUM_LEDS; i++) {
    digitalWrite(LEDS[i], LOW);
  }
}

void parpadeoInicial() {
  for (int i = 0; i < 3; i++) {
    for (int j = 0; j < NUM_LEDS; j++) {
      digitalWrite(LEDS[j], HIGH);
    }
    delay(100);
    apagarTodosLEDs();
    delay(100);
  }
}

void secuenciaError() {
  // Parpadeo rápido de todos los LEDs para indicar error
  for (int i = 0; i < 5; i++) {
    for (int j = 0; j < NUM_LEDS; j++) {
      digitalWrite(LEDS[j], HIGH);
    }
    delay(100);
    apagarTodosLEDs();
    delay(100);
  }
}

void limpiarBufferSerial() {
  while (Serial.available() > 0) {
    Serial.read();
  }
}

// Definimos los pines para los botones
#define BTN_PUNCH_BLUE  13
#define BTN_BODY_BLUE   12
#define BTN_HEAD_BLUE   14

#define BTN_PUNCH_RED   27
#define BTN_BODY_RED    26
#define BTN_HEAD_RED    25

#define DEBOUNCE_DELAY 500

volatile bool sendPunch = true;

// Estructura para almacenar los datos del jugador
typedef struct player_data {
  char player;
  uint8_t points;
};
volatile player_data data = {'n', 0}; // Inicializar struct con valores por defecto

// Variables de debounce específicas para cada botón
volatile unsigned long lastDebounceTimeBluePunch = 0;
volatile unsigned long lastDebounceTimeBlueBody = 0;
volatile unsigned long lastDebounceTimeBlueHead = 0;
volatile unsigned long lastDebounceTimeRedPunch = 0;
volatile unsigned long lastDebounceTimeRedBody = 0;
volatile unsigned long lastDebounceTimeRedHead = 0;

// Rutinas de interrupciones
void IRAM_ATTR btn_blue_punch_pressed() {
  unsigned long currentTime = millis();
  if ((currentTime - lastDebounceTimeBluePunch) > DEBOUNCE_DELAY) {
    lastDebounceTimeBluePunch = currentTime;
    data.player = 'A';
    if (sendPunch) {
      data.points = 1;
    } else {
      sendPunch = true;
    }
  }
}

void IRAM_ATTR btn_blue_body_pressed() {
  unsigned long currentTime = millis();
  if ((currentTime - lastDebounceTimeBlueBody) > DEBOUNCE_DELAY) {
    lastDebounceTimeBlueBody = currentTime;
    data.player = 'A';
    if (digitalRead(BTN_PUNCH_BLUE)) {
      data.points = 4;
      sendPunch = false;
    } else {
      data.points = 2;
    }
  }
}

void IRAM_ATTR btn_blue_head_pressed() {
  unsigned long currentTime = millis();
  if ((currentTime - lastDebounceTimeBlueHead) > DEBOUNCE_DELAY) {
    lastDebounceTimeBlueHead = currentTime;
    data.player = 'A';
    if (digitalRead(BTN_PUNCH_BLUE)) {
      data.points = 5;
      sendPunch = false;
    } else {
      data.points = 3;
    }
  }
}

void IRAM_ATTR btn_red_punch_pressed() {
  unsigned long currentTime = millis();
  if ((currentTime - lastDebounceTimeRedPunch) > DEBOUNCE_DELAY) {
    lastDebounceTimeRedPunch = currentTime;
    data.player = 'R';
    if (sendPunch) {
      data.points = 1;
    } else {
      sendPunch = true;
    }
  }
}

void IRAM_ATTR btn_red_body_pressed() {
  unsigned long currentTime = millis();
  if ((currentTime - lastDebounceTimeRedBody) > DEBOUNCE_DELAY) {
    lastDebounceTimeRedBody = currentTime;
    data.player = 'R';
    if (digitalRead(BTN_PUNCH_RED)) {
      data.points = 4;
      sendPunch = false;
    } else {
      data.points = 2;
    }
  }
}

void IRAM_ATTR btn_red_head_pressed() {
  unsigned long currentTime = millis();
  if ((currentTime - lastDebounceTimeRedHead) > DEBOUNCE_DELAY) {
    lastDebounceTimeRedHead = currentTime;
    data.player = 'R';
    if (digitalRead(BTN_PUNCH_RED)) {
      data.points = 5;
      sendPunch = false;
    } else {
      data.points = 3;
    }
  }
}

void setup() {
  pinMode(BTN_PUNCH_BLUE, INPUT_PULLDOWN);
  pinMode(BTN_BODY_BLUE, INPUT_PULLDOWN);
  pinMode(BTN_HEAD_BLUE, INPUT_PULLDOWN);

  pinMode(BTN_PUNCH_RED, INPUT_PULLDOWN);
  pinMode(BTN_BODY_RED, INPUT_PULLDOWN);
  pinMode(BTN_HEAD_RED, INPUT_PULLDOWN);

  attachInterrupt(digitalPinToInterrupt(BTN_PUNCH_BLUE), btn_blue_punch_pressed, FALLING);
  attachInterrupt(digitalPinToInterrupt(BTN_BODY_BLUE), btn_blue_body_pressed, RISING);
  attachInterrupt(digitalPinToInterrupt(BTN_HEAD_BLUE), btn_blue_head_pressed, RISING);

  attachInterrupt(digitalPinToInterrupt(BTN_PUNCH_RED), btn_red_punch_pressed, FALLING);
  attachInterrupt(digitalPinToInterrupt(BTN_BODY_RED), btn_red_body_pressed, RISING);
  attachInterrupt(digitalPinToInterrupt(BTN_HEAD_RED), btn_red_head_pressed, RISING);

  // Inicializar monitor serie
  Serial.begin(9600);
}

void loop() {
  if (data.points != 0) {
    Serial.print(data.player);
    Serial.println(data.points);
    data.points = 0;
  }
}

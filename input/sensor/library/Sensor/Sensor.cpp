#include <Sensor.h>

Sensor::Sensor(const char pin): pin(pin) {
  pinMode(pin, INPUT);
  callback = NULL;
}

void Sensor::setCallback(sensor_callback_t callback) {
  this -> callback = callback;
}


void Sensor::check() {      // sensor detection 체크
  bool value;
  
  value = digitalRead(pin);

  if(value == 0){     // sensor detected 시점
    if(callback != NULL) {
      callback();
    }
  }
}

int Sensor::read() {    // detected 경우 H, not detected 경우 L 리턴
  return !digitalRead(pin);
}

void Sensor::attachInterrupt(sensor_callback_t callback, int mode) {
  ::attachInterrupt(digitalPinToInterrupt(pin), callback, mode);
}
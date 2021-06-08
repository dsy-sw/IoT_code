#pragma once

#include <Arduino.h>

typedef void (*sensor_callback_t)();    // 함수에 대한 포인터를 sensor_callback_t로 정의

class Sensor{
  protected:
    const char pin;
    // void (*callback)();   // 콜백 함수(함수에 대한 포인터)
    sensor_callback_t callback;
    unsigned long t1;     // unsigned : 부호가 없다 = 양수만 가능

  public:
    Sensor(const char pin);
    void setCallback(sensor_callback_t callback);
    void check();
    int read();
    void attachInterrupt(sensor_callback_t callback, int mode);
};
#pragma once

#include <Arduino.h>
#include <LiquidCrystal_I2C.h>
#include <SimpleTimer.h>

class MiniCom {
protected:
  int serial_bps;
  LiquidCrystal_I2C lcd;
  SimpleTimer timer;

public:
  MiniCom(int Serial_bps=9600, int lcd_addr=0x27);
  void init();
  int setInterval(unsigned long interval, timer_callback f);
  void run();
  SimpleTimer& getTimer() { return timer; }

  // LCD 출력 지원 메서드(helper 함수)
  void print(int row, const char *pMsg, bool bserial=false);
  void print_i(int row, String title, int value, bool bserial=false);
  void print_i(int row, String title1, int value1, String title2, int value2, bool bserial=false);
  void print_d(int row, String title, double value, bool bserial=false);
};
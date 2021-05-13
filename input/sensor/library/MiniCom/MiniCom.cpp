#include <MiniCom.h>

MiniCom::MiniCom(int serial_bps, int lcd_addr)
  : serial_bps(serial_bps), lcd(lcd_addr, 16, 2) {
}

void MiniCom::init() {
  Serial.begin(serial_bps);
  lcd.begin();
}

int MiniCom::setInterval(unsigned long interval, timer_callback f) {
  return timer.setInterval(interval, f);
}

void MiniCom::run() {
  timer.run();
}

void MiniCom::print(int row, const char *pMsg, bool bserial) {
  char buf[17];
  sprintf(buf, "%-16s", pMsg);
  lcd.setCursor(0, row);
  lcd.print(buf);

  if(bserial) {
    Serial.println(buf);
  }
}

void MiniCom::print_i(int row, String title, int value, bool bseiral) {
  String buf = title + value;
  print(row, buf.c_str(), bseiral);
}

void MiniCom::print_i(int row, String title1, int value1, String title2, int value2, bool bserial) {
  String buf = title1 + value1 + "," + title2 + value2;
  print(row, buf.c_str(), bserial);
}

void MiniCom::print_d(int row, String title, double value, bool bseiral) {
  String buf = title + value;
  print(row, buf.c_str(), bseiral);
}
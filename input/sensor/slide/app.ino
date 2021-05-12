#include <MqttCom.h>
#include <Sensor.h>

const char *ssid = "TECH2_2G";
const char *password = "tech21234!";
const char *server =  "172.30.1.3";
// const char *ssid = "DO";
// const char *password = "ehtldud123";
// const char *server =  "192.168.0.10";
const char *pub_topic = "door/msg";

MqttCom com(ssid, password);
Sensor sensor(D6);

void publishWorking() {
  com.publish("door/work", "working on");
}

void publish_sensor(){
  com.publish(pub_topic, "door_open");
}

void setup(){
  Serial.begin(115200);
  com.init(server);                         // publish만 실행
  com.setInterval(30000, publishWorking);   // 센서 작동 중인지 확인
  sensor.setCallback(publish_sensor);       // 센서 감지 시 콜백
}

void loop(){
  com.run();
  sensor.check();
}
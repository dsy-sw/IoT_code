#include <MqttCom.h>
#include <Sensor.h>


const char *ssid = "dsy_msi";
const char *password = "1q2w3e4r";
const char *server =  "192.168.137.36";
// const char *ssid = "DO";
// const char *password = "ehtldud123";
// const char *server =  "192.168.0.10";
const char *pub_topic = "input/sensor";

MqttCom com(ssid, password);
Sensor sensor(D6);

void publishWorking() {
  com.publish("input/lift/work", "working on");
}

ICACHE_RAM_ATTR void publish_sensor(){
  com.publish(pub_topic, "detected");
}


void setup()
{
  Serial.begin(115200);
  com.init(server);                         // publish만 실행
  com.setInterval(30000, publishWorking);   // 센서 작동 확인
  sensor.setCallback(publish_sensor);       // 센서 감지 시 콜백
}

void loop()
{
  com.run();
  sensor.run(publish_sensor, 3000);
}
#include <MqttCom.h>
#include <Servo.h>


const char *ssid = "TECH2_2G";
const char *password = "tech21234!";
const char *server =  "172.30.1.107";
const char *sub_topic = "iot/gate/request";

MqttCom com(ssid, password);
Servo servo;

void publish() {
  com.publish("iot/gate/work", "working on");
}

void subscribe(char* topic, uint8_t* payload, unsigned int length) {
  char buf[128];
  memcpy(buf, payload, length);
  buf[length] = '\0';
  // String ms = String(char* buf);
  String ms = buf;
  
  Serial.print(topic);
  Serial.println(buf);

  if(ms == "open"){
    servo_control();
  }

}

void servo_control(){
  servo.write(90);
  com.publish("iot/gate/control","open");
  Serial.println("open");
  delay(3000);
  servo.write(0);
  com.publish("iot/gate/control","close");
  Serial.println("close");
}

void setup()
{
  Serial.begin(115200);
  servo.attach(D6);
  com.init(server, sub_topic, subscribe);   // subscribe하는 경우
  com.setInterval(60000, publish);
}

void loop()
{
  com.run();
}
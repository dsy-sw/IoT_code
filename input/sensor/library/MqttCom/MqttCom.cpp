#include <MqttCom.h>

MqttCom::MqttCom(const char *ssid, const char *password): 
  MiniCom(115200), ssid(ssid), password(password), client(espClient) {
  topic = NULL;
  callback = NULL;
  server = NULL;
  randomSeed(analogRead(0));
  int r = random(300);
  client_id = String("ESP8266Client") + r;
}

void MqttCom::wifi_connect(){
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println(WiFi.localIP());

  lcd.setCursor(0, 0);
  lcd.print("WiFi connected");
  lcd.setCursor(0, 1);
  lcd.print(WiFi.localIP());
}

void MqttCom::init(const char *server, const char *topic, MQTT_CALLBACK_SIGNATURE) {
  this->server = server;
  this->callback = callback;
  this->topic = topic;

  MiniCom::init();
  wifi_connect();

  client.setServer(server, 1883);

  if(callback != NULL) {
    client.setCallback(callback);
  }
}

void MqttCom::reconnect() {
  while(!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    print(0, "try MQTT con...");
    if(client.connect(client_id.c_str())) {
      Serial.println("connected");
      print(1, "connected");
      if(topic != NULL) {
        client.subscribe(topic);
      }
    } else {
      char buf[17];
      sprintf(buf, "failed, rc=%d", client.state());
      Serial.print(buf);
      print(0, buf);
      Serial.println("try agian in 5 seconds");
      print(1, "try again in 5 sec");
      delay(5000);
    }
  }
}

void MqttCom::run() {
  MiniCom::run();

  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}

void MqttCom::publish(const char *topic, const char *value) {
  client.publish(topic, value);
}
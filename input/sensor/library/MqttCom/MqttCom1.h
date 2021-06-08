#pragma once

#include <MiniCom.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

class MqttCom: public MiniCom {
  protected:
  const char *server;       // MQTT 서버 주소
  const char *ssid;         // 네트워크 ID
  const char *password;     // 네트워크 비밀번호
  String client_id;         // MQTT 클라이언트 ID
  WiFiClient espClient;     // WiFi 객체
  PubSubClient client;      // MQTT 클라이언트 객체
  const char *topic;        // 구독할 토픽명
  MQTT_CALLBACK_SIGNATURE;  // 구독 콜백 함수 포인터

  public:
  MqttCom(const char *ssid, const char *password);
  void wifi_connect();
  void init(const char *server, const char *topic = NULL, MQTT_CALLBACK_SIGNATURE = NULL);
  void reconnect();
  void run();
  void publish(const char *topic, const char *value);
};
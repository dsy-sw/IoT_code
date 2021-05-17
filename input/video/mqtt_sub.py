import paho.mqtt.client as mqtt
from _thread import *


def subscribe(host, topic, forever=True):
    def on_connect(client, userdata, flags, rc):
        print(f"Connected server with result code {rc}")
        if rc == 0:
            client.subscribe(topic)  # 연결 성공시 토픽 구독 신청
        else:
            print('연결 실패 : ', rc)

    def on_message(client, userdata, msg):
        msg = str(msg.payload)
        print("Received :", msg.topic," ",msg)

    client = mqtt.Client()
    try:
        client.connect(host)
        client.on_connect = on_connect
        client.on_message = on_message
        if forever:
            client.loop_forever()
        else:
            client.loop_start()
    except Exception as err:
        print('Error :', err)

from video import Video
from os import path
from cv2.data import haarcascades
import socket
import json
import net
import time
import cv2
from _thread import *
import paho.mqtt.client as mqtt

HOST = '15.161.17.179'
PORT = 5000
door_topic='door/#'

client = mqtt.Client()


def detect_face(frame):
  face_xml = path.join(haarcascades, 'haarcascade_frontalface_default.xml')
  face_cascade = cv2.CascadeClassifier(face_xml)

  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  face = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(0,0))
  if len(face) == 0:
    return 0
  else:
    faces = face.shape[0]
    if faces > 0:
      num_detections = faces
      return num_detections


def show_image(data):
  cv2.imshow('frame', data)
  cv2.waitKey(0.5)


def server_msg(reader):
    request = net.receive(reader)[0]
    if len(request) > 0:
        print(json.loads(request.decode()))       # 전송 결과

def camera(ip, port):
  start_time = time.time()    # 시작 시간
  need_second = 2
  print(ip, port)
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((ip, port))

    writer = s.makefile('wb')
    reader = s.makefile('rb')
    with Video(device = 0) as v:    # 카메라 번호 지정
    # with Video(file = 'test_people.jpg') as v:    # 카메라 번호 지정
      middle_time = time.time()
      check = middle_time - start_time    # 사전 작업시간
      num_detections, image_data = 0, []
      for i in range(5):
        v.cap.read()
      for image in v:
        Video.show(image)                       # 영상 스트리밍
        num_detection = detect_face(image)      # 검출 인원 수 체크
        print(num_detection)
        if time.time() - middle_time > need_second:
          break         # 지정된 n초 후 break
        elif num_detection == 0:
          continue

        if num_detection > num_detections:
          num_detections = num_detection        # 최대로 인원 수 갱신
          image_data = Video.to_jpg(image)   # jpg파일 압축
          print(type(image_data))
      if len(image_data) == 0:                    # 이미지가 없으면
        print('no data')
      else:
        print("Number of faces detected: ", num_detections)
        net.send(writer, image_data)            # 서버로 데이터 전송
        print('video send ', len(image_data), '/', 'people :', num_detections)
        server_msg(reader)

    end_time = time.time()    # 끝나는 시간
    print('사전 작업시간 :', check)
    print('전체 시간 : ', end_time - start_time)

# if __name__ == '__main__':
#   print('start client...')
#   # start_new_thread(subscribe, (HOST, door_topic))
#   vclient(HOST, PORT, camera)

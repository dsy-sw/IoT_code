from cam import USBCam
from video import Video
from os import path
from cv2.data import haarcascades
import socket
import json
import net
import time
import cv2
# from detection import detect_face

HOST = '218.38.254.30'
PORT = 5000

second = 3
time_end = time.time() + second

face_xml = path.join(haarcascades, 'haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier(face_xml)


def detect_face(frame):
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(150, 150))
  if len(faces) == 0:
    return False
  elif len(faces) > 0:
    num_detection = len(faces)
    return num_detection


def show_image(data):
  cv2.imshow('frame', image)
  cv2.waitKey(1)


def server_msg(reader):
    request = net.receive(reader)[0]
    if len(request) > 0:
        print(json.loads(request.decode()))        # 전송 결과


if __name__ == '__main__':
  start_time = time.time()    # 시작 시간
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    writer = s.makefile('wb')
    reader = s.makefile('rb')
    with Video(device=0) as v:    # 카메라 번호 지정
      num_detections = 0
      image_data = []
      for image in v:
        show_image(image)                       # 영상 스트리밍
        num_detection = detect_face(image)      # 검출 인원 수 체크
        print(num_detection)
        if time.time() > time_end:
          break         # 지정된 n초 후 break
        elif num_detection == False:
          continue

        if num_detection > num_detections:
          num_detections = num_detection        # 최대로 인원 수 갱신
          image_data = Video.to_jpg(image, 80)   # jpg파일 압축
      if len(image_data) > 0:                   # 이미지 데이터가 있으면
        net.send(writer, image_data)            # 서버로 데이터 전송
        print('video send ', len(image_data), '/', 'people :', num_detections)
        server_msg(reader)
      elif len(image_data) == 0:
        print('no data')
    #   cv2.imshow('frame', image_data)
    #   cv2.waitKey(1)
  end_time = time.time()    # 끝나는 시간

  print('작업 시간 : ', end_time - start_time-second)
  print('전체 시간 : ', end_time - start_time)
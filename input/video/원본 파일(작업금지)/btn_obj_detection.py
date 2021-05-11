import cv2
from cv2.data import haarcascades
from os import path
from video import Video
from gpiozero import Button
from gpiozero import LED
import numpy as np

button_off = Button(21, bounce_time=0.05)
button_on = Button(16, bounce_time=0.05)
led = LED(20)
video_on = False

face_xml = path.join(haarcascades, 'haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier(face_xml)

empty_image = np.full((480, 640, 3), (128, 128, 128), dtype=np.uint8)
FACE_WIDTH = 200

def detect_face(frame):
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  faces = face_cascade.detectMultiScale(gray, 1.3, 5)
  for (x,y,w,h) in faces:
    minLength = min(w,h)
    if minLength <150: break
    width = max(w,h)

    # 얼굴 부분 검출
    x = x+w//2 - width//2
    y = y+h//2 - width//2
    face_image = frame[y:y+width, x:x+width].copy()

    # 얼굴 영역 표시
    cv2.rectangle(frame, (x,y), (x+width, y+width), (255,0,0), 2)

    # 얼굴 부분만 좌측 상단에 출력
    face_image = cv2.resize(face_image, dsize=(FACE_WIDTH, FACE_WIDTH), interpolation=cv2.INTER_AREA)
    frame[0:FACE_WIDTH, 0:FACE_WIDTH] = face_image[:]

  return frame

def start():
  global video_on
  print('video on')
  video_on = True
  led.on()

def end():
  global video_on
  print('end')
  video_on = False
  led.off()

button_on.when_pressed = start
button_off.when_pressed = end

with Video(device=0) as v:
  for image in v:
    if video_on:
      # image = detect_face(image)
      Video.show(image)
    else:
      Video.show(empty_image)

    if not Video.show(image): break


cv2.destroyAllWindows()
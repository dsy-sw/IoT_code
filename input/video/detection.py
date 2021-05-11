from os import path
from cv2.data import haarcascades
import cv2

face_xml = path.join(haarcascades, 'haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier(face_xml)

def detect_face(frame):
  global num_detection
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(150,150))
  if len(faces) == 0:
    return False
  elif len(faces) > 0:
    num_detection = len(faces)
    return num_detection
import net
import json
import numpy as np
import cv2

HOST = '218.38.254.30'
PORT = 5000

def receiver(client, addr):
  reader = client.makefile('rb')
  writer = client.makefile('wb')
  while True:
    data, data_len = net.receive(reader)
    if not data:
      break
    print('received', data_len)   # 이미지 처리
    show_image(data)
    result = json.dumps({'result':'ok'})
    net.send(writer, result.encode())

  print('exit receiver')

def show_image(data):
  # byte 배열을 numpy로 변환
  data = np.frombuffer(data, dtype=np.uint8)
  image=cv2.imdecode(data, cv2.IMREAD_COLOR)
  cv2.imshow('frame', image)
  cv2.waitKey(1)

if __name__ == '__main__':
  print('start server...')
  net.server(HOST, PORT, receiver)


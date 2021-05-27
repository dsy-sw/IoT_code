import net
import json
import numpy as np
import cv2


HOST = '218.38.254.30'
PORT = 5000

ix = 0

def receiver(client, addr):
  reader = client.makefile('rb')
  writer = client.makefile('wb')
  try:
    data, data_len = net.receive(reader)
    if not data:
      print('no data')
    print('received', data_len)   # 이미지 처리
    # print(location)
    # save_image(data)
    save_image(data)
    result = json.dumps({'url':'https://yangjae-team08-bucket.s3.eu-south-1.amazonaws.com/Ecoche.mp4', 'ad_file' : 'Ecoche'})
    net.send(writer, result.encode())
  except Exception as e:
    print('Error :', e)

  print('exit receiver')

def show_image(data):
  # byte 배열을 numpy로 변환
  data = np.frombuffer(data, dtype=np.uint8)
  image = cv2.imdecode(data, cv2.IMREAD_COLOR)
  cv2.imshow('frame', image)
  cv2.waitKey(1)

def save_image(img):
  global ix
  data = np.frombuffer(img, dtype=np.uint8)
  image=cv2.imdecode(data, cv2.IMREAD_COLOR)
  # cv2.imwrite(f'/home/ubuntu/iot/save_img/face_{ix:04d}.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 90])
  cv2.imwrite(f'C:/iot_workspace/project/input/video\save_img/face_{ix:04d}.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 100])
  ix += 1

if __name__ == '__main__':
  try:
    print('start server...')
    net.server(HOST, PORT, receiver)
  except Exception as err:
      print('에러 : %s' % err)
  except KeyboardInterrupt:
      print('수동 종료')
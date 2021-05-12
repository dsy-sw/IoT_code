from video import Video
from time import sleep
import socket, json, net

HOST = '127.0.0.1'
PORT = 5000

if __name__ == '__main__':
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    writer = s.makefile('wb')
    reader = s.makefile('rb')
    with Video(device=1) as v:
      for image in v:
        image = Video.to_jpg(image,80)
        print('video send ', len(image))
        net.send(writer, image)

        result = net.receive(reader)[0]
        print(json.loads(result.decode()))

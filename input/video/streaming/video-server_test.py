import net
import json
import numpy as np
import cv2
import pymysql
import pandas as pd
from tensorflow import keras
import random
from mtcnn.mtcnn import MTCNN
import matplotlib.image as img
import matplotlib.pyplot as plt
import time
from PIL import Image
import base64
from io import BytesIO

# HOST = '172.30.1.55'
HOST = '15.161.17.179'
PORT = 22

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
    ai(data)
    result = json.dumps({'result':'ok'})
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

def face_crop(IoT_Input):
    detector = MTCNN()
    result_list = detector.detect_faces(IoT_Input)
    face_list = []
    for i in range(len(result_list)):
        result_list2 = []
        for v in result_list[i]['box']:
            if v >= 0:
                result_list2.append(v)
            else:
                result_list2.append(0)
        x1, y1, width, height = result_list2
        x2, y2 = x1 + width, y1 + height
        cropped = cv2.resize(IoT_Input[y1:y2, x1:x2], (64, 64))
        cropped = cropped.astype('float32')
        cropped /= 255.
        cropped = cropped.reshape(-1, 64, 64, 3)
        face_list.append(cropped)
    return face_list

def load_models():
    model_age = keras.models.load_model('/home/ubuntu/ai/models/test_CNN_age_model.h5')
    model_gender = keras.models.load_model('/home/ubuntu/ai/models/test_CNN_gender_model.h5')

    return model_age, model_gender

def predict_models(model_age, model_gender,cropped_image):
    age_idx = 0
    age_result = ''
    gender_result = ''

    age = model_age.predict(cropped_image)  # [아동 2030 4050 실버]

    for i in range(len(age[0])):
        if age[0][i] == max(age[0]):
            age_idx = i

    if age_idx == 0:
        age_result = 'kids'
    elif age_idx == 1:
        age_result = '2030'
    elif age_idx == 2:
        age_result = '4050'
    else:
        age_result = 'silver'

    if age_result == 'kids' or age_result == 'silver':
        return age_result, -1
    else:
        gender = model_gender.predict(cropped_image)  # 0 남자 1 여자
        if gender[0][0] > 0.5:
            gender_result = 'woman'
        else:
            gender_result = 'man'
        return age_result, gender_result

def select_AD(count_list):  # [kids, 2030M, 2030W, 4050M, 4050W, silver]
    max_index = []
    count_max = max(count_list)
    for i, n in enumerate(count_list):
        if n == count_max:
            max_index.append(i)
    selected_index = random.choice(max_index)

    if selected_index == 0:
        return 'kids', '-1'
    elif selected_index == 1:
        return '2030', '남자'
    elif selected_index == 1:
        return '2030', '여자'
    elif selected_index == 1:
        return '4050', '남자'
    elif selected_index == 1:
        return '4050', '여자'
    else:
        return 'silver', '-1'

def ai(data):
    count_list = [0, 0, 0, 0, 0, 0]
    conn = pymysql.connect(host='yangjae-team08-database.ca8iiefanafw.eu-south-1.rds.amazonaws.com',
                         port=3306, user='admin', password='yangjae8', db='mydb', charset='utf8')
    cur = conn.cursor()

    tm = time.localtime((time.time()))
    data_date = f'{tm.tm_year}_{tm.tm_mon}_{tm.tm_mday}_{tm.tm_min}_{tm.tm_sec}'
    faces_list = face_crop(data)
    model_age, model_gender = load_models()
    cam_location = 'Seoul'

    temp_age = []
    temp_gender = []
    temp_crop = []

    for i, face in enumerate(faces_list):
        buffer = BytesIO()
        age_result, gender_result = predict_models(model_age, model_gender, face)

        face = face.reshape(64, 64, 3)
        face_jpg = Image.fromarray((face * 255).astype(np.uint8))
        face_jpg.save(buffer, format = 'jpeg')
        face_byte = base64.b64encode(buffer.getvalue())

        if age_result == 'kids':
            count_list[0] += 1
        elif age_result == '2030' and gender_result == 'man':
            count_list[1] += 1
        elif age_result == '2030' and gender_result == 'woman':
            count_list[2] += 1
        elif age_result == '4050' and gender_result == 'man':
            count_list[3] += 1
        elif age_result == '4050' and gender_result == 'woman':
            count_list[4] += 1
        else:
            count_list[5] += 1

        temp_age.append(age_result)
        temp_gender.append(gender_result)
        temp_crop.append(face_byte)

    selected_age, selected_gender = select_AD(count_list)

    if selected_age == 'kids' or selected_age == 'silver':
        sql_select_AD = f'SELECT ad_id, ad_name, budget FROM advert WHERE target_age = "{selected_age}"'
        cur.execute(sql_select_AD)
        ad_id, ad_name, budget = cur.fetchone()
    else:
        sql_select_AD = f'SELECT ad_id, ad_name, budget FROM advert WHERE target_age = "{selected_age}" AND target_gender = "{selected_gender}"'
        cur.execute(sql_select_AD)
        ad_id, ad_name, budget = cur.fetchone()

    for crop, age, gender in zip(temp_crop, temp_age, temp_gender):
        # INSERT face Table
        sql_face = '''INSERT INTO face(face_array, input_image, location)
                VALUES(%s, %s, %s)'''
        cur.execute(sql_face, [crop, data_date, cam_location])
        conn.commit()

        # MAX(face_id)
        sql_face_id = '''SELECT MAX(face_id) FROM face'''
        cur.execute(sql_face_id)
        face_id = cur.fetchone()

        # INSERT target Table SQL
        sql_target = '''INSERT INTO target(face_id, ad_id, age, gender)
                VALUES(%s, %s, %s, %s)'''
        cur.execute(sql_target, [face_id, ad_id, age, gender])
        conn.commit()

if __name__ == '__main__':
  print('start server...')
  net.server(HOST, PORT, receiver)
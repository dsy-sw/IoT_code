
  data = np.frombuffer(data, dtype=np.uint8)
  image=cv2.imdecode(data, cv2.IMREAD_COLOR)
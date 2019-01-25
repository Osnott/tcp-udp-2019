import cv2
import numpy as np
import pickle
import socket
import sys

UDP_IP = "localhost"
UDP_PORT = 7446
# camera = cv2.VideoCapture(0)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    data = "".encode('utf-8')
    sock.sendto(data, (UDP_IP, UDP_PORT))
    bytes_data = sock.recv(65536)
    data = pickle.loads(bytes_data)
    # print(type(data))
    # grabbed, frame = camera.read()
    # frame = cv2.flip(frame, 1)
    decimg = cv2.imdecode(data, 1)
    cv2.imshow("Jetson Camera", decimg)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
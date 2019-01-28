import cv2
import numpy as np
import pickle
import socket
import sys
import time
import threading
import select

UDP_IP = "192.168.43.235"
UDP_PORT = 9999
# camera = cv2.VideoCapture(0)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(5)
pings = []
packets_lost = 0
start = 0
end = 0

data = "W".encode('utf-8')
sock.sendto(data, (UDP_IP, UDP_PORT))

while True:
    start = time.time()
    try:
        bytes_data = sock.recv(65536)
    except socket.timeout as e:
        print("ERROR! CONNECTION LOST!")
        print("\nEXITING")
        sys.exit(0)
    except ConnectionResetError as e:
        print("ERROR! COULD NOT ESTABLISH A CONNECTION!")
        sys.exit(0)
    end = time.time()
    if data == "":
        print("ERROR! LOST A PACKET!")
        packets_lost = packets_lost + 1
    else:
        data = pickle.loads(bytes_data)
        # print(type(data))
        # grabbed, frame = camera.read()
        # frame = cv2.flip(frame, 1)
        decimg = cv2.imdecode(data, 1)
        cv2.imshow("Jetson Camera", decimg)
        ping = ((end-start) * 1000)
        print("Ping: " + str(ping))
        pings.append(ping)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        top_ping = 0
        all_pings = 0
        for ping in pings:
            if ping > top_ping:
                top_ping = ping
            all_pings += ping
        print("\nEXITING\n-----------------")
        print("Total Pings: " + str(len(pings)))
        print("Top Ping: " + str(top_ping))
        print("Average Ping: " + str(all_pings/len(pings)))
        print("Packets Lost: " + str(packets_lost))
        break

cv2.destroyAllWindows()

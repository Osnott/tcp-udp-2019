import socketserver
import sys
import pickle
import cv2


class DriverstationConnectionHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # initial = self.request[0].strip()
        socket = self.request[1]
        print("CONNECTED")
        packets = 0
        while True:
            # print("CONNECTED: " + str(initial.decode('utf-8')))
            grabbed, feed = camera.read()
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 10]
            result, encimg = cv2.imencode('.jpg', feed, encode_param)
            packet = pickle.dumps([encimg, packets])
            socket.sendto(packet, self.client_address)
            packets = packets + 1


camera = cv2.VideoCapture(0)
HOST, PORT = str(sys.argv[1]), 1183  # 192.168.43.235
print("STARTING SERVER ON " + HOST + " ON PORT " + str(PORT))
server = socketserver.UDPServer((HOST, PORT), DriverstationConnectionHandler)
print("SERVER ONLINE")
server.serve_forever()

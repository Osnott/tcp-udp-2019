import socketserver
import pickle
import cv2


class UDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # initial = self.request[0].strip()
        socket = self.request[1]
        packets = 0
        while True:
            # print("CONNECTED: " + str(initial.decode('utf-8')))
            grabbed, feed = camera.read()
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 40]
            result, encimg = cv2.imencode('.jpg', feed, encode_param)
            packet = pickle.dumps([encimg, packets])
            socket.sendto(packet, self.client_address)
            packets = packets + 1


camera = cv2.VideoCapture(0)
HOST, PORT = "localhost", 9999  # 192.168.43.235
server = socketserver.UDPServer((HOST, PORT), UDPHandler)
server.serve_forever()

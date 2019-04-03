import socketserver
import sys
import pickle
import cv2


class DriverstationConnectionHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # initial = self.request[0].strip()
        socket = self.request[1]
        print("CONNECTED")
        while True:
            # print("CONNECTED: " + str(initial.decode('utf-8')))
            grabbed, feed = camera.read()
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 10]
            result, encimg = cv2.imencode('.jpg', feed, encode_param)
            packet = pickle.dumps(encimg)
            socket.sendto(packet, self.client_address)


camera = cv2.VideoCapture(0)
HOST, PORT = str(sys.argv[1]), 9999  # 192.168.43.235
print("STARTING SERVER ON " + HOST + " ON PORT " + str(PORT))
server = socketserver.UDPServer((HOST, PORT), DriverstationConnectionHandler)
print("SERVER ONLINE")
server.serve_forever()


# class DriverstationConnectionFactoryThread(StoppableThread):
#     def __init__(self):
#         self._HOST, self._PORT = netifaces.ifadresses("eth0")[netifaces.AF_INET][0]["addr"], 9999
#         self._server = socketserver.UDPServer((self._HOST, self._PORT), DriverstationConnectionHandler())
#
#     def run(self):
#         try:
#             self._server.serve_forever()
#         except Exception:
#             self.stop()
#
#     def stop(self):
#         self._server.shutdown()

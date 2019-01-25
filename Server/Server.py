import socketserver
import pickle
import cv2

class UDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        initial = self.request[0].strip()
        socket = self.request[1]
        grabbed, feed = camera.read()
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 40]
        result, encimg = cv2.imencode('.jpg', feed, encode_param)
        feed_as_bytes = pickle.dumps(encimg)
        # print(type(encimg))
        # print(type(feed_as_bytes))
        socket.sendto(feed_as_bytes, self.client_address)

camera = cv2.VideoCapture(0)
HOST, PORT = "localhost", 7446
server = socketserver.UDPServer((HOST, PORT), UDPHandler)
server.serve_forever()
import socketserver
import pickle
import cv2

class UDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        initial = self.request[0].strip()
        socket = self.request[1]
        packets = 0
        while True:
            print("CONNECTED: " + str(initial.decode('utf-8')))
            grabbed, feed = camera.read()
            encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 40]
            result, encimg = cv2.imencode('.jpg', feed, encode_param)
            feed_as_bytes = pickle.dumps(encimg)
            pickled_packets = pickle.dumps(packets)
            packet = pickle.dumps([feed_as_bytes, pickled_packets])
            socket.sendto(packet, self.client_address)
            if packets >= 30:
                packets = 0
            else:
                packets = packets + 1

camera = cv2.VideoCapture(0)
HOST, PORT = "192.168.43.235", 9999
server = socketserver.UDPServer((HOST, PORT), UDPHandler)
server.serve_forever()
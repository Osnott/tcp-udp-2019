import socketserver
from Camera import VideoCamera

class UDPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        try:
            socket = self.request[1]
            camera = VideoCamera(10)
            feed = camera.get_frame()
            socket.sendto(feed, self.client_address)
        except KeyboardInterrupt:
            camera.__del__()


if __name__ == "__main__":
    HOST, PORT = "localhost", 5005
    server = socketserver.UDPServer((HOST, PORT), UDPHandler)
    server.serve_forever()
import socket
import time

# init vars
TCP_IP = '127.0.0.1'
TCP_PORT = 5050
BUFFER_SIZE = 1024

# connect to socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind to port and start listening for incoming connection requests
s.bind((TCP_IP, TCP_PORT))
s.listen(1)

print('Listening for connection...')

# accept incoming request
conn, addr = s.accept()

print('Connection address: ' + str(addr))
# receive data
data = conn.recv(BUFFER_SIZE)
print("received data " + data.decode('utf-8'))
# send back data
conn.send(data)
print("sent data " + data.decode('utf-8'))
# close socket connection
conn.close()
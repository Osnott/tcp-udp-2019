import socket

# init vars
TCP_IP = '127.0.0.1' # 192.168.1.7
TCP_PORT = 5050
BUFFER_SIZE = 1024

# connect to socket
s = openSocket(TCP_IP, TCP_PORT)

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





async def openSocket(ip = '127.0.0.1', port = 5050):
  """
  Opens connection to ip and port provided, defalts to 127.0.0.1 and 5050
  """
  # connect to socket
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  # bind to port and start listening for incoming connection requests
  s.bind((ip, port))
  s.listen(1)
  return s
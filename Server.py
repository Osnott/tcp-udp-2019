import socket
from enum import Enum
from Camera import VideoCamera

class ConnectionType(Enum):
  TCP = 0
  UDP = 1

def openSocket(ip = '127.0.0.1', port = 5050, type = ConnectionType.TCP):
  """
  Opens connection to ip and port provided, defalts to 127.0.0.1 and 5050
  """
  # connect to socket
  if (ConnectionType.TCP):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind to port and start listening for incoming connection requests
    s.bind((ip, port))
    s.listen(1)
  else:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  return s

def parseData(data):
  if (data[0] == 'GET'):
    pass
  elif (data[0] == 'SET'):
    pass

def sendVideoStream(s, stream, ip, port):
  s.sendto(stream, (ip, port))

def gen(camera):
  while True:
    frame = camera.get_frame()
    yield (b'--frame\r\n'
      b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


#########################################################################################################################################################################
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------#
#####################################################################################################################sorry thomas i didnt wanna make another file########


# init vars
CONNECTION_TYPE = ConnectionType.UDP
IP = '127.0.0.1' # 192.168.1.7
PORT = 5005
BUFFER_SIZE = 1024

# connect to socket
s = openSocket(IP, PORT, CONNECTION_TYPE)

print('Listening for connection...')

if (CONNECTION_TYPE == ConnectionType.TCP):
  # accept incoming request
  conn, addr = s.accept()
  print('Connection address: ' + str(addr))
  # receive data
  rawData = conn.recv(BUFFER_SIZE)
  # decode data
  decodedData = rawData.decode('utf-8')

  print("received data " + decodedData)
  # splits decoded data into an array
  dataArray = rawData.decode('utf-8').split(' ')
  # parses get or set
  parseData(dataArray)
  print("sent data " + rawData)
  # close socket connection
  conn.close()
elif (CONNECTION_TYPE == ConnectionType.UDP):

  feed = VideoCamera().get_frame()
  sendVideoStream(s, feed, IP, PORT)
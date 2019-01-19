import socket
from enum import Enum
from Camera import VideoCamera

class ConnectionType(Enum):
  TCP = 0
  UDP = 1

def openSocket(ip = '127.0.0.1', port = 5050, connType = ConnectionType.TCP):
  """
  Opens connection to IP and port provided, defaults to 127.0.0.1 and 5050
  """
  # connect to socket
  if (connType == ConnectionType.TCP):
    print("Opening TCP server")
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # bind to port and start listening for incoming connection requests
    s.bind((ip, port))
    print('Listening for connection...')
    s.listen(1)
  else:
    print("Opening UDP server")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((ip, port))
  return s

def parseData(data):
  if (data[0] == 'GET'):
    pass
  elif (data[0] == 'SET'):
    pass

def sendVideoStream(s, stream, ip, port):
  s.sendto(stream, (ip, port))


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
  camera = VideoCamera()
  while(True):
    feed = camera.get_frame()
    sendVideoStream(s, feed, IP, PORT)

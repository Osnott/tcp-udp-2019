import pickle
import socket
import queue
import cv2

failedInit = False


class FrameQueue(queue.LifoQueue):
    """
    LifoQueue for incoming frames to get the most recent for lower latency
    """

    def _get(self):
        return self.queue[-1]

    def put(self, item):
        if self.full():
            try:
                del self.queue[0]
            except Exception:
                pass
        self._put(item)


def openServer(ip, port):
    """
    Connect to the server specified in the ip and port parameters
    """
    global failedInit

    failedInit = False
    client = {
        "sock": socket.socket(socket.AF_INET, socket.SOCK_DGRAM),
        "pings": [],
        "packets_lost": 0,
        "start": 0,
        "end": 0,
        "expected_packet": 0,
        "recv_packet": 0,
    }

    client["sock"].settimeout(5)
    data = "W".encode("utf-8")
    client["sock"].sendto(data, (ip, port))
    return client


def initRecvData(sock, buffer):
    """
    Recieves data and also checks for timeouts and disconnects.
    """
    global failedInit

    try:
        bytes_data = sock.recv(buffer)
    except socket.timeout:
        print("ERROR! CONNECTION LOST OR SERVER NOT OPEN!\n")
        print("EXITING")
        failedInit = True
        bytes_data = b""
    except ConnectionResetError:
        print("ERROR! COULD NOT ESTABLISH A CONNECTION!\n")
        print("EXITING")
        failedInit = True
        bytes_data = b""
    return bytes_data


def recvData(sock, buffer):
    """
    Recieves data and also checks for timeouts and disconnects.
    """
    try:
        bytes_data = sock.recv(buffer)
    except socket.timeout:
        bytes_data = b""
    except ConnectionResetError:
        bytes_data = b""
    return bytes_data


def keepAlive(sock, ip, port):
    """
    Sends the keep alive
    """

    data = "W".encode("utf-8")
    sock.sendto(data, (ip, port))


def decodeData(bytes_data):
    """
    Decodes data and returns the package number and decoded image.
    """
    data = pickle.loads(bytes_data)
    img = data[0]
    recv_packet = data[1]
    decimg = cv2.imdecode(img, 1)
    return recv_packet, decimg


def checkLostPackets(expected_packet, recv_packet, packets_lost):
    """
    Preforms checks for lost packets
    """
    if expected_packet != recv_packet:
        packets_lost = packets_lost + (recv_packet - expected_packet)
        expected_packet = recv_packet + 1
    else:
        expected_packet = expected_packet + 1
    return expected_packet, packets_lost


def calculatePings(pings):
    """
    Calculates top and total pings
    """
    top_ping = 0
    all_pings = 0
    if len(pings) >= 900:
        pings.clear()
        pings.append(0)
    for ping in pings:
        if ping > top_ping:
            top_ping = ping
        all_pings += ping
    return top_ping, all_pings, pings

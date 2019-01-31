import cv2
import pickle
import socket
import sys


def openServer(ip, port):
    """
    Connect to the server specified in the ip and port parameters
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)
    pings = []
    packets_lost = 0
    start = 0
    end = 0
    expected_packet = 0
    recv_packet = 0

    data = "W".encode('utf-8')
    sock.sendto(data, (ip, port))
    return sock, pings, packets_lost, start, end, expected_packet, recv_packet


def recvData(sock, buffer):
    """
    Recieves data and also checks for timeouts and disconnects.
    """
    try:
        bytes_data = sock.recv(buffer)
    except socket.timeout:
        print("ERROR! CONNECTION LOST OR SERVER NOT OPEN!\n")
        print("EXITING")
        sys.exit(0)
    except ConnectionResetError:
        print("ERROR! COULD NOT ESTABLISH A CONNECTION!\n")
        print("EXITING")
        sys.exit(0)
    return bytes_data


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
        print("--------------------LOST PACKET(S) OR FRAME OUT OF ORDER!--------------------")
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
    for ping in pings:
        if ping > top_ping:
            top_ping = ping
        all_pings += ping
    return top_ping, all_pings
